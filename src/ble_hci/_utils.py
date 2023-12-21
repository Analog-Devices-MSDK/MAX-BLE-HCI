from typing import Optional, Union, List
from enum import Enum
from multiprocessing import Process
from threading import Event, Lock, Thread
import sys
import datetime
import time
import weakref

import serial

from ._hci_logger import get_formatted_logger
from .packet_defs import ADI_PORT_BAUD_RATE, PacketType
from .hci_packets import (
    AsyncPacket,
    CommandPacket,
    Endian,
    EventPacket,
    ExtendedPacket,
    _byte_length
)

def to_le_nbyte_list(value: int, n_bytes: int):
    little_endian = []
    for i in range(n_bytes):
        num_masked = (value & (0xFF << 8 * i)) >> (8 * i)
        little_endian.append(num_masked)
    return little_endian


def le_list_to_int(nums: List[int]) -> int:
    full_num = 0
    for i, num in enumerate(nums):
        full_num |= num << 8 * i
    return full_num

_MAX_U16 = 2**16 - 1
_MAX_U32 = 2**32 - 1
_MAX_U64 = 2**64 - 1


class PhyOption(Enum):
    """PHY Options"""

    P1M = 1
    P2M = 2
    PCODED = 3


class SerialUartTransport:
    def __new__(cls, *args, **kwargs):
        if "instances" not in cls.__dict__:
            cls.instances = weakref.WeakValueDictionary()
        
        serial_port = kwargs.get("port_id", args[0])
        if serial_port in cls.instances:
            cls.instances[serial_port].stop()
            cls.instances[serial_port].port.flush()
        
        cls.instance = super(SerialUartTransport, cls).__new__(cls)
        cls.instances[serial_port] = cls.instance

        return cls.instance

    def __init__(
        self,
        port_id: str,
        baud: int = ADI_PORT_BAUD_RATE,
        id_tag: str = "DUT",
        logger_name: str = "BLE-HCI",
        retries: int = 0,
        timeout: float = 1.0
    ):
        self.port_id = port_id
        self.port = None
        self.id_tag = id_tag
        self.logger = get_formatted_logger(name=logger_name)
        self.retries = retries
        self.timeout = timeout

        self._event_packets = []
        self._async_packets = []
        self._read_thread = None
        self._kill_evt = None
        self._data_lock = None
        self._port_lock = None

        self._init_port(port_id, baud)
        self._init_read_thread()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with self._port_lock:
            self.stop()
            self.port.close()

    def __del__(self):
        if self._read_thread.is_alive():
            self.stop()

    def start(self):
        self._read_thread.start()

    def stop(self):
        self._kill_evt.set()
        self._read_thread.join()

    def send_command(
        self, pkt: CommandPacket, timeout: Optional[float] = None
    ) -> EventPacket:
        """Sends a command to the test board and retrieves the response.

        PRIVATE

        """
        return self._write(pkt.to_bytes(), timeout)
    
    def retrieve_packet(self, timeout: Optional[float] = None):
        return self._retrieve(timeout)

    def _init_read_thread(self) -> None:
        self._kill_evt = Event()
        self._read_thread = Thread(
            target=self._read,
            args=(self._kill_evt,),
            daemon=True,
            name=f"Thread-{self.id_tag}",
        )
        self._data_lock = Lock()
        self._port_lock = Lock()
        self.start()

    def _init_port(self, port_id: str, baud: int) -> None:
        """Initializes serial port.

        PRIVATE

        """
        try:
            self.port = serial.Serial(
                port=port_id,
                baudrate=baud,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                rtscts=False,
                dsrdtr=False,
                timeout=2.0,
            )
        except serial.SerialException as err:
            self.logger.error("%s: %s", type(err).__name__, err)
            sys.exit(1)
        except OverflowError as err:
            self.logger.error("Baud rate exception, %i is too large", baud)
            self.logger.error("%s: %s", type(err).__name__, err)
            sys.exit(1)

    def _read(self, kill_evt: Event) -> None:
        while not kill_evt.is_set():
            if self.port.in_waiting and self._port_lock.acquire(blocking=False):
                pkt_type = self.port.read(1)
                if pkt_type[0] == PacketType.ASYNC.value:
                    read_data = self.port.read(4)
                    data_len = read_data[2] | (read_data[3] << 8)
                else:
                    read_data = self.port.read(2)
                    data_len = read_data[1]

                read_data += self.port.read(data_len)
                self._port_lock.release()
                self.logger.info(
                    "%s  %s<%02X%s",
                    datetime.datetime.now(),
                    self.id_tag,
                    pkt_type[0],
                    read_data.hex(),
                )

                with self._data_lock:
                    if pkt_type[0] == PacketType.ASYNC.value:
                        self._async_packets.append(AsyncPacket.from_bytes(read_data))
                    else:
                        self._event_packets.append(EventPacket.from_bytes(read_data))

    def _retrieve(self, timeout: Optional[float]) -> Union[EventPacket, AsyncPacket]:
        """Reads event from serial port.
        Returns
        ----------
        Event: EventPacket

        """
        if timeout is None:
            timeout = self.timeout

        def _wait_timeout():
            time.sleep(timeout)
            return 0

        timeout_process = Process(target=_wait_timeout)
        timeout_process.start()

        while True and self._read_thread.is_alive():
            if self._event_packets:
                timeout_process.terminate()
                timeout_process.join()
                timeout_process.close()
                break
            if timeout_process.exitcode is None:
                continue
            raise TimeoutError(
                "Timeout occured before DUT could respond. Check connection and retry."
            )

        with self._data_lock:
            evt = self._event_packets.pop(0)

        return evt

    def _write(self, pkt: bytearray, timeout: Optional[float]) -> EventPacket:
        """Sends a data stream to the test board and retrieves the response.

        PRIVATE

        """
        tries = self.retries
        self.logger.info("%s  %s>%s", datetime.datetime.now(), self.id_tag, pkt.hex())
        timeout_err = None

        self.port.flush()
        self.port.write(pkt)
        while tries >= 0 and self._read_thread.is_alive():
            try:
                return self._retrieve(timeout)
            except TimeoutError as err:
                tries -= 1
                timeout_err = err
                self.logger.warning(
                    "Timeout occured. Retrying. %d retries remaining.", tries + 1
                )

        raise TimeoutError("Timeout occured. No retries remaining.") from timeout_err
