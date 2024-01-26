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
"""Contains full HCI implementation."""
# pylint: disable=too-many-arguments
import logging
from typing import Any, Callable, Optional, Union

from .ble_standard_cmds import BleStandardCmds
from ._hci_logger import get_formatted_logger
from ._transport import SerialUartTransport
from .vendor_spec_cmds import VendorSpecificCmds
from .data_params import AdvParams, ConnParams
from .hci_packets import AsyncPacket, CommandPacket, EventPacket
from .packet_codes import StatusCode
from .constants import ADI_PORT_BAUD_RATE


class BleHci(BleStandardCmds, VendorSpecificCmds):
    """Host-controller interface.

    The BleHci object defines a host-controller interface for
    BLE testing on any BLE-compatible microchip. Controller provides
    implementations for both BLE standard HCI command and ADI vendor
    specific commands. Support is also provided for the creation and
    use of custom vendor-specific commands.

    Parameters
    ----------
    port_id : str
        ID string for the port on which a connection should be
        established.
    baud : int
        Port baud rate.
    id_tag : str
        Connection ID string to use when logging.
    log_level : Union[str, int]
        Logging level.
    logger_name : str
        Name that should be used to reference HCI logger.
    retries : int
        Number of times a port read should be retried before
        and error is thrown.
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
        Id string for the port on which a connection has been
        established
    port : SerialUartTransport
        Serial port interfacing object connected to the DUT.
    id_tag : str
        Connection ID string used by the logger.
    logger : logging.Logger
        HCI logging object reference by the `logger_name` argument.
    retries : int
        Number of times a port read should be retried before an error
        is thrown.
    timeout : float
        Port timeout.

    """

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
    ):
        self.port_id = port_id
        self.port = None
        self.id_tag = id_tag
        self.logger = get_formatted_logger(log_level=log_level, name=logger_name)
        self.retries = retries
        self.timeout = timeout

        self._init_ports(port_id, baud, logger_name, async_callback, evt_callback)
        super().__init__(self.port, logger_name)

    def get_log_level(self) -> str:
        """Retrieve the current log level.

        Retrieved the current logging level in string
        format.

        Returns
        -------
        str
            The current logging level.

        """
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
        self, connect: bool = True, adv_params: Optional[AdvParams] = None
    ) -> StatusCode:
        """Start advertising.

        Convenience function which sends a sequence of commands to
        the DUT, telling it to begin advertising. PHYs preferences
        cannot be set when using this function, but advertising
        parameters can be using the optional `adv_params` parameter.
        If a value is provided for `adv_params`, the value of the
        `connect` parameter is ignored. If no value is provided, all
        advertising parameters are defaulted and `connect` is used
        to determine the advertising type.

        Parameters
        ----------
        connect : bool, optional
            Make connectable? If true, advertising type is set to
            `0x0 (ADV_IND)`. If false, advertising type is set to
            `0x3 (ADV_NONCONN_IND)`. Ignored if `adv_params` is
            not None.
        adv_params : AdvParams, optional.
            Advertising parameters.

        Returns
        -------
        StatusCode
            The return status of the enable advertising command.

        """

        self.reset_connection_stats()
        self.set_default_phy(all_phys=0, tx_phys=7, rx_phys=7)

        if adv_params is None:
            adv_type = 0 if connect else 3
            adv_params = AdvParams(adv_type=adv_type)
        self.set_adv_params(adv_params)

        status = self.enable_adv(True)

        return status

    def init_connection(
        self,
        addr: Optional[int] = None,
        interval: int = 0x6,
        sup_timeout: int = 0x64,
        conn_params: Optional[ConnParams] = None,
    ) -> StatusCode:
        """Initialize a connection.

        Convenience function which sends a sequence of commands to
        the DUT, telling it to initialize a connection. PHYs preferences
        cannot be set when using this function, but connection parameters
        can be using the optional `conn_params` parameter. If a value is
        provided for `conn_params`, the values of the `addr`, `interval`,
        and `sup_timeout` parameters are ignored. If no value is provided,
        all connection parameters except min/max interval and supervision
        timeout are defaulted. In addition, a value for `addr` must be
        provided.

        Parameters
        ----------
        addr : int
            Peer device BD address.
        interval : int, optional
            Connection inverval.
        sup_timeout : int, optional
            Supervision timeout.

        Returns
        -------
        StatusCode
            The return status of the create connection command.

        Raises
        ------
        ValueError
            If both `addr` and `conn_params` are None.
        ValueError
            If `addr` is more than 6 bytes in size.

        """
        if conn_params is None:
            if addr is None:
                raise ValueError(
                    "Either connection parameters or address must be provided."
                )

            if max((addr.bit_length() + 7) // 8, 1) > 6:
                raise ValueError(
                    f"Address ({addr}) is too large, must be 6 bytes or less."
                )

            conn_params = ConnParams(
                addr,
                conn_interval_max=interval,
                conn_interval_min=interval,
                sup_timeout=sup_timeout,
            )

        self.reset_connection_stats()
        self.set_default_phy(all_phys=0, tx_phys=7, rx_phys=7)

        status = self.create_connection(conn_params)

        return status

    def read_event(self, timeout: Optional[float] = None) -> EventPacket:
        """Read an event from controller.

        Parameters
        ----------
        timeout : Optional[float], optional
            Timeout for read operation. Can be used to
            temporarily override this object's `timeout`
            attribute.

        Returns
        -------
        EventPacket
            Packet retrieved from the controller.

        Raises
        ------
        TimeoutError
            If a timeout occurs and there are no retries remaining.

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
        """Send a command and retrieve the return packet.

        Parameters
        ----------
        command : Union[str, int]
            Command to send. Must be an instance of the
            `CommandPacket` class.
        timeout : int
            Timeout for read portion of the read/write.
            Can be used to temporarily override this object's
            `timeout` attribute.

        Returns
        -------
        EventPacket
            The command return packet.

        """
        if not timeout:
            timeout = self.timeout
        evt = self.port.send_command(command, timeout=timeout)

        return evt

    def write_command_raw(
        self,
        raw_command: bytearray,
        timeout: Optional[float] = None,
    ) -> EventPacket:
        """Write raw command to device

        Parameters
        ----------
        raw_command : bytearray
            Command as bytearray
        timeout : int
            Timeout for read portion of the read/write.
            Can be used to temporarily override this object's
            `timeout` attribute.

        Returns
        -------
        EventPacket

        """

        if not timeout:
            timeout = self.timeout
        return self.port.send_command_raw(raw_command, timeout)

    def exit(self) -> None:
        """Close the HCI connection.

        Used to safely close the connection between the HCI and
        the test board.

        """
        self.port.close()

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
