#! /usr/bin/env python3
###############################################################################
#
#
# Copyright (C) 2023 Maxim Integrated Products, Inc., All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of Maxim Integrated
# Products, Inc. shall not be used except as stated in the Maxim Integrated
# Products, Inc. Branding Policy.
#
# The mere transfer of this software does not imply any licenses
# of trade secrets, proprietary technology, copyrights, patents,
# trademarks, maskwork rights, or any other form of intellectual
# property whatsoever. Maxim Integrated Products, Inc. retains all
# ownership rights.
#
##############################################################################
#
# Copyright 2023 Analog Devices, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################
"""
Contains serial port functionality for the HCI implementation.
"""
# pylint: disable=too-many-instance-attributes, too-many-arguments
from typing import Optional, Callable, Any
from multiprocessing import Process
from threading import Event, Lock, Thread
import sys
import datetime
import time
import weakref

import serial

from ._hci_logger import get_formatted_logger
from .hci_packets import AsyncPacket, CommandPacket, EventPacket
from .packet_codes import EventCode
from .packet_defs import PacketType
from .constants import ADI_PORT_BAUD_RATE


class SerialUartTransport:
    """HCI UART serial port transportation object.

    Class defines the implementation of a thread-based UART
    serial port transportation object. The object is used
    by the HCI to retrieve and sort both event packet and
    asynchronous packets received from the DUT.

    Parameters
    ----------
    port_id : str
        ID string for the port on which a connection should be
        established.
    baud : int
        Port baud rate.
    id_tag : str
        Connection ID string to use when logging.
    logger_name : str
        Name used to reference the HCI logger.
    retries : int
        Number of times a port read should be retried before
        an error is thrown.
    timeout : float
        Port timeout.
    async_callback : Callable[[AsyncPacket], Any], optional
        Function pointer defining the process that should be taken
        when an async packet is received. If not defined, the async
        packet will be thrown out.
    evt_callback : Callable[[EventPacket], Any], optional
        Function pointer defining the process that should be taken
        when an unexpected event packet is received. If not defined,
        the event packet will be thrown out.

    Attributes
    ----------
    port_id : str
        ID string for the port on which a connection has been
        established.
    port : serial.Serial
        Port baud rate.
    id_tag : str
        Connection ID string used by the logger.
    logger : logging.Logger
        HCI logging object referenced by the `logger_name` argument.
    retries : int
        Number of times a port read should be retried before an error
        is thrown.
    timeout : float
        Port timeout.
    async_callback : Callable[[AsyncPacket], Any], optional
        Function pointer defining the process that should be taken
        when an async packet is received.
    evt_callback : Callable[[AsyncPacket], Any], optional
        Function pointer defining the process that should be taken
        when an unexpected event packet is received.

    """

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
        timeout: float = 1.0,
        async_callback: Optional[Callable[[AsyncPacket], Any]] = None,
        evt_callback: Optional[Callable[[EventPacket], Any]] = None,
        exclusive_port: bool = True,
    ):
        self.port_id = port_id
        self.port = None
        self.id_tag = id_tag
        self.logger = get_formatted_logger(name=logger_name)
        self.retries = retries
        self.timeout = timeout
        self.async_callback = async_callback
        self.evt_callback = evt_callback

        self._event_packets = []
        self._read_thread = None
        self._kill_evt = None
        self._data_lock = None
        self._port_lock = None

        self._init_port(port_id, baud, exclusive_port)
        self._init_read_thread()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with self._port_lock:
            self.stop()
            self.port.close()

    def __del__(self):
        if self._read_thread and self._read_thread.is_alive():
            self.stop()
        if self.port and self.port.isOpen():
            self.port.close()

    def start(self):
        """Start the port read thread.

        Starts the thread that is used to read from the serial
        port and store the received events.

        """
        self._read_thread.start()

    def stop(self):
        """Stop the port read thread.

        Safely stops the execution of the thread used to
        read from the serial port.

        """
        self._kill_evt.set()
        self._read_thread.join()

    def close(self):
        """Close the serial connection.

        Safely stops the execution of any active threads and
        closes the serial connection.

        """
        if self._read_thread.is_alive():
            self.stop()

        if self.port.is_open:
            self.port.flush()
            self.port.close()

    def send_command(
        self, pkt: CommandPacket, timeout: Optional[float] = None
    ) -> EventPacket:
        """Send a command over the serial connection.

        Sends the given command to the DUT over the serial
        connection and retrieves the response.

        Parameters
        ----------
        pkt : CommandPacket
            Command that should be transported.
        timeout : Optional[float], optional
            Timeout for response retrieval. Can be used
            to temporarily override this object's `timeout`
            attribute.

        Returns
        -------
        EventPacket
            The retrieved packet.

        """

        return self._write(pkt.to_bytes(), timeout)

    def send_command_raw(
        self,
        raw_command: bytearray,
        timeout: Optional[float] = None,
    ) -> EventPacket:
        """Write a raw HCI command to device

        Parameters
        ----------
        raw_command : bytearray
            Command as a byte array

        timeout : Optional[float], optional
            Timeout for response retrieval. Can be used
            to temporarily override this object's `timeout`
            attribute.

        Returns
        -------
        EventPacket
        """
        return self._write(raw_command, timeout)

    def retrieve_packet(self, timeout: Optional[float] = None) -> EventPacket:
        """Retrieve a packet from the serial line.

        Retrieves a single packet from the front of the
        serial port queue.

        Parameters
        ----------
        timeout : Optional[float], optional
            Timeout for read operation. Can be used to
            temporarily override this object's `timeout`
            attribute.

        Returns
        -------
        EventPacket
            The retrieved packet.

        """
        return self._retrieve(timeout)

    def _init_read_thread(self) -> None:
        """Initializes the port read thread and data locks.

        PRIVATE

        """
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

    def _init_port(self, port_id: str, baud: int, exclusive: bool) -> None:
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
                exclusive=exclusive,
            )

        except serial.SerialException as err:
            self.logger.error("%s: %s", type(err).__name__, err)
            sys.exit(1)

        except OverflowError as err:
            self.logger.error("Baud rate exception, %i is too large", baud)
            self.logger.error("%s: %s", type(err).__name__, err)
            sys.exit(1)

    def _read(self, kill_evt: Event) -> None:
        """Process executed by the port read thread.

        PRIVATE

        """
        while not kill_evt.is_set():
            # pylint: disable=consider-using-with
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
                    if pkt_type[0] == PacketType.ASYNC.value and self.async_callback:
                        self.async_callback(AsyncPacket.from_bytes(read_data))
                    else:
                        pkt = EventPacket.from_bytes(read_data)
                        if pkt.evt_code == EventCode.COMMAND_COMPLETE:
                            self._event_packets.append(pkt)
                        elif self.evt_callback:
                            self.evt_callback(pkt)

    def _retrieve(
        self,
        timeout: Optional[float],
    ) -> EventPacket:
        """Reads an event from serial port.

        PRIVATE

        """
        if timeout is None:
            timeout = self.timeout

        timeout_process = Process(target=time.sleep, args=(timeout,))
        timeout_process.start()

        while self._read_thread.is_alive():
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
        """Sends a command to the test board and retrieves the response.

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
