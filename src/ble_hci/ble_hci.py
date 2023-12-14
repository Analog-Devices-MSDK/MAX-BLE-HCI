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
"""Module contains a host-controller interface for ADI BLE-compatible chips.

Module defines a host-controller interface for BLE operation on any Analog
Devices BLE compatible microchip. The HCI class provides basic testing
functionality, and is designed to be used with the `BLE5_ctrl` example
housed in the Analog Devices MSDK.

"""
import datetime
import logging
import sys
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
from threading import Thread, Lock, Event
from multiprocessing import Process
import serial

from ._hci_logger import get_formatted_logger

# pylint: disable=unused-import
from .hci_packets import (
    AsyncPacket,
    CommandPacket,
    EventPacket,
    ExtendedPacket,
    Endian,
    _byte_length,
)
from .packet_codes import EventCode, StatusCode
from .packet_defs import ADI_PORT_BAUD_RATE, OCF, OGF, PacketType, PubKeyValidateMode

_MAX_U16 = 2**16 - 1
_MAX_U32 = 2**32 - 1
_MAX_U64 = 2**64 - 1

TEST_VAL = 0


class PhyOption(Enum):
    """PHY Options"""

    P1M = 1
    P2M = 2
    PCODED = 3


def _to_le_nbyte_list(value: int, n_bytes: int):
    little_endian = []
    for i in range(n_bytes):
        num_masked = (value & (0xFF << 8 * i)) >> (8 * i)
        little_endian.append(num_masked)
    return little_endian

def _le_list_to_int(nums: List[int]) -> int:
    full_num = 0
    for i, num in enumerate(nums):
        full_num |= num << 8 * i
    return full_num

def to_little_endian(value) -> int:
    """Convert an int to a to little endian format
    Parameters
    ----------
    vale: int
        value to convert to little endian
    Returns
    -------
    int
       value as little endian
    """

    big_endian_bytes = value.to_bytes((value.bit_length() + 7) // 8, byteorder="big")

    little_endian_bytes = big_endian_bytes[::-1]

    return int.from_bytes(little_endian_bytes, byteorder="big")


class BleHci:
    """Host-controller interface for ADI BLE-compatible microchips.

    The BleHci object defines a host-controller interface for
    BLE operations on any Analog Devices BLE-compatible microchip.
    Controller provides implementations for both connection mode
    and DTM testing. It is designed to be used in conjunction with
    the embedded firmware found in the `BLE5_ctr` example in the
    Analog Devices MSDK.

    Parameters
    ----------
    port_id : str
        Serial port ID string.
    id_tag : str
        String identification for class instance.
    log_level : str
        HCI logging level.

    Attributes
    ----------
        port : serial.Serial
            Test board serial port connection.
        id_tag : str
            Identification for class instance.
        opcodes : Dict[str, int]
            Command name to opcode map.

    """

    PHY_1M = 1
    PHY_2M = 2
    PHY_S8 = 3
    PHY_S2 = 4

    def __init__(
        self,
        port_id: str,
        mon_port_id: Optional[str] = None,
        baud=ADI_PORT_BAUD_RATE,
        id_tag: str = "DUT",
        log_level: Union[str, int] = "INFO",
        logger_name: str = "BLE-HCI",
        retries: int = 0,
        timeout: float = 1.0
    ) -> None:
        self.port = None
        self.mon_port = None
        self.id_tag = id_tag
        self.logger = get_formatted_logger(log_level=log_level, name=logger_name)
        self.retries = retries
        self.timeout = timeout

        self._event_packets = []
        self._async_packets = []
        self._read_thread = None
        self._kill_evt = None
        self._lock = None

        self.set_log_level(log_level)
        self._init_ports(port_id=port_id, mon_port_id=mon_port_id, baud=baud)
        self._init_read_thread()

    def __del__(self):
        print('DELETE')
        self._kill_evt.set()
        self._read_thread.join()
    
    def get_log_level(self) -> str:
        level = self.logger.level
        if level == logging.DEBUG:
            return "DEBUG"
        if level == logging.INFO:
            return "INFO"
        if level == logging.WARNING:
            return "WARNING"
        if level == logging.ERROR:
            return "ERROR"
        if level == logging.CRITICAL:
            return "CRITICAL"
        return "NOTSET"

    def set_log_level(self, level: Union[str, int]) -> None:
        """Sets log level.

        Provides intermediary control over the logging level
        of the host-controller interface module logger. If
        necessary, desired log level is automatically converted
        from a string to an integer. As such, both strings and
        integers are valid inputs to the `level` parameter.

        Parameters
        ----------
        level : Union[int, str]
            Desired log level.

        """
        if isinstance(level, int):
            self.logger.setLevel(level)
            return

        ll_str = level.upper()
        if ll_str == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif ll_str == "INFO":
            self.logger.setLevel(logging.INFO)
        elif ll_str == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif ll_str == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif ll_str == "CRITICAL":
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.NOTSET)
            self.logger.warning(
                f"Invalid log level string: {ll_str}, level set to 'logging.NOTSET'"
            )

    def set_address(self, addr: int) -> StatusCode:
        """Sets the BD address.

        Function sets the chip BD address. Address can be given
        as either a bytearray or as a list of integer values.

        Parameters
        ----------
        addr : Union[List[int], bytearray]
            Desired BD address.

        Returns
        -------
        EventPacket
            Object containing board return data.

        """
        addr = _to_le_nbyte_list(addr, 6)
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_BD_ADDR, params=addr
        )
        evt = self._send_command(cmd)

        return evt.status

    def start_advertising(
        self,
        interval: int = 0x60,
        connect: bool = True,
        listen: Union[bool, int] = False,
    ) -> StatusCode:
        # TODO: more options?
        """Command board to start advertising.

        Sends a command to the board, telling it to start advertising
        with the given interval. Advertising type can be either
        scannable/connectable or non-connectable in accordance with
        the `connect` argument. HCI can be directed to listen for
        events for either a finite number or seconds or indefinitely
        in accordance with the `listen` argument. Indefinite listening
        can only be ended with `CTRL-C`. A test end function must be
        called to end this process on the board.

        Parameters
        ----------
        interval : int
            The advertising interval.
        connect : bool
            Use scannable/connectable advertising type?
        listen : Union[bool, int]
            Listen (indefinitely or finite) for incoming events?

        Returns
        -------
        EventPacket
            Object containing board return data.

        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.RESET_CONN_STATS)
        self._send_command(cmd)

        params = [
            0x0,  # All PHYs Preference
            0x7,  # TX PHYs Preference
            0x7,  # RX PHYs Preference
        ]
        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_DEF_PHY, params=params)
        self._send_command(cmd)

        params = [
            interval,  # Advertising Interval Min.
            interval,  # Advertising Interval Max.
            0x3,  # Advertisiing Type
            0x0,  # Own Address Type
            0x0,  # Peer Address Type
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,  # Peer Address
            0x7,  # Advertising Channel Map
            0x0,  # Advertising Filter Policy
        ]

        if connect:
            params[2] = 0x0  # If connecting, change Advertising Type

        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_ADV_PARAM, params=params)
        self._send_command(cmd)

        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_ADV_ENABLE, params=0x1)
        evt = self._send_command(cmd)

        if not listen:
            return evt.status

        if isinstance(listen, int):
            self._wait(seconds=listen)
            return evt.status

        while True:
            self._wait(seconds=10)
            self.get_conn_stats()

    def enable_scanning(self, enable: bool, filter_duplicates: bool = False) -> StatusCode:
        """Command board to start scanning for connections.

        Sends a command to the board, telling it to start scanning with
        the given interval for potential connections. Function then
        listens for events indefinitely. The listening can only be
        stopped with `CTRL-C`. A test end function must be called to end
        this process on the board.

        Parameters
        ----------
        interval : int
            The scan interval.

        """
        params = [
            int(enable),  # LE Scan Enable
            int(filter_duplicates)  # Filter Duplicates
        ]

        cmd = CommandPacket(
            OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_SCAN_ENABLE, params=params
        )
        evt = self._send_command(cmd)
        
        return evt.status

    def set_scan_params(
        self,
        scan_type: int = 0x1,
        scan_interval: int = 0x100,
        scan_window: int = 0x100,
        addr_type: int = 0x0,
        filter_policy: int = 0x0
    ) -> StatusCode:
        params = [scan_type]
        params.extend(_to_le_nbyte_list(scan_interval, 2))
        params.extend(_to_le_nbyte_list(scan_window, 2))
        params.append(addr_type)
        params.append(filter_policy)

        cmd = CommandPacket(
            OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_SCAN_PARAM, params=params
        )
        evt = self._send_command(cmd)        

        return evt.status

    def init_connection(
        self,
        addr: Union[List[int], bytearray],
        interval: int = 0x6,
        sup_timeout: int = 0x64,
        listen: Union[bool, int] = False,
    ) -> StatusCode:
        """Command board to initialize a connection.

        Sends a sequence of commands to the board, telling it to
        initialize a connection in accordance with the given address,
        interval, and timeout. The `address` argument must be a
        string representing six bytes of hex values, with each byte
        seperated by a ':'. HCI can be directed to listen for events
        for either a finite number or seconds or indefinitely in
        accordance with the `listen` argument. Indefinite listening
        can only be ended with `CTRL-C`. The `disconnect()` function
        must be called to end the connection if it is successfully made.

        Parameters
        ----------
        addr : str
            BD address to use for connection initialization. String
            containing six bytes of hex data, with each byte separated
            by a ':'.
        interval : int
            Connection interval.
        timeout : int
            Connection initialization timeout.
        listen : Union[bool, int]
            Listen (finite or indefinite) for further events?

        Returns
        -------
        EventPacket
            Object containing board return data.

        """
        if isinstance(addr, list):
            try:
                addr = bytearray(addr)
            except ValueError as err:
                self.logger.error("%s: %s", type(err).__name__, err)
                sys.exit(1)
            except TypeError as err:
                self.logger.error("%s: %s", type(err).__name__, err)
                sys, exit(1)

        # self.set_event_mask(0xFFFFFFFFFFFFFFFF, mask_pg2=0xFFFFFFFFFFFFFFFF)
        # self.set_event_mask(0xFFFFFFFFFFFFFFFF)
        # self.set_event_mask_le(0xFFFFFFFFFFFFFFFF)

        self.reset_connection_stats()
        self.set_default_phy()
        status = self.create_connection(
            addr, conn_interval_min=interval, conn_interval_max=interval, sup_timeout=sup_timeout
        )

        if not listen:
            return status

        if isinstance(listen, int):
            self._wait(seconds=listen)
            return status

        while True:
            self._wait(seconds=10)
            self.get_conn_stats()

    def reset_connection_stats(self) -> StatusCode:
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.RESET_CONN_STATS)
        evt = self._send_command(cmd)

        return evt.status

    def create_connection(
        self,
        peer_addr: int,
        scan_interval: int = 0xA000,
        scan_window: int = 0xA000,
        init_filter_policy: int = 0x0,
        peer_addr_type: int = 0x0,
        own_addr_type: int = 0x0,
        conn_interval_min: int = 0x6,
        conn_interval_max: int = 0x6,
        max_latency: int = 0x0000,
        sup_timeout: int = 0x64,
        min_ce_length: int = 0x0F10,
        max_ce_length: int = 0x0F10
    ) -> StatusCode:
        params = _to_le_nbyte_list(scan_interval, 2)
        params.extend(_to_le_nbyte_list(scan_window, 2))
        params.append(init_filter_policy)
        params.append(peer_addr_type)
        params.extend(_to_le_nbyte_list(peer_addr, 6))
        params.append(own_addr_type)
        params.extend(_to_le_nbyte_list(conn_interval_min, 2))
        params.extend(_to_le_nbyte_list(conn_interval_max, 2))
        params.extend(_to_le_nbyte_list(max_latency, 2))
        params.extend(_to_le_nbyte_list(sup_timeout, 2))
        params.extend(_to_le_nbyte_list(min_ce_length, 2))
        params.extend(_to_le_nbyte_list(max_ce_length, 2))

        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.CREATE_CONN, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def set_default_phy(
        self,
        all_phys: int = 0x0,
        tx_phys: int = 0x7,
        rx_phys: int = 0x7
    ) -> StatusCode:
        params = [
            all_phys,
            tx_phys,
            rx_phys
        ]

        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_DEF_PHY, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def set_data_len(
        self,
        handle: int = 0x0000,
        tx_octets: int = 0xFB00,
        tx_time: int = 0x9042
    ) -> StatusCode:
        """Command board to set data length to the max value.

        Sends a command to the board, telling it to set its internal
        data length parameter to the maximum value.

        Returns
        -------
        Event
            Object containing board return data.

        """
        params = _to_le_nbyte_list(handle, 2)
        params.extend(_to_le_nbyte_list(tx_octets, 2))
        params.extend(_to_le_nbyte_list(tx_time, 2))

        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_DATA_LEN, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def enable_autogenerate_acl(self, enable) -> StatusCode:
        # TODO: implement/check params @eric
        """Enable automatic generation of ACL packets.

        Parameters
        ----------
        enable: bool
            Enable automatic ACL packet generation?

        Returns
        -------
        Event
            Object containing board return data.

        """
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GENERATE_ACL, params=int(enable)
        )
        evt = self._send_command(cmd)
        return evt.status

    def generate_acl(
        self, handle: int, packet_len: int, num_packets: int
    ) -> StatusCode:
        # TODO: implement
        """Command board to generate ACL data.

        Sends a command to the board telling it to generate/send ACL data
        in accordance with the provided packet length and number
        of packets. A test end function must be called to end this
        process on the board.

        Parameters
        ----------
        handle : int
            Connection handle.
        packet_len : int
            Desired packet length.
        num_packets : int
            Desired number of packets to send.

        Returns
        -------
        EventCode
            Process status code.

        Raises
        ------
        ValueError
            If the handle is greater than 65535.
        ValueError
            If packet length greater than 65535.
        ValueError
            If number of packets greater than 255.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle too large! {handle}")

        if packet_len > 0xFFFF:
            raise ValueError(
                f"Invalid packet length {packet_len}. Must be less than 65536."
            )

        if num_packets > 0xFF:
            raise ValueError(
                f"Invalid number of packets: {num_packets}. Must be less than 256."
            )

        params = [handle, packet_len, num_packets]
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GENERATE_ACL, 5, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def enable_acl_sink(self, enable: bool) -> StatusCode:
        # TODO: implement
        """Command board to sink ACL data.

        Sends a command to the board, telling it to sink
        incoming ACL data.

        Parameters
        ----------
        enable : bool
            Enable ACL sink?

        Returns
        -------
        Event
            Object containing board return data.

        """
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.ENA_ACL_SINK, 1, params=int(enable)
        )
        evt = self._send_command(cmd)
        return evt.status

    def set_phy(self, phy: int = 1, handle: int = 0x0000) -> StatusCode:
        """Set the PHY.

        Sends a command to the board, telling it to set the
        PHY to the given selection. PHY must be one of the
        values 1, 2, 3 or 4. Alternatively, PHY selection
        values are declared in `utils/constants.py` as
        ADI_PHY_1M (1), ADI_PHY_2M (2), ADI_PHY_S8 (3), and
        ADI_PHY_S2 (4).

        Parameters
        ----------
        phy_sel : int
            Desired PHY.
        timeout : int
            Process timeout.

        Returns
        -------
        Event
            Object containing board return data.

        """
        params = _to_le_nbyte_list(handle, 2)
        params.append(0x0)
        if phy == self.PHY_1M:
            params.append(0x0)
            params.append(0x0)
            params.extend(_to_le_nbyte_list(0x0, 2))
        elif phy == self.PHY_2M:
            params.append(0x2)
            params.append(0x2)
            params.extend(_to_le_nbyte_list(0x0, 2))
        elif phy == self.PHY_S8:
            params.append(0x4)
            params.append(0x4)
            params.extend(_to_le_nbyte_list(0x2, 2))
        elif phy == self.PHY_S2:
            params.append(0x4)
            params.append(0x4)
            params.extend(_to_le_nbyte_list(0x1, 2))
        else:
            self.logger.warning("Invalid PHY selection = %i, using 1M.", phy)

        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_PHY, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def listen(self, time: int = 0) -> float:
        """Listen for events and monitor connection stats.

        Listens for events and monitors connection stats for
        the specified amount of time. To listen indefinitely,
        set `time` argument to 0. Indefinite listening can only
        be ended with `CTRL-C`.

        Parameters
        ----------
        time : int
            The amount of time to listen/monitor for. Set to `0`
            for indefinitely.

        Returns
        -------
        float
            The current connection PER as a percent.

        """
        per = 100.0
        start_time = datetime.datetime.now()
        while True:
            if time == 0:
                self._wait(10)
            else:
                self._wait(time)

            cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_CONN_STATS, 0)
            evt = self._send_command(cmd)

            per = self._parse_conn_stats_evt(evt)
            time_now = datetime.datetime.now()

            if time != 0 and (time_now - start_time).total_seconds() > time:
                return per

    def tx_test(
        self, channel: int = 0, phy: int = 1, payload: int = 0, packet_len: int = 0
    ) -> StatusCode:
        """Command board to being transmitting.

        Sends a command to the board, telling it to begin transmitting
        packets of the given packet length, with the given payload, on
        the given channel, using the given PHY. The payload must be one
        of the values 0, 1, 2, 3, 4, 5, 6, or 7. Alternatively, payload
        selection values are declared in `utils/constants.py` as
        ADI_PAYLOAD_PRBS9 (0), ADI_PAYLOAD_11110000 (1), ADI_PAYLOAD_10101010 (2),
        ADI_PAYLOAD_PRBS15 (3), ADI_PAYLOAD_11111111 (4) ADI_PAYLOAD_00000000 (5),
        ADI_PAYLOAD_00001111 (6) and ADI_PAYLOAD_01010101 (7). The PHY must
        be one of the values 1, 2, 3 or 4. Alternatively, PHY selection
        values are declared in `utils/constants.py` as ADI_PHY_1M (1),
        ADI_PHY_2M (2), ADI_PHY_S8 (3), and ADI_PHY_S2 (4). A test end
        function must be called in order to end this process on the board.

        Parameters
        ----------
        channel : int
            The channel to transmit on.
        phy : int
            The PHY to use.
        payload : int
            The payload type to use.
        packet_len : int
            The TX packet length.

        Returns
        -------
        Event
            Object containing board return data.

        """
        params = [channel, packet_len, payload, phy]
        cmd = CommandPacket(
            OGF.LE_CONTROLLER,
            OCF.LE_CONTROLLER.ENHANCED_TRANSMITTER_TEST,
            params=params,
        )
        evt = self._send_command(cmd)

        return evt.status

    def tx_test_vs(
        self,
        channel: int = 0,
        phy: int = 1,
        payload: int = 0,
        packet_len: int = 0,
        num_packets: int = 0,
    ) -> StatusCode:
        """Command board to being transmitting (vendor-specific).

        Sends a command to the board, telling it to begin transmitting
        the given number of packets of the given length, with the given payload,
        on the given channel, using the given PHY. The payload must be one
        of the values 0, 1, 2, 3, 4, 5, 6, or 7. Alternatively, payload
        selection values are declared in `utils/constants.py` as
        ADI_PAYLOAD_PRBS9 (0), ADI_PAYLOAD_11110000 (1), ADI_PAYLOAD_10101010 (2),
        ADI_PAYLOAD_PRBS15 (3), ADI_PAYLOAD_11111111 (4) ADI_PAYLOAD_00000000 (5),
        ADI_PAYLOAD_00001111 (6) and ADI_PAYLOAD_01010101 (7). The PHY must
        be one of the values 1, 2, 3 or 4. Alternatively, PHY selection
        values are declared in `utils/constants.py` as ADI_PHY_1M (1),
        ADI_PHY_2M (2), ADI_PHY_S8 (3), and ADI_PHY_S2 (4). A test end
        function must be called in order to end this process on the board.

        Parameters
        ----------
        channel : int
            The channel to transmit on.
        phy : int
            The PHY to use.
        payload : int
            The payload type to use.
        packet_len : int
            The TX packet length.
        num_packets : int
            The number of packets to transmit.

        Returns
        -------
        Event
            Object containing board return data.

        """
        params = [channel, packet_len, payload, phy]
        params.extend(_to_le_nbyte_list(num_packets, 2))

        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.TX_TEST, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def rx_test(
        self, channel: int = 0, phy: int = 1, modulation_idx: float = 0
    ) -> StatusCode:
        """Command board to begin receiving.

        Sends a command to the board, telling it to begin receiving
        on the given channel using the given PHY. The PHY must
        be one of the values 1, 2, 3 or 4. Alternatively, PHY selection
        values are declared in `utils/constants.py` as ADI_PHY_1M (1),
        ADI_PHY_2M (2), ADI_PHY_S8 (3), and ADI_PHY_S2 (4). A test end
        function must be called in order to end this process on the board.

        Parameters
        ----------
        channel : int
            The channel to receive on.
        phy : int
            The PHY to use.

        Returns
        -------
        Event
            Object containing board return data.

        """
        if phy == self.PHY_S2:
            phy = self.PHY_S8

        params = [channel, phy, modulation_idx]
        cmd = CommandPacket(
            OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.ENHANCED_RECEIVER_TEST, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def rx_test_vs(
        self,
        channel: int = 0,
        phy: int = 1,
        num_packets: int = 0,
        modulation_idx: float = 0,
    ) -> StatusCode:
        """Command board to begin receiving (vendor-specific).

        Sends a command to the board, telling it to begin receiving
        the given number of packets on the given channel using the given
        PHY. The PHY must be one of the values 1, 2, 3 or 4. Alternatively,
        PHY selection values are declared in `utils/constants.py` as
        ADI_PHY_1M (1), ADI_PHY_2M (2), ADI_PHY_S8 (3), and ADI_PHY_S2 (4).
        A test end function must be called in order to end this process on
        the board.

        Parameters
        ----------
        channel : int
            The channel to receive on.
        phy : int
            The PHY to use.
        num_packets : int
            The number of packets to expect to receive.

        Returns
        -------
        Event
            Object containing board return data.

        """
        if phy == self.PHY_S2:
            phy = self.PHY_S8

        params = [channel, phy, modulation_idx]
        params.extend(_to_le_nbyte_list(num_packets, 2))

        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.RX_TEST, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def end_test(self) -> Tuple[StatusCode, int]:
        """Command board to end the current test.

        Sends a command to the board, telling it to end whatever test
        it is currently running. Function then parses the test stats
        and returns the number of properly received packets.

        Returns
        -------
        Union[int, None]
            The amount of properly received packets, or `None` if
            the return data from the board is empty. In this case
            it is likely that a test error occured.

        """
        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.TEST_END)
        evt = self._send_command(cmd)

        rx_ok = evt.get_return_params()
        return rx_ok

    def reset_test_stats(self) -> StatusCode:
        """Command board to end the current test (vendor-specific).

        Sends a command to the board, telling it to end whatever test
        it is currently running. Function then parses and returns the
        test statistics, which inclue the number of packets properly
        received, the number of crc errors, the number of RX timeout
        occurances, and the number of TX packets sent.

        Returns
        -------
        Union[Dict[str, int], None]
            The test statistics, or `None` if the return data from
            the board is empty. In this case, it is likely that a
            test error occured.

        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.RESET_TEST_STATS)
        evt = self._send_command(cmd)

        return evt.status

    def set_adv_tx_power(self, tx_power: int) -> StatusCode:
        """Set the advertising TX power.

        Sends a command to the board, telling
        it to set the advertising TX power to the given value.

        Parameters
        ----------
        power : int
            The desired TX power value in dBm.

        Returns
        -------
        EventPacket
            Object containing board return data from setting the
            advertising power.

        Raises
        ------
        ValueError
            If desired TX power is not between -127dBm and 127dBm

        """
        if not (-127 < tx_power < 127):
            raise ValueError("TX power must be between -127 and 127.")

        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_ADV_TX_PWR, params=tx_power)
        evt = self._send_command(cmd)
        return evt.status

    def set_conn_tx_power(self, tx_power: int, handle: int = 0x0000) -> StatusCode:
        """Set the connection TX power.

        Sends a command to the board, telling
        it to set the connection TX power to the given value.

        Parameters
        ----------
        power : int
            The desired TX power value.
        handle : int
            Connection handle.

        Returns
        -------
        EventPacket
            Object containing board return data from setting the
            connection power.

        Raises
        ------
        ValueError
            If desired TX power is not between -127dBm and 127dBm

        """
        if not (-127 < tx_power < 127):
            raise ValueError("TX power must be between -127 and 127.")

        params = _to_le_nbyte_list(handle, 2)
        params.append(tx_power)
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_CONN_TX_PWR, params=params)
        evt = self._send_command(cmd)
        return evt.status

    def disconnect(self, handle: int = 0x0000, reason: int = 0x16) -> StatusCode:
        """Command board to disconnect from an initialized connection.

        Sends a command to the board, telling it to break a currently
        initialized connection. Board gives Local Host Termination (0x16)
        as the reason for the disconnection. Function is used to exit
        Connection Mode Testing.

        Returns
        -------
        Event
            Object containing board return data.

        """
        params = _to_le_nbyte_list(handle, 2)
        params.append(reason)
        
        cmd = CommandPacket(
            OGF.LINK_CONTROL, OCF.LINK_CONTROL.DISCONNECT, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_channel_map(
        self,
        channels: Optional[Union[List[int], int]] = None,
        handle: int = 0x0000,
    ) -> StatusCode:
        """Set the channel map.

        Creates a channel map/mask based on the given arguments
        and sends a command to the board, telling it to set its
        internal channel map to the new one.

        Parameters
        ----------
        channel : int, optional
            Channel to mask out.
        mask : int, optional
            Channel mask to use.
        handle : int
            Connection handle.

        Returns
        -------
        Event
            Object containing board return data.

        """
        if channels is None:  # Use all channels
            channel_mask = _MAX_U32
        elif channels == 0:  # Use channels 0 and 1
            channel_mask = 0x0000000003
        else:  # Mask the given channel(s)
            if not isinstance(channels, list):
                channels = [channels]

            channel_mask = 0x0000000001
            for chan in channels:
                channel_mask = channel_mask | (1 << chan)

        channel_mask = channel_mask & ~(0xE000000000)

        params = _to_le_nbyte_list(handle, 2)
        params.extend(_to_le_nbyte_list(channel_mask, 5))

        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_CHAN_MAP, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def read_register(
        self, addr: int, length: int
    ) -> Tuple[StatusCode, List[int]]:
        """Read data from a specific register.

        Sends a command to the board, telling it to read data
        or a given length from a given register address. Address
        must begin with '0x' and must be a string representing
        four bytes of hex data. Function both prints and returns
        the read data.

        Parameters
        ----------
        addr : str
            The register address to read from. Must being with '0x'
            and contain four bytes of hex data.
        length : int
            The desired length of the register read in bytes.

        Returns
        -------
        List[int]
            The data as read from the register.

        """
        self.logger.info("Reading %i bytes from address %08X", length, addr)

        params = [length]
        params.extend(_to_le_nbyte_list(addr, 4))
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.REG_READ, params=params)
        evt = self._send_command(cmd)

        param_len = [4] * int(length / 4)
        if not (length % 4) == 0:
            param_len.append(length % 4)
        read_data = evt.get_return_params(param_lens=param_len)
        curr_addr = addr

        for idx, data in enumerate(read_data):
            if param_len[idx] == 1:
                self.logger.info("0x%08X: 0x______%02X", curr_addr, data)
            elif param_len[idx] == 2:
                self.logger.info("0x%08X: 0x____%04X", curr_addr, data)
            elif param_len[idx] == 3:
                self.logger.info("0x%08X: 0x__%06X", curr_addr, data)
            else:
                self.logger.info("0x%08X: 0x%08X", curr_addr, data)

            curr_addr += 4

        return evt. status, evt.get_return_params(param_lens=param_len, endianness=Endian.BIG)

    def read_event(self, timeout: Optional[float] = None) -> EventPacket:
        timeout_err = None
        tries = self.retries
        if not timeout:
            timeout = self.timeout
        while tries >= 0:
            try:
                return self._retrieve_event(timeout=self.timeout)
            except TimeoutError as err:
                tries -= 1
                timeout_err = err
                self.logger.warning(
                    f"Timeout occured. Retrying. {self.retries - tries} retries remaining."
                )

        raise TimeoutError("Timeout occured. No retries remaining.") from timeout_err

    def write_command(
        self,
        command: CommandPacket,
        listen: Union[bool, int] = False,
        timeout: Optional[float] = None,
    ) -> EventPacket:
        """Send a custom command to the board.

        Sends a custom HCI command to the board. Safeguarding is
        not implemented, and therefore it is best to ensure desired
        command is supported prior to sending, and no error will
        be thrown for unsupported commands. The `command` argument will
        accept either a string or an integer value, however, string values
        must be in hex format, and integers must have originated from hex
        numbers. HCI can be directed to listen for events for either a finite
        number or seconds or indefinitely in accordance with the `listen`
        argument. Indefinite listening can only be ended with `CTRL-C`.

        Parameters
        ----------
        command : Union[str, int]
            The command to give the board. Can be a string or an integer.
            String input must be formatted as hex values.
        listen : Union[bool, int]
            Listen (finite or indefinite) for further events?
        timeout : int
            Command timeout. Set to None for indefinite.

        Returns
        -------
        Event
            Object containing board return data.

        """
        if not timeout:
            timeout = self.timeout
        evt = self._send_command(command, timeout=timeout)

        if not listen:
            return evt

        if isinstance(listen, int):
            self._wait(seconds=listen)
        else:
            while True:
                self._wait(seconds=10)

        return evt

    def write_command_raw(
        self,
        data: bytearray,
        listen: Union[bool, int] = False,
        timeout: Optional[float] = None,
    ) -> StatusCode:
        """Send a custom bytearray command to the board.

        Sends a custom HCI command to the board as a bytearray. Safeguarding
        is not implemented, and therefore it is best to ensure desired
        command is supported prior to sending, and no error will
        be thrown for unsupported commands. The `command` argument will
        accept either a string or an integer value, however, string values
        must be in hex format, and integers must have originated from hex
        numbers. HCI can be directed to listen for events for either a finite
        number or seconds or indefinitely in accordance with the `listen`
        argument. Indefinite listening can only be ended with `CTRL-C`.

        Parameters
        ----------
        command : Union[str, int]
            The command to give the board. Can be a string or an integer.
            String input must be formatted as hex values.
        listen : Union[bool, int]
            Listen (finite or indefinite) for further events?
        timeout : int
            Command timeout. Set to None for indefinite.

        Returns
        -------
        Event
            Object containing board return data.

        """
        if not timeout:
            timeout = self.timeout
        evt = self._send_command(data, timeout=timeout)

        if not listen:
            return evt

        if isinstance(listen, int):
            self._wait(seconds=listen)
        else:
            while True:
                self._wait(seconds=10)

        return evt.status

    def reset(self) -> StatusCode:
        """Sets log level.
        Resets the controller

        Returns
        ----------
        Event: EventPacket

        """
        cmd = CommandPacket(OGF.CONTROLLER, OCF.CONTROLLER.RESET)
        evt = self._send_command(cmd)

        return evt.status

    def set_scan_channel_map(self, channel_map: int) -> StatusCode:
        """Set the channel map used for scanning

        Parameters
        ----------
        channel_map : int
            channel map used for scanning

        Returns
        -------
        EventCode

        """
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_SCAN_CH_MAP, params=channel_map
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_event_mask(
        self, mask: int, mask_pg2: Optional[int] = None
    ) -> Union[StatusCode, Tuple[StatusCode, StatusCode]]:
        """Set event mask(s).

        Sets the event masks using the Controller command group
        Set Event Mask command. If a page 2 mask is provided,
        then the Set Event Mask Page 2 command is also called.

        Parameters
        ----------
        mask : int
            event mask

        Returns
        -------
        EventCode
            The status of the event mask set operation.
        Tuple[EventCode, EventCode]
            The statuses of the both the event mask set and the
            event mask page 2 set operation.

        """
        mask = _to_le_nbyte_list(mask, 8)

        cmd = CommandPacket(
            OGF.CONTROLLER, OCF.CONTROLLER.SET_EVENT_MASK, params=mask
        )
        evt = self._send_command(cmd)
        status = evt.status

        if mask_pg2:
            mask_pg2 = _to_le_nbyte_list(mask_pg2, 8)
            cmd = CommandPacket(
                OGF.CONTROLLER, OCF.CONTROLLER.SET_EVENT_MASK_PAGE2, params=mask_pg2
            )
            evt = self._send_command(cmd)

            return status, evt.status

        return status

    def set_event_mask_le(self, mask: int) -> StatusCode:
        """LE controller set event mask

        Parameters
        ----------
        mask : int
            event mask
        enable : _type_
            whether the events should be enabled or disabled

        Returns
        -------
        EventCode

        """
        mask = _to_le_nbyte_list(mask, 8)

        cmd = CommandPacket(OGF.LE_CONTROLLER, OCF.LE_CONTROLLER.SET_EVENT_MASK, params=mask)
        return self._send_command(cmd).status

    def set_event_mask_vs(self, mask: int, enable: bool) -> StatusCode:
        """Vendor specific set event mask

        Parameters
        ----------
        mask : int
            event mask
        enable : _type_
            whether the events should be enabled or disabled

        Returns
        -------
        EventCode

        """
        params = _to_le_nbyte_list(mask, 8)
        params.append(int(enable))

        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_EVENT_MASK, params=params)
        evt = self._send_command(cmd)

        return evt.status

    def set_tx_test_err_pattern(self, pattern: int) -> StatusCode:
        """Set the TX test error pattern

        Parameters
        ----------
        pattern : int
            32-bit error pattern

        Returns
        -------
        StatusCode

        Raises
        ------
        ValueError
            If pattern > 32-bit
        """

        if pattern > _MAX_U32:
            raise ValueError("Pattern expected to be 32-bit number!")

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_TX_TEST_ERR_PATT, params=[pattern]
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_connection_op_flags(
        self, handle: int, flags: int, enable: bool
    ) -> StatusCode:
        """Set connection operation flags

        Parameters
        ----------
        handle : int
            Handle to connection
        flags : int
            flags to enable or disable
        enable : bool
            True to enable, False to disable

        Returns
        -------
        EventCode

        """
        params = [handle & 0xFF, (handle >> 8) & 0xFF]
        flags = _to_le_nbyte_list(flags, 4)
        params.extend(flags)
        params.append(int(enable))

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_CONN_OP_FLAGS, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_256_priv_key(self, key: List[int]) -> StatusCode:
        """Set the 256 Byte private key used

        Parameters
        ----------
        key : list[int]
            private key

        Returns
        -------
        EventCode


        Raises
        ------
        ValueError
            If key is not 256 bytes long
        """
        if len(bytearray(key)) != 32:
            raise ValueError("Must had an array of 32 bytes")

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_P256_PRIV_KEY, params=key
        )
        evt = self._send_command(cmd)

        return evt.status

    def get_channel_map_periodic_scan_adv(
        self, handle: int, is_advertising: bool
    ) -> Tuple[int, StatusCode]:
        """Get the channel map used for periodic scanning

        Parameters
        ----------
        handle : int
            handle to connection
        is_advertising : bool
            True if advertiser, False if Scanner

        Returns
        -------
        EventPacket

        """

        params = [handle & 0xFF, (handle >> 8) & 0xFF]
        params.append(int(is_advertising))

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_PER_CHAN_MAP, params=params
        )

        evt = self._send_command(cmd)
        channel_map = evt.get_return_params()

        return channel_map, evt.status

    def get_acl_test_report(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get ACL Test Report

        Returns
        -------
        Dict[str, int]
            ACL Test Report
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_ACL_TEST_REPORT)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(param_lens=[4, 4, 4, 4])

        stats = {
            "rx-acl-pkt-cnt": vals[0],
            "rx-acl-oct-cnt": vals[1],
            "gen-acl-pkt-cnt": vals[2],
            "gen-acl-oct-cnt": vals[3],
        }

        return stats, evt.status

    def set_local_num_min_used_channels(
        self, phy: PhyOption, power_thresh: int, min_used: int
    ) -> StatusCode:
        """Set local number of minimum used channels

        Parameters
        ----------
        phy : PhyOption
            Which PHY to set min num channels
        power_thresh : int
            Power threshold for min num channels
        min_used : int
            min num channels

        Returns
        -------
        EventCode


        Raises
        ------
        ValueError
            min num channels must be between 1-37
        ValueError
            power threshold must be between +/-127
        """
        if min_used < 1 or min_used > 37:
            raise ValueError("min_used must be between 1-37")
        if power_thresh < -127 or power_thresh > 127:
            raise ValueError("power_thresh must be between -127 and 127")

        params = [phy.value, power_thresh, min_used]
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_LOCAL_MIN_USED_CHAN, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def get_peer_min_num_channels_used(
        self, handle: int
    ) -> Tuple[Dict[PhyOption, int], StatusCode]:
        """Get minimum number of channels used by peer

        Parameters
        ----------
        handle : int
            handle to connection to peer

        Returns
        -------
        Dict[PhyOption, int]
            min num used channel map
        """
        params = _to_le_nbyte_list(handle, 2)
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_PEER_MIN_USED_CHAN, params=params
        )
        evt = self._send_command(cmd)

        vals = evt.get_return_params(param_lens=[1, 1, 1])

        min_used_map = {
            PhyOption.P1M: vals[0],
            PhyOption.P2M: vals[1],
            PhyOption.PCODED: vals[2],
        }

        return min_used_map, evt.status

    def set_validate_pub_key_mode(self, mode: PubKeyValidateMode) -> StatusCode:
        """Set validate public key mode

        Parameters
        ----------
        mode : PubKeyValidateMode
            Mode to use for validation

        Returns
        -------
        EventCode

        """
        cmd = CommandPacket(
            ogf=OGF.VENDOR_SPEC,
            ocf=OCF.VENDOR_SPEC.VALIDATE_PUB_KEY_MODE,
            params=[mode.value],
        )

        evt = self._send_command(cmd)
        return evt.status

    def get_rand_address(self) -> Tuple[List[int], StatusCode]:
        """Gets a randomly generated address

        Returns
        -------
        List[int]
            6 Byte address
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_RAND_ADDR)
        evt = self._send_command(cmd)

        addr = _to_le_nbyte_list(evt.get_return_params(), 6)
        return addr, evt.status

    def set_local_feature(self, features: int) -> StatusCode:
        """Set local features

        Parameters
        ----------
        features : int
            64-Bit Mask of features

        Returns
        -------
        StatusCode


        Raises
        ------
        ValueError
            If features > 2^64
        """
        if features > 2**64:
            raise ValueError("Feature mask is a 64-Bit number!")

        features = _to_le_nbyte_list(features, 8)

        cmd = CommandPacket(
            ogf=OGF.VENDOR_SPEC, ocf=OCF.VENDOR_SPEC.SET_LOCAL_FEAT, params=features
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_operational_flags(self, flags: int, enable: bool) -> StatusCode:
        """Set operational flags

        Parameters
        ----------
        flags : int
            32-Bit mask of flags
        enable : bool
            True to enable, False to disable

        Returns
        -------
        StatusCode


        Raises
        ------
        ValueError
            If flags is greater than 32-Bit
        """

        if flags > _MAX_U32:
            raise ValueError("Flags must be a 32-bit number")

        flags = _to_le_nbyte_list(flags, 4)

        params = []
        params.extend(flags)
        params.append(int(enable))

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_OP_FLAGS, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def get_pdu_filter_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get PDU Filter Stats

        Returns
        -------
        Dict[str, int]
            Filter stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_PDU_FILT_STATS)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(
            param_lens=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        )

        stats = {
            "fail-pdu": vals[0],
            "pass-pdu": vals[1],
            "fail-whitelist": vals[2],
            "pass_whitellist": vals[3],
            "fail-peer-addr-match": vals[4],
            "pass-peer-addr-match": vals[5],
            "fail-local-addr-match": vals[6],
            "pass-local-addr-match": vals[7],
            "fail-peer-rpa-verify": vals[8],
            "pass-peer-rpa-verify": vals[9],
            "fail-peer-priv-addr": vals[10],
            "pass-peer-priv-addr": vals[11],
            "fail-local-priv-addr": vals[12],
            "pass-local-priv-addr": vals[13],
            "fail-peer-addr-res-req": vals[14],
            "pass-peer-addr-res-req": vals[15],
            "pass-local-addr-res-opt": vals[16],
            "peer-res-addr-pend": vals[17],
            "local-res-addr-pend": vals[18],
        }

        return stats, evt.status

    def set_encryption_mode(
        self, handle: int, enable: bool, noonce_mode: bool
    ) -> StatusCode:
        """Set encryption mode

        Parameters
        ----------
        handle : int
            handle to connection
        enable : bool
            True to enable, False to disable
        noonce_mode : bool
            True for Noonce mode, False otherwise

        Returns
        -------
        EventCode

        """
        params = _to_le_nbyte_list(handle, 2)
        params.append(int(enable))
        params.append(int(noonce_mode))

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_ENC_MODE, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_diagnostic_mode(self, enable: bool) -> StatusCode:
        """Set diagnostic mode

        Parameters
        ----------
        enable : bool
            True to enable, False to disable

        Returns
        -------
        EventCode

        """
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_DIAG_MODE, params=int(enable)
        )
        evt = self._send_command(cmd)

        return evt.status

    def enable_sniffer_packet_forwarding(self, enable: bool) -> StatusCode:
        """Enable packet sniffer forwarding

        Parameters
        ----------
        enable : bool
            True to enable, False to disable

        Returns
        -------
        EventCode

        """
        out_method = 0  # HCI Through Tokens (Only option available)
        cmd = CommandPacket(
            OGF.VENDOR_SPEC,
            OCF.VENDOR_SPEC.SET_SNIFFER_ENABLE,
            params=[out_method, int(enable)],
        )
        evt = self._send_command(cmd)

        return evt.status

    def get_memory_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get memory use stats

        Returns
        -------
        Dict[str, int]
            Memory use stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_SYS_STATS)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(
            param_lens=[2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        )

        stats = {
            "stack": vals[0],
            "sys-assert-cnt": vals[1],
            "free-mem": vals[2],
            "used-mem": vals[3],
            "max-connections": vals[4],
            "conn-ctx-size": vals[5],
            "cs-watermark-lvl": vals[6],
            "ll-watermark-lvl": vals[7],
            "sch-watermark-lvl": vals[8],
            "lhci-watermark-lvl": vals[9],
            "max-adv-sets": vals[10],
            "adv-set-ctx-size": vals[11],
            "ext-scan-max": vals[12],
            "ext-scan-ctx-size": vals[13],
            "max-num-ext-init": vals[14],
            "exit-init-ctx-size": vals[15],
            "max-per-scanners": vals[16],
            "per-scan-ctz-size": vals[17],
            "max-cig": vals[18],
            "cig-ctx-size": vals[19],
            "cis-ctx-size": vals[20],
        }
        return stats, evt.status

    def get_adv_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get advertising stats

        Returns
        -------
        Dict[str, int]
            Advertising stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_ADV_STATS)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(param_lens=[4, 4, 4, 2, 4, 4, 2, 2, 2, 2])

        stats = {
            "tx-adv": vals[0],
            "rx-req": vals[1],
            "rx-req-crc": vals[2],
            "rx-req-timeout": vals[3],
            "tx-resp": vals[4],
            "err-adv": vals[5],
            "rx-setup": vals[6],
            "tx-setup": vals[7],
            "rx-isr": vals[8],
            "tx-isr": vals[9],
        }
        return stats, evt.status

    def get_scan_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get scanning stats

        Returns
        -------
        Dict[str, int]
            Scanning stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_SCAN_STATS)
        evt = self.write_command(cmd)

        vals = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = {
            "rx-adv": vals[0],
            "rx-adv-crc": vals[1],
            "rx-adv-timeout": vals[2],
            "tx-req": vals[3],
            "rx-rsp": vals[4],
            "rx-rsp-crc": vals[5],
            "rx-rsp-timeout": vals[6],
            "err-scan": vals[7],
            "rx-setup": vals[8],
            "tx-setup": vals[9],
            "rx-isr": vals[10],
            "tx-isr": vals[11],
        }

        return stats, evt.status

    def get_conn_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Gets and parses connection stats.

        Sends a command to the board, telling it to return
        a connection statistics packet. Function then attempts
        to parse the packet and calculate the current connection
        PER%. Function will attempt this process for the given
        number of retries.

        Parameters
        ----------
        retries : int
            Amount of times to attempt to collect and parse the
            connection statistics.

        Returns
        -------
        Dict[str, int]
            The current connection statistics.

        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_CONN_STATS)
        evt = self._send_command(cmd)
        report = evt.get_return_params([4, 4, 4, 4, 4, 2, 2, 2, 2])
        stats = {
            "rx-data": report[0],
            "rx-data-crc": report[1],
            "tx-data": report[2],
            "err-data": report[3],
            "rx-setup": report[4],
            "tx-setup": report[5],
            "rx-isr": report[6],
            "tx-isr": report[7],
        }

        return stats, evt.status

    def get_test_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get test stats

        Returns
        -------
        Dict[str, int]
            Test stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_TEST_STATS)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = {
            "rx-data": vals[0],
            "rx-data-crc": vals[1],
            "rx-data-timeout": vals[2],
            "tx-data": vals[3],
            "err-data": vals[4],
            "rx-setup": vals[5],
            "tx-setup": vals[6],
            "rx-isr": vals[7],
            "tx-isr": vals[8],
        }
        return stats, evt.status

    def get_pool_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get memory pool stats

        Returns
        -------
        Dict[str, int]
            memory pool stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_POOL_STATS)
        evt = self._send_command(cmd)

        # TODO: Whaaaaat?

        num_pool = evt.raw_return[0]
        pool_stats = {"num-pool": num_pool}

        data = evt.raw_return[1:]

        for i in range(num_pool):
            key = f"pool{i}"
            pool_stats[key] = {
                "buf-size": _le_list_to_int(data[0 * i : 2 * i]),
                "num-buf": data[2 * i],
                "num-alloc": data[3 * i],
                "max-alloc": data[4 * i],
                "max-req-len": data[5 * i : 7 * i :],
            }

        return pool_stats, evt.status

    def set_additional_aux_ptr_offset(self, delay: int, handle: int) -> StatusCode:
        """Set auxillary pointer delay

        Parameters
        ----------
        delay : int
            delay in microseconds. (0 to disable)
        handle : int
            handle to connection

        Returns
        -------
        EventCode

        """
        params = _to_le_nbyte_list(delay, 4)
        params.append(handle)

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_AUX_DELAY, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_ext_adv_data_fragmentation(
        self, handle: int, frag_length: int
    ) -> StatusCode:
        """Set extended advertising fragmentation length

        Parameters
        ----------
        handle : int
            advertising handle
        frag_length : int
            fragmentation length

        Returnss
        -------
        EventCode

        """
        params = _to_le_nbyte_list(handle, 2)
        params.append(frag_length)

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_EXT_ADV_FRAG_LEN, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_extended_advertising_phy_opts(
        self, handle: int, primary: int, secondary: int
    ) -> StatusCode:
        """Set phy options used for extended advertsing

        Parameters
        ----------
        handle : int
            handle to connection
        primary : int
            primary options
        secondary : int
            secondary options

        Returns
        -------
        EventCode

        """
        params = _to_le_nbyte_list(handle, 2)
        params.append(primary)
        params.append(secondary)

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_EXT_ADV_PHY_OPTS, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def set_extended_advertising_default_phy_opts(
        self, handle: int, primary: int, secondary: int
    ) -> StatusCode:
        """Set default phy options used for extended advertsing

        Parameters
        ----------
        handle : int
            handle to connection
        primary : int
            primary options
        secondary : int
            secondary options

        Returns
        -------
        EventCode

        """
        params = _to_le_nbyte_list(handle, 2)
        params.append(primary)
        params.append(secondary)

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_EXT_ADV_DEF_PHY_OPTS, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def generate_iso_packets(
        self, handle: int, packet_length: int, num_packets: int
    ) -> StatusCode:
        """Generate ISO packets

        Parameters
        ----------
        handle : int
            handle to connection
        packet_length : int
            length of iso packet
        num_packets : int
            number of iso packets per event

        Returns
        -------
        EventCode

        """
        params = _to_le_nbyte_list(handle, 2)
        params.extend(_to_le_nbyte_list(packet_length, 2))
        params.append(num_packets)

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GENERATE_ISO, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def get_iso_test_report(self) -> Tuple[Dict[str, int], StatusCode]:
        # TODO
        """Get ISO test report

        Returns
        -------
        Dict[str, int]
            ISO test report
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_ISO_TEST_REPORT)
        evt = self._send_command(cmd)

        if evt.status == StatusCode.LL_SUCCESS:
            vals = evt.get_return_params(param_lens=[4, 4, 4, 4])

            stats = {
                "rx-iso-pkt-cnt": vals[0],
                "rx-iso-oct-cnt": vals[1],
                "gen-pkt-cnt": vals[2],
                "gen-oct-cnt": vals[3],
            }
        else:
            stats = None

        return stats, evt.status

    def enable_iso_packet_sink(self, enable: bool) -> StatusCode:
        """Enable ISO packet sink

        Parameters
        ----------
        enable : bool
            True to enable, False to disable

        Returns
        -------
        EventCode

        """
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.ENA_ISO_SINK, params=int(enable)
        )
        evt = self._send_command(cmd)

        return evt.status

    def enable_autogen_iso_packets(self, packet_length: int) -> StatusCode:
        """Enable autogeneration of of ISO packets

        Parameters
        ----------
        packet_length : int
            Length of packet (0 to disable)

        Returns
        -------
        EventCode


        Raises
        ------
        ValueError
            If value is more than 4 bytes
        """
        if packet_length > _MAX_U32:
            raise ValueError(
                f"Invalid packet length {packet_length}. Must be maximum 4 bytes in size."
            )

        packet_length = _to_le_nbyte_list(packet_length, 4)
        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.ENA_AUTO_GEN_ISO, params=packet_length
        )

        evt = self._send_command(cmd)
        return evt.status

    def get_iso_connection_stats(self) -> Dict[str, int]:
        """Get ISO connection stats

        Returns
        -------
        Dict[str, int]
            ISO connection stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_ISO_TEST_REPORT)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = {
            "rx-data": vals[0],
            "rx-data-crc": vals[1],
            "rx-data-timeout": vals[2],
            "tx-data": vals[3],
            "err-data": vals[4],
            "rx-setup": vals[5],
            "tx-setup": vals[6],
            "rx-isr": vals[7],
            "tx-isr": vals[8],
        }

        return stats

    def get_aux_adv_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get auxillary advertising stats

        Returns
        -------
        Dict[str, int]
            AUX adv stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_AUX_ADV_STATS)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(param_lens=[4, 4, 4, 2, 4, 4, 4, 2, 2, 2, 2])

        stats = {
            "tx-adv": vals[0],
            "rx-req": vals[1],
            "rx-req-crc": vals[2],
            "rx-req-timeout": vals[3],
            "tx-resp": vals[4],
            "tx-chain": vals[5],
            "err-adv": vals[6],
            "rx-setup": vals[7],
            "tx-setup": vals[8],
            "rx-isr": vals[9],
            "tx-isr": vals[10],
        }

        return stats, evt.status

    def get_aux_scan_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get auxillary scanning stats

        Returns
        -------
        Dict[str, int]
            Aux scan stats
        """
        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_AUX_SCAN_STATS)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(
            param_lens=[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2]
        )

        stats = {
            "rx-adv": vals[0],
            "rx-adv-crc": vals[1],
            "rx-adv-timeout": vals[2],
            "tx-req": vals[3],
            "rx-rsp": vals[4],
            "rx-rsp-crc": vals[5],
            "rx-rsp-timeout": vals[6],
            "rx-chain": vals[7],
            "rx-chain-crc": vals[8],
            "rx-chain-timeout": vals[9],
            "err-scan": vals[10],
            "rx-setup": vals[11],
            "tx-setup": vals[12],
            "rx-isr": vals[13],
            "tx-isr": vals[14],
        }
        return stats, evt.status

    def get_periodic_scanning_stats(self) -> Tuple[Dict[str, int], StatusCode]:
        """Get periodic scanning stats

        Returns
        -------
        Dict[str, int]
            Periodic scanning stats
        """

        cmd = CommandPacket(OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.GET_PER_SCAN_STATS)
        evt = self._send_command(cmd)

        vals = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = {
            "rx-adv": vals[0],
            "rx-adv-crc": vals[1],
            "rx-adv-timeout": vals[2],
            "rx-chain": vals[3],
            "rx-chain-crc": vals[4],
            "rx-chain-timeout": vals[5],
            "err-scan": vals[6],
            "rx-setup": vals[7],
            "tx-setup": vals[8],
            "rx-isr": vals[9],
            "tx-isr": vals[10],
        }
        return stats, evt.status

    def set_connection_phy_tx_power(
        self, handle: int, power: int, phy: PhyOption
    ) -> StatusCode:
        """Set TX Power for connection on given PHY

        Parameters
        ----------
        handle : int
            handle to connection
        power : int
            _description_
        phy : PhyOption
            PHY to apply power to

        Returns
        -------
        EventCode

        """
        params = _to_le_nbyte_list(handle, 2)
        params.append(power)
        params.append(phy.value)

        cmd = CommandPacket(
            OGF.VENDOR_SPEC, OCF.VENDOR_SPEC.SET_CONN_PHY_TX_PWR, params=params
        )
        evt = self._send_command(cmd)

        return evt.status

    def get_rssi_vs(self, channel: int = 0):
        if channel > 39:
            raise ValueError("Channel must be between 0-39")

        cmd = CommandPacket(
            ogf=OGF.VENDOR_SPEC, ocf=OCF.VENDOR_SPEC.GET_RSSI, params=[channel]
        )
        evt = self._send_command(cmd)
        rssi = evt.get_return_params()

        # RSSI is 8 bit signed
        SIGN_BIT = 1 << 13
        if rssi & SIGN_BIT:
            rssi &= ~SIGN_BIT
            rssi *= -1

        return rssi, evt.status

    def exit(self) -> None:
        """Close the HCI connection.

        Used to safely close the connection between the HCI and
        the test board.

        """
        if self.port.is_open:
            self.port.flush()
            self.port.close()

    def _init_ports(
        self,
        port_id: Optional[str] = None,
        mon_port_id: Optional[str] = None,
        baud: int = ADI_PORT_BAUD_RATE,
    ) -> None:
        """Initializes serial ports.

        PRIVATE

        """
        if self.port is not None:
            if self.port.is_open:
                self.port.flush()
                self.port.close()

        if self.mon_port is not None:
            if self.mon_port.is_open and mon_port_id:
                self.mon_port.flush()
                self.mon_port.close()

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
            if mon_port_id:
                self.mon_port = serial.Serial(
                    port=mon_port_id,
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

    def _init_read_thread(self):
        print("INIT THREAD")
        self._kill_evt = Event()
        self._read_thread = Thread(target=self._read_process, args=(self._kill_evt,), daemon=True)
        self._lock = Lock()

        self._read_thread.start()

    def _parse_conn_stats_evt(self, evt: EventPacket) -> float:
        """Parse connection statistics packet.

        PRIVATE

        """
        try:
            stats = evt.return_vals
            rx_data_ok = stats[0:4]
            rx_data_crc = stats[4:8]
            rx_data_to = stats[8:12]
            tx_data = stats[12:16]
            err_trans = stats[16:20]
        except ValueError as err:
            self.logger.error("%s: %s", type(err).__name__, err)
            return None

        self.logger.info("%s<", self.id_tag)
        self.logger.info("rxDataOK   : %i", rx_data_ok)
        self.logger.info("rxDataCRC  : %i", rx_data_crc)
        self.logger.info("rxDataTO   : %i", rx_data_to)
        self.logger.info("txData     : %i", tx_data)
        self.logger.info("errTrans   : %i", err_trans)

        per = 100.0
        if rx_data_crc + rx_data_to + rx_data_ok != 0:
            per = round(
                float(
                    (rx_data_crc + rx_data_to) / (rx_data_crc + rx_data_to + rx_data_ok)
                )
                * 100,
                2,
            )
            self.logger.info("PER         : %i%%", per)

        return per
           
    def _read_process(self, kill_evt: Event):
        while True:
            if kill_evt.is_set():
                break
            if self.port.in_waiting:
                pkt_type = self.port.read(1)
                if pkt_type[0] == PacketType.ASYNC.value:
                    self._get_async_packet()
                else:
                    self._get_event_packet()

    def _retrieve_event(
        self, timeout: Optional[float] = None
    ) -> Union[EventPacket, AsyncPacket]:
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

        while True:
            if len(self._event_packets):
                timeout_process.terminate()
                timeout_process.join()
                timeout_process.close()
                break
            if timeout_process.exitcode is None:
                continue
            raise TimeoutError(
                "Timeout occured before DUT could respond. Check connection and retry."
            )
        
        self._lock.acquire()
        evt = self._event_packets.pop(0)
        self._lock.release()

        return evt

    def _get_event_packet(self) -> EventPacket:
        read_data = self.port.read(2)
        param_len = read_data[1]

        read_data += self.port.read(param_len)
        self.logger.info(
            "%s  %s<%02X%s",
            datetime.datetime.now(),
            self.id_tag,
            PacketType.EVENT.value,
            read_data.hex(),
        )

        self._lock.acquire()
        self._event_packets.append(EventPacket.from_bytes(read_data))
        self._lock.release()

    def _get_async_packet(self):
        read_data = self.port.read(4)
        data_len = read_data[2] | (read_data[3] << 8)

        read_data += self.port.read(data_len)
        self.logger.info(
            "%s  %s<%02X%s",
            datetime.datetime.now(),
            self.id_tag,
            PacketType.ASYNC.value,
            read_data.hex()
        )
        
        self._lock.acquire()
        self._async_packets.append(AsyncPacket.from_bytes(read_data))
        self._lock.release()

    def _wait(self, seconds: int = 2) -> None:
        """Wait for events from the test board for a few seconds.

        PRIVATE

        """
        start_time = datetime.datetime.now()
        delta = datetime.datetime.now() - start_time

        while True:
            if seconds != 0:
                if delta.seconds > seconds:
                    break

            self._retrieve_event(timeout=0.1)
            delta = datetime.datetime.now() - start_time
            if (delta.seconds > 30) and (delta.seconds % 30 == 0):
                self.logger.info("%s |", datetime.datetime.now())

    def _send_command(
        self, pkt: CommandPacket, timeout: Optional[float] = None
    ) -> EventPacket:
        """Sends a command to the test board and retrieves the response.

        PRIVATE

        """
        return self._send_command_raw(pkt.to_bytes(), timeout=timeout)

    def _send_command_raw(
        self, pkt: bytearray, timeout: Optional[float] = None
    ) -> EventPacket:
        """Sends a data stream to the test board and retrieves the response.

        PRIVATE

        """
        tries = self.retries
        self.logger.info("%s  %s>%s", datetime.datetime.now(), self.id_tag, pkt.hex())
        timeout_err = None

        
        self.port.flush()
        self.port.write(pkt)
        while tries >= 0:
            try:
                return self._retrieve_event(timeout=timeout)
            except TimeoutError as err:
                tries -= 1
                timeout_err = err
                self.logger.warning(
                    f"Timeout occured. Retrying. {tries+1} retries remaining."
                )

        raise TimeoutError("Timeout occured. No retries remaining.") from timeout_err
