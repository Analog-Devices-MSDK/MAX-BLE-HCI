# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module defines an HCI serial port sniffer object.

This module contains the definition of the `HciSerialSniffer` class,
which can be used to sniff and decode HCI packets off a serial
connection. Due to the single-access nature of serial communication,
the `HciSerialSniffer` object requires that a proxy port be used by
the primary communicators. The `HciSerialSniffer` object will create
this proxy and will handle data fowarding across it.

Usage
-----
Example: Sniffing HCI communication on a serial line

.. code-block:: python

    from hci_decode_tools import HciSerialSniffer, HciSerialSnifferPortCfg
    # example port config: 921600 8N1, RTS/CTS enabled
    port_cfg = HciSerialSnifferPortCfg(
        baudrate=921600,
        bytesize=8,
        parity="N",
        stopbits=1,
        rtscts=True
    )
    # example sniffing mode: controller->host only
    mode = HciSerialSniffer.SniffMode.CTRL2HOST_ONLY
    # example serial port: /dev/ttyUSB0
    sniffer = HciSerialSniffer("/dev/ttyUSB0", sniff_mode=mode, port_config=port_cfg)
    print(f"Proxy Port: {sniffer.get_proxy()}")
    try:
        sniffer.start()
        sniffer.join()
    except KeyboardInterrupt:
        sniffer.close()

"""
from dataclasses import dataclass
from enum import Enum
import os
import queue
import select
import serial
import threading
from typing import Optional

from .packets.acl_packet import AclPacket
from .packets.command_packet import CommandPacket
from .packets.event_packet import EventPacket
from .decode import decode_packet

@dataclass
class HciSerialSnifferPortCfg:
    """Serial port configuration container.

    Parameters
    ----------
    baudrate : int
        Serial port baud rate.
    bytesize : int
        Serial port byte size.
    parity : str
        Serial port parity.
    stopbits : float
        Serial port stop bits.
    timeout : float, optional
        Serial port read timeout.
    xonxoff : bool
        Serial port software flow control enable/disable.
    rtscts : bool
        Serial port RTS/CTS hardware flow control enable/diable.
    dsrdtr : bool
        Serial port DSR/DTR hardware flow control enable/diable.
    write_timeout : float, optional
        Serial port write timeout.
    inter_byte_timeout : float, optional
        Serial port inter byte timeout.
    exclusive : bool, optional
        Serial port exclusive access enable/disable.

    Attributes
    ----------
    baudrate : int
        Baud rate.
    bytesize : int
        Byte size.
    parity : str
        Parity.
    stopbits : float
        Stop bits.
    timeout : float, optional
        Read timeout.
    xonxoff : bool
        Software flow control enable/disable.
    rtscts : bool
        RTS/CTS hardware flow control enable/diable.
    dsrdtr : bool
        DSR/DTR hardware flow control enable/diable.
    write_timeout : float, optional
        Write timeout.
    inter_byte_timeout : float, optional
        Inter byte timeout.
    exclusive : bool, optional
        Exclusive access enable/disable.

    """
    baudrate: int = 115200
    bytesize: int = serial.EIGHTBITS
    parity: str = serial.PARITY_SPACE
    stopbits: float = serial.STOPBITS_ONE
    timeout: Optional[float] = None
    xonxoff: bool = False
    rtscts: bool = False
    dsrdtr: bool = False
    write_timeout: Optional[float] = None
    inter_byte_timeout: Optional[float] = None
    exclusive: Optional[bool] = False

class HciSerialSniffer(threading.Thread):
    """HCI serial port sniffer.

    Object sniffs/decodes HCI packets from a serial
    connection. As serial ports are single-access,
    a proxy must be used to establish the serial
    connection to the HCI device. This proxy can
    be obtained via the `get_proxy` function.

    Parameters
    ----------
    port_id : str
        Serial port ID string.
    sniff_mode
        Sniffing mode.
    port_config
        Serial port configuration.
    output_file : str, optional
        Output data path, or `None` if decoded packets
        should be printed to the console.

    Attributes
    ----------
    mode : HciSerialSniffer.SniffMode
        Sniffing mode.
    cfg : HciSerialSnifferPortCfg
        Serial port configuration.
    port : serial.Serial
        Serial port interfacing object.
    proxy : str
        Proxy serial port ID string.
    output_file : str, optional
        Output data path. If `None`, print
        to console.

    """
    class SniffMode(Enum):
        """Sniffer mode selection."""
        BIDIRECTIONAL = 0x00
        CTRL2HOST_ONLY = 0x01
        HOST2CTRL_ONLY = 0x02

    class SniffData:
        """Sniffed data container.

        Parameters
        ----------
        data : bytes
            Sniffed data.
        is_from_dev : bool
            Direction indicator.

        Attributes
        ----------
        data : bytes
            Sniffed data.
        is_from_dev : bool
            Direction indicator.

        """
        def __init__(self, data: bytes, is_from_dev: bool) -> None:
            self.data = data
            self.is_from_dev = is_from_dev

        def get_direction(self) -> str:
            """Get data direction string.

            Returns
            -------
            str
                Data direction string.

            """
            return "[Controller-->Host]" if self.is_from_dev else "[Host-->Controller]"

        def get_data(self) -> bytes:
            """Get sniffed data.

            Returns
            -------
            bytes
                Sniffed data bytes.

            """
            return self.data

    def __init__(
        self,
        port_id: str,
        sniff_mode: SniffMode = SniffMode.BIDIRECTIONAL,
        port_config: Optional[HciSerialSnifferPortCfg] = None,
        output_file: Optional[str] = None
    ) -> None:
        if port_config is None:
            port_config = HciSerialSnifferPortCfg()
        pty_mst, pty_slv = os.openpty()
        proxy_str = os.ttyname(pty_slv)
        port = serial.Serial(
            port=port_id,
            baudrate=port_config.baudrate,
            bytesize=port_config.bytesize,
            parity=port_config.parity,
            stopbits=port_config.stopbits,
            timeout=port_config.timeout,
            xonxoff=port_config.xonxoff,
            rtscts=port_config.rtscts,
            dsrdtr=port_config.dsrdtr,
            write_timeout=port_config.write_timeout,
            inter_byte_timeout=port_config.inter_byte_timeout,
            exclusive=port_config.exclusive
        )

        self.mode: self.SniffMode = sniff_mode
        self.cfg: HciSerialSnifferPortCfg = port_config
        self.port: serial.Serial = port
        self.proxy: str = proxy_str
        self.output_file: str = output_file
        self._pty_mst: int = pty_mst
        self._pty_slv: int = pty_slv
        self._data: queue.Queue = queue.Queue()
        self._host2ctrl_thread: threading.Thread = None
        self._ctrl2host_thread: threading.Thread = None
        self._decoder_thread: threading.Thread = None
        self._kill_evt: threading.Event = None

        if self.output_file is not None:
            with open(self.output_file, "w", encoding="utf-8") as stream_out:
                stream_out.write("HCI Sniffer Logs\n================\n")

        self._init_threads()

    def start(self) -> None:
        """
        Start sniffing.
        """
        self._host2ctrl_thread.start()
        self._ctrl2host_thread.start()
        self._decoder_thread.start()

    def join(self) -> None:
        """
        Join the sniffing threads.
        """
        self._host2ctrl_thread.join()
        self._ctrl2host_thread.join()
        self._decoder_thread.join()

    def stop(self) -> None:
        """
        Stop sniffing.
        """
        self._kill_evt.set()
        self.join()

    def close(self) -> None:
        """
        Stop sniffing and safely close connections..
        """
        self.stop()
        self.port.close()
        os.close(self._pty_slv)
        os.close(self._pty_mst)

    def get_proxy(self) -> str:
        """Get the proxy port ID.

        Returns
        -------
        str
            Proxy port ID string.

        """
        return self.proxy

    def _init_threads(self) -> None:
        """
        Initialize sniffing threads.
        """
        self._kill_evt = threading.Event()
        self._host2ctrl_thread = threading.Thread(
            target=self._monitor_host2ctrl,
            args=(self._kill_evt,),
            daemon=True,
            name="Host2Controller"
        )
        self._ctrl2host_thread = threading.Thread(
            target=self._monitor_ctrl2host,
            args=(self._kill_evt,),
            daemon=True,
            name="Controller2Host"
        )
        self._decoder_thread = threading.Thread(
            target=self._decode_packets,
            args=(self._kill_evt,),
            daemon=True,
            name="Decoder"
        )

    def _monitor_host2ctrl(self, kill_evt: threading.Event) -> None:
        """Monitor the host-to-controller data path.

        Parameters
        ----------
        kill_evt : threading.Event
            When set, indicates the thread bound to this
            function should abort.

        """
        poller = select.poll()
        poller.register(self._pty_mst)
        while not kill_evt.is_set():
            for _, evtype in poller.poll(1000):
                if evtype & select.POLLIN:
                    pkt = os.read(self._pty_mst, 1)
                    pkt_code = int.from_bytes(pkt[0:], byteorder="little")
                    pkt_length = 0
                    if pkt_code == AclPacket.PACKET_ID:
                        pkt += os.read(self._pty_mst, 4)
                        pkt_length = int.from_bytes(pkt[3:], byteorder="little")
                    elif pkt_code == CommandPacket.PACKET_ID:
                        pkt += os.read(self._pty_mst, 3)
                        pkt_length = int.from_bytes(pkt[3:], byteorder="little")
                    elif pkt_code == EventPacket.PACKET_ID:
                        pkt += os.read(self._pty_mst, 2)
                        pkt_length = int.from_bytes(pkt[2:], byteorder="little")
                    else:
                        print(f"--Invalid Packet ID: {pkt[0]}--")
                        continue
                    pkt += os.read(self._pty_mst, pkt_length)
                    self._data.put(self.SniffData(pkt, False))
                    self.port.write(pkt)

    def _monitor_ctrl2host(self, kill_evt: threading.Event) -> None:
        """Monitor the controller-to-host data path.

        Parameters
        ----------
        kill_evt : threading.Event
            When set, indicates the thread bound to this
            function should abort.

        """
        poller = select.poll()
        poller.register(self._pty_mst)
        while not kill_evt.is_set():
            for _, evtype in poller.poll(1000):
                if evtype & select.POLLOUT:
                    while self.port.in_waiting > 0:
                        pkt = self.port.read(1)
                        pkt_code = int.from_bytes(pkt[0:], byteorder="little")
                        pkt_length = 0
                        if pkt_code == AclPacket.PACKET_ID:
                            pkt += self.port.read(4)
                            pkt_length = int.from_bytes(pkt[3:], byteorder="little")
                        elif pkt_code == CommandPacket.PACKET_ID:
                            pkt += self.port.read(3)
                            pkt_length = int.from_bytes(pkt[3:], byteorder="little")
                        elif pkt_code == EventPacket.PACKET_ID:
                            pkt += self.port.read(2)
                            pkt_length = int.from_bytes(pkt[2:], byteorder="little")
                        else:
                            print(f"--Invalid Packet ID: {pkt[0]}--")
                            continue
                        pkt += self.port.read(pkt_length)
                        self._data.put(self.SniffData(pkt, True))
                        os.write(self._pty_mst, pkt)

    def _decode_packets(self, kill_evt: threading.Event) -> None:
        """Decode and output sniffed packets.

        Parameters
        ----------
        kill_evt : threading.Event
            When set, indicates the thread bound to this
            function should abort.

        """
        while not kill_evt.is_set():
            try:
                pkt = self._data.get(timeout=0.1)
                if self.output_file is not None:
                    with open(self.output_file, "a", encoding="utf-8") as stream_out:
                        stream_out.write(f"{pkt.get_direction()}\n")
                        stream_out.write(f"{decode_packet(pkt.get_data())}\n")
                else:
                    print(pkt.get_direction())
                    print(decode_packet(pkt.get_data()))
            except queue.Empty:
                continue

