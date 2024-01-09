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
# pylint: disable=too-many-arguments
import logging
from typing import Any, Callable, Optional, Union

from ._ble_standard_cmds import BleStandardCmds
from ._hci_logger import get_formatted_logger
from ._transport import SerialUartTransport
from ._vendor_spec_cmds import VendorSpecificCmds
from .data_params import AdvParams, ConnParams
from .hci_packets import AsyncPacket, CommandPacket, EventPacket
from .packet_codes import StatusCode
from .packet_defs import ADI_PORT_BAUD_RATE


class BleHci(BleStandardCmds, VendorSpecificCmds):
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
        baud: int = ADI_PORT_BAUD_RATE,
        id_tag: str = "DUT",
        log_level: Union[str, int] = "INFO",
        logger_name: str = "BLE-HCI",
        retries: int = 0,
        timeout: float = 1.0,
        async_callback: Optional[Callable[[AsyncPacket], Any]] = None,
        evt_callback: Optional[Callable[[EventPacket], Any]] = None,
    ) -> None:
        self.port_id = port_id
        self.port = None
        self.mon_port = None
        self.id_tag = id_tag
        self.logger = get_formatted_logger(log_level=log_level, name=logger_name)
        self.retries = retries
        self.timeout = timeout

        self._init_ports(port_id, baud, logger_name, async_callback, evt_callback)
        super().__init__(self.port, logger_name)

    def get_log_level(self) -> str:
        """DOCSTRING"""
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
                "Invalid log level string: %s, level set to 'logging.NOTSET'", ll_str
            )

    def start_advertising(
        self,
        connect: bool = True,
    ) -> StatusCode:
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

        self.reset_connection_stats()
        self.set_default_phy(all_phys=0, tx_phys=7, rx_phys=7)

        adv_type = 0 if connect else 3
        adv_params = AdvParams(adv_type=adv_type)
        self.set_adv_params(adv_params)

        status = self.enable_adv(True)

        return status

    def init_connection(
        self,
        addr: int,
        interval: int = 0x6,
        sup_timeout: int = 0x64,
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

        if addr > 2**48 - 1:
            raise ValueError("Addr must be able to be represented in 6 Bytes")

        self.reset_connection_stats()
        self.set_default_phy()

        conn_params = ConnParams(
            addr,
            conn_interval_max=interval,
            conn_interval_min=interval,
            sup_timeout=sup_timeout,
        )
        status = self.create_connection(conn_params)

        return status

    def read_event(self, timeout: Optional[float] = None) -> EventPacket:
        """Read sync event from controller

        Parameters
        ----------
        timeout : Optional[float], optional
            time before aborting operation, by default None

        Returns
        -------
        EventPacket

        Raises
        ------
        TimeoutError
            If time has passed without response
        """
        timeout_err = None
        tries = self.retries
        if not timeout:
            timeout = self.timeout
        while tries >= 0:
            try:
                return self.port.retrieve_packet(timeout=self.timeout)
            except TimeoutError as err:
                tries -= 1
                timeout_err = err
                self.logger.warning(
                    "Timeout occured. Retrying. %d retries remaining.",
                    self.retries - tries,
                )

        raise TimeoutError("Timeout occured. No retries remaining.") from timeout_err

    def write_command(
        self,
        command: CommandPacket,
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
        evt = self.port.send_command(command, timeout=timeout)

        return evt

    def exit(self) -> None:
        """Close the HCI connection.

        Used to safely close the connection between the HCI and
        the test board.

        """
        self.port.exit()

    def _init_ports(
        self,
        port_id: str,
        baud: int,
        logger_name: str,
        async_callback: Optional[Callable[[AsyncPacket], Any]],
        evt_callback: Optional[Callable[[EventPacket], Any]],
    ) -> None:
        """Initializes serial ports.

        PRIVATE

        """
        self.port = SerialUartTransport(
            port_id,
            baud=baud,
            id_tag=self.id_tag,
            logger_name=logger_name,
            retries=self.retries,
            timeout=self.timeout,
            async_callback=async_callback,
            evt_callback=evt_callback,
        )
