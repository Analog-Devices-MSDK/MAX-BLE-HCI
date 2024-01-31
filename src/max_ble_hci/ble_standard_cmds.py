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
Module contains definitions for BLE standard HCI commands.
"""
# pylint: disable=too-many-arguments
from typing import Optional, Tuple, Union, List

from ._hci_logger import get_formatted_logger
from ._transport import SerialUartTransport
from .constants import PhyOption, PayloadOption
from .data_params import AdvParams, ConnParams, ScanParams
from .hci_packets import CommandPacket, EventPacket
from .packet_codes import StatusCode
from .packet_defs import OCF, OGF
from .utils import to_le_nbyte_list


class BleStandardCmds:
    """Definitions for BLE standard HCI commands.

    Class contains functions used to implement BLE standard HCI
    commands. Used as a parent for the full Analog Devices BLE
    HCI class.

    Arguments
    ---------
    port : SerialUartTransport
        Serial port interfacing object.
    logger_name: str
        Name used to reference the HCI logger.

    Attributes
    ----------
    port : SerialUartTransport
        Serial port interfacing object.
    logger : logging.Logger
        HCI logging object referenced by the `name` argument.

    """

    def __init__(self, port: SerialUartTransport, logger_name: str):
        self.port = port
        self.logger = get_formatted_logger(name=logger_name)

    def send_le_controller_command(
        self, ocf: OCF, params: List[int] = None, return_evt: bool = False
    ) -> Union[StatusCode, EventPacket]:
        """Send an LE Controller command to the test board.

        Sends a command from the OGF LE Controller subgroup to the DUT.

        Parameters
        ----------
        ocf : OCF
            Opcode command field value for the desired HCI command.
        params : List[int], optional
            Command parameters as single-byte values.
        return_evt : bool, optional
            If true, function returns full `EventPacket` object. If
            false, function returns only the status code.

        Returns
        -------
        Union[StatusCode, EventPacket]
            If `return_evt` argument is true, the full return packet
            from the DUT. If `return_evt` argument is false, the return
            packet status code.


        """
        cmd = CommandPacket(OGF.LE_CONTROLLER, ocf, params=params)
        if return_evt:
            return self.port.send_command(cmd)

        return self.port.send_command(cmd).status

    def send_link_control_command(
        self, ocf: OCF, params: List[int] = None, return_evt: bool = False
    ) -> Union[StatusCode, EventPacket]:
        """Send a Link Control command to the test board.

        Sends a command from the OGF Link Control subgroup to the DUT.

        Parameters
        ----------
        ocf : OCF
            Opcode command field value for the desired HCI command.
        params : List[int], optional
            Command parameters as single-byte values.
        return_evt : bool, optional
            If true, function returns full `EventPacket` object. If
            false, function returns only the status code.

        Returns
        -------
        Union[StatusCode, EventPacket]
            If `return_evt` argument is true, the full return packet
            from the DUT. If `return_evt` argument is false, the return
            packet status code.


        """
        cmd = CommandPacket(OGF.LINK_CONTROL, ocf, params=params)
        if return_evt:
            return self.port.send_command(cmd)

        return self.port.send_command(cmd).status

    def send_controller_command(
        self, ocf: OCF, params: List[int] = None, return_evt: bool = False
    ) -> Union[StatusCode, EventPacket]:
        """Send a Controller command to the test board.

        Sends a command from the OGF Controller subgroup to the DUT.

        Parameters
        ----------
        ocf : OCF
            Opcode command field value for the desired HCI command.
        params : List[int], optional
            Command parameters as single-byte values.
        return_evt : bool, optional
            If true, function returns full `EventPacket` object. If
            false, function returns only the status code.

        Returns
        -------
        Union[StatusCode, EventPacket]
            If `return_evt` argument is true, the full return packet
            from the DUT. If `return_evt` argument is false, the return
            packet status code.


        """
        cmd = CommandPacket(OGF.CONTROLLER, ocf, params=params)
        if return_evt:
            return self.port.send_command(cmd)

        return self.port.send_command(cmd).status

    def set_adv_params(self, adv_params: AdvParams = AdvParams()) -> StatusCode:
        """Set test board advertising parameters.

        Sends a command to the DUT, telling it to set the advertising
        parameters to the given values.

        Parameters
        ----------
        adv_params : AdvParams, optional
            Dataclass object containing the desired advertising
            parameters.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = to_le_nbyte_list(adv_params.interval_min, 2)
        params.extend(to_le_nbyte_list(adv_params.interval_max, 2))
        params.extend(
            [
                adv_params.adv_type,
                adv_params.own_addr_type.value,
                adv_params.peer_addr_type.value,
            ]
        )
        params.extend(to_le_nbyte_list(adv_params.peer_addr, 6))
        params.extend([adv_params.channel_map, adv_params.filter_policy])

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_ADV_PARAM, params=params
        )

    def enable_adv(self, enable: bool) -> StatusCode:
        """Command board to start/stop advertising.

        Sends a command to the DUT, telling it to either start or
        stop advertising based on the the `enable` argument.

        Parameters
        ----------
        enable : bool
            Enable advertising?

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_le_controller_command(OCF.LE_CONTROLLER, params=int(enable))

    def set_scan_params(self, scan_params: ScanParams = ScanParams()) -> StatusCode:
        """Set test board scanning parameters.

        Sends a command to the DUT, telling it to set the scanning
        parameters to the given values.

        Parameters
        ----------
        scan_params : ScanParams, optional
            Dataclass object containing the desired scanning parameters.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = [scan_params.scan_type]
        params.extend(to_le_nbyte_list(scan_params.scan_interval, 2))
        params.extend(to_le_nbyte_list(scan_params.scan_window, 2))
        params.append(scan_params.addr_type.value)
        params.append(scan_params.filter_policy)

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_SCAN_PARAM, params=params
        )

    def enable_scanning(
        self, enable: bool, filter_duplicates: bool = False
    ) -> StatusCode:
        """Command board to start/stop scanning.

        Sends a command to the DUT, telling it to either start or
        stop scanning based on the `enable` argument.

        Parameters
        ----------
        enable : bool
            Enable scanning?
        filter_duplicates : bool, optional
            Filter duplicates?

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = [int(enable), int(filter_duplicates)]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_SCAN_ENABLE, params=params
        )

    def create_connection(
        self, conn_params: ConnParams = ConnParams(0x0)
    ) -> StatusCode:
        """Command board to connect with a peer device.

        Sends a command to the DUT, telling it to create a connection
        to a peer device based on the given connection parameters.

        Parameters
        ----------
        conn_params : ConnParams, optional
            Dataclass object containing the desired connection parameters.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = to_le_nbyte_list(conn_params.scan_interval, 2)
        params.extend(to_le_nbyte_list(conn_params.scan_window, 2))
        params.append(conn_params.init_filter_policy)
        params.append(conn_params.peer_addr_type.value)
        params.extend(to_le_nbyte_list(conn_params.peer_addr, 6))
        params.append(conn_params.own_addr_type.value)
        params.extend(to_le_nbyte_list(conn_params.conn_interval_min, 2))
        params.extend(to_le_nbyte_list(conn_params.conn_interval_max, 2))
        params.extend(to_le_nbyte_list(conn_params.max_latency, 2))
        params.extend(to_le_nbyte_list(conn_params.sup_timeout, 2))
        params.extend(to_le_nbyte_list(conn_params.min_ce_length, 2))
        params.extend(to_le_nbyte_list(conn_params.max_ce_length, 2))

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.CREATE_CONN, params=params
        )

    def set_default_phy(
        self, all_phys: int = 0x0, tx_phys: int = 0x7, rx_phys: int = 0x7
    ) -> StatusCode:
        """Set defaults for ALL, TX, and RX PHYs.

        Sends a command to the DUT, telling it to set the default behavior
        for ALL, TX, and RX PHYs in accordance with the given values.

        Parameters
        ----------
        all_phys : int, optional
            Value describing desired behavior of all PHYs.
        tx_phys : int, optional
            Value describing desired behavior of TX PHYs.
        rx_phys : int, optional
            Value describing desired behavior of RX PHYs.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = [all_phys, tx_phys, rx_phys]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_DEF_PHY, params=params
        )

    def set_data_len(
        self, handle: int = 0x0000, tx_octets: int = 0xFB00, tx_time: int = 0x9042
    ) -> StatusCode:
        """Set the maximum TX payload size and transmit time.

        Sends a command to the DUT, telling it to set the maximum TX
        payload size and transmit time to the given values.

        Parameters
        ----------
        handle : int, optional
            Connection handle.
        tx_octets : int, optional
            Desired maximum number of payload octets.
        tx_time : int, optional
            Desired maximum TX time.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = to_le_nbyte_list(handle, 2)
        params.extend(to_le_nbyte_list(tx_octets, 2))
        params.extend(to_le_nbyte_list(tx_time, 2))
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_DATA_LEN, params=params
        )

    def set_phy(
        self,
        handle: int = 0x0000,
        all_phys: int = 0x0,
        tx_phys: int = 0x7,
        rx_phys: int = 0x7,
        phy_opts: int = 0x0,
    ) -> StatusCode:
        """Set the PHY preferences for a connection.

        Sends a command to the DUT, telling it to set the PHY preferences
        for the indicated connection in accordance with the given values.

        Parameters
        ----------
        handle : int, optional
            The handle to the desired connection.
        all_phys : int, optional
            Behavior settings for all PHYs. Indicates if a PHY preference
            exists for both RX and TX PHYs.
        tx_phys : PhyOption, optional
            PHY preference for TX PHYs.
        rx_phys : PhyOption, optional
            PHY preference for RX PHYs.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        if not 0 <= all_phys <= 3:
            self.logger.warning(
                "Invalid all PHYs option (%i), must be between 0x0 and 0x3. Defaulting to 0x0.",
                all_phys,
            )
        if all_phys in (1, 3) and not 0 < tx_phys <= 7:
            self.logger.warning(
                "Invalid TX PHY option (%i), must be between 0x1 and 0x7. Defaulting to 0x7.",
                tx_phys,
            )
            tx_phys = 0x7
        if all_phys in (2, 3) and not 0 < rx_phys <= 7:
            self.logger.warning(
                "Invalid RX PHY option (%i), must be between 0x1 and 0x7. Defaulting to 0x7.",
                rx_phys,
            )
            rx_phys = 0x7
        if phy_opts not in (0, 1, 2, 4):
            self.logger.warning(
                "Invalid PHY options (%i), must be 0x0, 0x1, 0x2, or 0x4. Defaulting to 0x0.",
                phy_opts,
            )
            phy_opts = 0x0

        params = to_le_nbyte_list(handle, 2)
        params.extend([all_phys, tx_phys, rx_phys])
        params.extend(to_le_nbyte_list(phy_opts, 2))

        return self.send_le_controller_command(OCF.LE_CONTROLLER.SET_PHY, params=params)

    def tx_test(
        self,
        channel: int = 0,
        phy: Union[PhyOption, int] = PhyOption.PHY_1M,
        payload: Union[PayloadOption, int] = PayloadOption.PLD_PRBS9,
        packet_len: int = 0,
    ) -> StatusCode:
        """Start a transmitter test.

        Sends a command to the DUT, telling it to start a DTM transmitter
        test in accordance with the given parameters.

        Parameters
        ----------
        channel : int, optional
            The channel on which transmission should take place.
        phy : Union[PhyOption,int], optional
            The PHY that should be used by the transmitter.
        payload : PayloadOption, optional
            The packet payload type that should be used.
        packet_len : int, optional
            The desired length of the transmitted packets.

        Returns
        -------
        StatusCode
            The return packet status code.

        """

        if isinstance(payload, PayloadOption):
            payload = payload.value
        if isinstance(phy, PhyOption):
            phy = phy.value

        params = [channel, packet_len, payload, phy]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.ENHANCED_TRANSMITTER_TEST, params=params
        )

    def rx_test(
        self,
        channel: int = 0,
        phy: Union[PhyOption, int] = PhyOption.PHY_1M,
        modulation_idx: int = 0,
    ) -> StatusCode:
        """Start a receiver test.

        Sends a command to the DUT, telling it to start a DTM receiver
        test in accordance with the given parameters.

        Parameters
        ----------
        channel : int, optional
            The channel on which the receiver should listen for packets.
        phy : Union[PhyOption,int], optional
            The PHY that should be used by the receiver.
        modulation_idx : float, optional
            The expected modulation index of the transmitter. Indicates
            whether the modulation index is standard (0) or stable (1).

        Returns
        -------
        StatusCode
            The return packet status code.

        """

        if phy == PhyOption.PHY_CODED_S2:
            phy = PhyOption.PHY_CODED_S8

        if isinstance(phy, PhyOption):
            phy = phy.value

        params = [channel, phy, modulation_idx]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.ENHANCED_RECEIVER_TEST, params=params
        )

    def end_test(self) -> Tuple[int, StatusCode]:
        """End the current test.

        Sends a command to the DUT, telling it to end the current
        DTM test.

        Returns
        -------
        StatusCode
            The return packet status code.
        int
            The number of packets received correctly during the test. If
            ending a TX test, this value will be 0.

        """
        evt = self.send_le_controller_command(
            OCF.LE_CONTROLLER.TEST_END, return_evt=True
        )
        rx_ok = evt.get_return_params()

        return rx_ok, evt.status

    def disconnect(self, handle: int = 0x0000, reason: int = 0x16) -> StatusCode:
        """Disconnect from an existing connection.

        Sends a command to the DUT, telling it to disconnect from
        the indicated connection for the given reason.

        Parameters
        ----------
        handle : int, optional
            The handle to the desired connection.
        reason : int, optional
            The reason for the disconnection.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = to_le_nbyte_list(handle, 2)
        params.append(reason)
        return self.send_link_control_command(
            OCF.LINK_CONTROL.DISCONNECT, params=params
        )

    def reset(self) -> StatusCode:
        """Reset board controller/link layer.

        Sends a command to the DUT, telling it that the controller
        and the link layer should be reset. On-board implementation
        may vary, meaning this command does not necessarily perform
        a full hardware reset.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_controller_command(OCF.CONTROLLER.RESET)

    def set_event_mask(
        self, mask: int, mask_pg2: Optional[int] = None
    ) -> Union[StatusCode, Tuple[StatusCode, StatusCode]]:
        """Enable/disable events the board can generate.

        Sends a command to the DUT, telling it to enable/disable
        events that can be generated and returned to the host in
        accordance with the given mask. If a page2 mask if provided,
        then the command which sets the page2 masks will also be sent.

        Parameters
        ----------
        mask : int
            Mask indicating the desired events. Setting a bit to `1`
            enables the corresponding event. Setting the bit to `0`
            disables it.
        mask_pg2 : Optional[int], optional
            Mask indicating the desired events for the second event
            mask page. Setting a bit to `1` enables the corresponding
            event. Setting the bit to `0` disables it.

        Returns
        -------
        Union[StatusCode, Tuple[StatusCode, StatusCode]]
            The return packet status codes(s). If both page1 and page2
            were set, the first return is the status code for the page1
            command and the second is the status code for the page2
            command.

        """
        params = to_le_nbyte_list(mask, 8)
        status = self.send_controller_command(
            OCF.CONTROLLER.SET_EVENT_MASK, params=params
        )

        if mask_pg2:
            params = to_le_nbyte_list(mask_pg2, 8)
            return (
                status,
                self.send_controller_command(
                    OCF.CONTROLLER.SET_EVENT_MASK_PAGE2, params=params
                ),
            )

        return status

    def set_event_mask_le(self, mask: int) -> StatusCode:
        """Enable/disable LE events the board can generate.

        Sends a command to the DUT, telling it to enable/disable
        LE events that can be generated and returned to the host
        in accordance with the given mask.

        Parameters
        ----------
        mask : int
            Mask indicating the desired LE events. Setting a bit
            to `1` enables the corresponding event. Setting the
            bit to `0` disables it.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = to_le_nbyte_list(mask, 8)
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_EVENT_MASK, params=params
        )
