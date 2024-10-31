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
# pylint: disable=too-many-arguments,too-many-lines
from typing import List, Optional, Tuple, Union, Callable

from ._hci_logger import get_formatted_logger
from ._transport import SerialUartTransport
from .constants import PayloadOption, PhyOption
from .data_params import AdvParams, ConnParams, EstablishConnParams, ScanParams
from .hci_packets import CommandPacket, EventPacket
from .packet_codes import EventMask, EventMaskPage2, EventMaskLE, StatusCode
from .packet_defs import OCF, OGF
from .utils import (
    can_represent_as_bytes,
    to_le_nbyte_list,
    byte_length,
    address_str2int,
)
from .ad_types import AddressType


class BleStandardCmds:
    # pylint: disable=too-many-public-methods
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
        self.event_mask = None
        self.event_mask_pg2 = None
        self.event_mask_le = None

    def __enter__(self):
        self.port.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.port.close()

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

    def set_adv_data(self, data: list) -> StatusCode:
        """Set advertising data

        Parameters
        ----------
        data : list
            data to advertise

        Returns
        -------
        StatusCode
            Status

        Raises
        ------
        ValueError
            If advertising data cannot be represented in 31 octets or less
        """
        if not can_represent_as_bytes(data) or len(data) > 31:
            raise ValueError("Advertising data length can be up to 31 octets")

        params = [len(data)] + data
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_ADV_DATA, params=params
        )

    def set_scan_resp_data(self, data: list) -> StatusCode:
        """Set advertising data

        Parameters
        ----------
        data : list
            data to respond with on scan requests

        Returns
        -------
        StatusCode
            Status

        Raises
        ------
        ValueError
            If scan request data cannot be represented in 31 octets or less
        """
        if not can_represent_as_bytes(data) or len(data) > 31:
            raise ValueError("Advertising data length can be up to 31 octets")

        params = [len(data)] + data
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_SCAN_RESP_DATA, params=params
        )

    def set_random_address(self, addr: Union[int, str]) -> StatusCode:
        """Sets the random address.

        Function sets the chip random address. Address can be given
        as either a bytearray or as a list of integer values.

        Parameters
        ----------
        addr : Union[int, str]
            Desired random address.
            If str, format expected xx:xx:xx:xx:xx

        Returns
        -------
        StatusCode
            The return packet status code.

        """

        if isinstance(addr, str):
            addr = address_str2int(addr)

        params = to_le_nbyte_list(addr, 6)
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_RAND_ADDR, params=params
        )

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
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_ADV_ENABLE, params=int(enable)
        )

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

    def update_connection_params(
        self,
        handle: int = 0x0000,
        conn_params: ConnParams = ConnParams(0x0),
        callback: Callable = None,
    ) -> StatusCode:
        """Update connection parameters

        Parameters
        ----------
        handle : str
            Connection Handle
        conn_params : ConnParams, optional
            Connection paramters by default ConnParams(0x0)

        Returns
        -------
        StatusCode
            The return packet status code.
        """

        if callback is not None:
            self.set_event_mask_le(EventMaskLE.CONN_UPDATE_COMPLETE)
            self.set_event_callback(callback)

        params = to_le_nbyte_list(handle, 2) + conn_params.to_payload()

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.CONN_UPDATE, params=params
        )

    def create_connection(
        self, conn_params: EstablishConnParams = EstablishConnParams(0x0)
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

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.CREATE_CONN, params=conn_params.to_payload()
        )

    def set_default_phy(
        self,
        tx_phys: Union[PhyOption, List[PhyOption]] = None,
        rx_phys: Union[PhyOption, List[PhyOption]] = None,
    ) -> StatusCode:
        """Set default phy used for TX and RX

        Parameters
        ----------
        tx_phys : Union[PhyOption, List[PhyOption]], optional
            Preferred PHY or list of preferred PHYs for TX, by default None meaning no preference
        rx_phys : Union[PhyOption, List[PhyOption]], optional
            Preferred PHY or list of preferred PHYs for TX, by default None meaning no preference

        Returns
        -------
        StatusCode
            The return packet status code.
        """

        if not isinstance(tx_phys, list):
            tx_phys = [tx_phys]

        if not isinstance(rx_phys, list):
            rx_phys = [rx_phys]

        all_phys = 0
        if tx_phys is None:
            all_phys |= 1
            tx_phys = []
        elif rx_phys is None:
            all_phys |= 2
            rx_phys = []

        phy_opts = 0
        tx_phy_mask = 0
        for phy in tx_phys:
            tx_mask, coded_opt = PhyOption.to_mask(phy)
            phy_opts |= coded_opt
            tx_phy_mask |= tx_mask

        rx_phy_mask = 0
        for phy in rx_phys:
            rx_mask, coded_opt = PhyOption.to_mask(phy)
            rx_phy_mask |= rx_mask
            phy_opts |= coded_opt

        params = [all_phys, tx_phy_mask, rx_phy_mask]
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
        tx_phys: Union[PhyOption, List[PhyOption]] = None,
        rx_phys: Union[PhyOption, List[PhyOption]] = None,
    ) -> StatusCode:
        """Set PHY during connection

        Parameters
        ----------
        handle : int, optional
            connection handle, by default 0x0000
        tx_phys : Union[PhyOption, List[PhyOption]], optional
            PHY or list of PHYS preferred for TX, by default None meaning no preference
        rx_phys : Union[PhyOption, List[PhyOption]], optional meaning no preference
            PHY or list of PHYs preferred for RX, by default None

        Returns
        -------
        StatusCode
            The return packet status code.
        """

        if not isinstance(tx_phys, list):
            tx_phys = [tx_phys]

        if not isinstance(rx_phys, list):
            rx_phys = [rx_phys]

        all_phys = 0
        if tx_phys is None:
            all_phys |= 1
            tx_phys = []
        elif rx_phys is None:
            all_phys |= 2
            rx_phys = []

        phy_opts = 0
        tx_phy_mask = 0
        for phy in tx_phys:
            tx_mask, coded_opt = PhyOption.to_mask(phy)
            phy_opts |= coded_opt
            tx_phy_mask |= tx_mask

        rx_phy_mask = 0
        for phy in rx_phys:
            rx_mask, coded_opt = PhyOption.to_mask(phy)
            rx_phy_mask |= rx_mask
            phy_opts |= coded_opt

        params = to_le_nbyte_list(handle, 2)
        params.extend([all_phys, tx_phy_mask, rx_phy_mask])
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

        # return self.send_controller_command(OCF.CONTROLLER.RESET)

    def set_event_mask(
        self,
        mask: Union[int, EventMask],
        mask_pg2: Optional[Union[int, EventMaskPage2]] = None,
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

        if isinstance(mask, EventMask):
            self.event_mask = mask
            mask = mask.value
        else:
            self.event_mask = EventMask(mask)

        params = to_le_nbyte_list(mask, 8)
        status = self.send_controller_command(
            OCF.CONTROLLER.SET_EVENT_MASK, params=params
        )

        if mask_pg2 is not None:
            if isinstance(mask_pg2, EventMaskPage2):
                self.event_mask_pg2 = mask_pg2
                mask_pg2 = mask_pg2.value
            else:
                self.event_mask_pg2 = EventMaskPage2(mask_pg2)

            params = to_le_nbyte_list(mask_pg2, 8)
            return (
                status,
                self.send_controller_command(
                    OCF.CONTROLLER.SET_EVENT_MASK_PAGE2, params=params
                ),
            )

        return status

    def set_event_mask_le(self, mask: Union[int, EventMaskLE]) -> StatusCode:
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
        if isinstance(mask, EventMaskLE):
            self.event_mask_le = mask
            mask = mask.value
        else:
            self.event_mask_le = EventMaskLE(mask)

        if self.event_mask is None:
            self.set_event_mask(EventMask.LE_META)
        else:
            self.set_event_mask(self.event_mask | EventMask.LE_META)

        params = to_le_nbyte_list(mask, 8)
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_EVENT_MASK, params=params
        )

    def clear_whitelist(self) -> StatusCode:
        """Clear whitelist entirely

        Returns
        -------
        StatusCode
            status of command
        """
        return self.send_le_controller_command(OCF.LE_CONTROLLER.CLEAR_WHITE_LIST)

    def read_whitelist_size(self) -> Union[StatusCode, int]:
        """Read total spaces in white list

        Returns
        -------
        int
            number of places in whitelist
        """
        params: EventPacket = self.send_le_controller_command(
            OCF.LE_CONTROLLER.READ_WHITE_LIST_SIZE, return_evt=True
        )

        if params.status != StatusCode.SUCCESS:
            self.logger.error("Failed to read whitelist size")
            return params.status

        print(list(params.evt_params))
        return params.get_return_params()

    def _form_whitelist_cmd_params(
        self, addr_type: Union[AddressType, int], address: Union[str, int, List[int]]
    ) -> List[int]:
        if isinstance(addr_type, AddressType):
            addr_type = addr_type.value

        params = [addr_type]

        if isinstance(address, list):
            if len(address) != 6:
                raise ValueError("Address length must be 6 bytes when given as list")

            # Apped as little endian
            params.extend(address.reverse())

        else:
            if isinstance(address, str):
                address = address_str2int(address)

            if byte_length(address) > 6:
                raise ValueError("Address must be representable in 6 bytes!")

            params.extend(to_le_nbyte_list(address, 6))

        return params

    def add_device_to_whitelist(
        self, addr_type: Union[AddressType, int], address: Union[str, int, List[int]]
    ) -> StatusCode:
        """Add device to whitelist

        Parameters
        ----------
        addr_type : Union[AddressType, int]
            Address type of devcie
        address : Union[str, int, List[int]]
            Address of device
            - str: aa:bb:cc:dd:ee
            - List[int]: [aa, bb, cc, dd, ee, ff]
            - int: 733295205870

        Returns
        -------
        StatusCode
            status of command
        """
        params = self._form_whitelist_cmd_params(addr_type=addr_type, address=address)

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.ADD_DEV_WHITE_LIST, params=params
        )

    def remove_device_from_whitelist(
        self, addr_type: Union[AddressType, int], address: Union[str, int, List[int]]
    ) -> StatusCode:
        """Remove device from whitelist

        Parameters
        ----------
        addr_type : Union[AddressType, int]
            Address type of devcie
        address : Union[str, int, List[int]]
            Address of device
            - str: aa:bb:cc:dd:ee
            - List[int]: [aa, bb, cc, dd, ee, ff]
            - int: 733295205870
        Returns
        -------
        StatusCode
            status of command

        """
        params = self._form_whitelist_cmd_params(addr_type=addr_type, address=address)

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.REMOVE_DEV_WHITE_LIST, params=params
        )

    def read_local_p256_pub_key(
        self, callback: Callable[[EventPacket], None] = None
    ) -> StatusCode:
        """Read local P256 Key

        Parameters
        ----------
        callback : Callable[[EventPacket], None], optional
            Callback to call when complete event is triggered, by default None

        Returns
        -------
        StatusCode
            The return packet status code.

        NOTE: Event not enabled for you. Please enable event.
        """
        if callback:
            self.port.evt_callback = callback

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.READ_LOCAL_P256_PUB_KEY
        )

    def generate_dhk(
        self,
        xcoord: int,
        ycoord: int,
        version: int = 1,
        use_debug_key=False,
        callback: Callable[[EventPacket], None] = None,
    ) -> StatusCode:
        """Generate Diffie-Hellman Key

        Parameters
        ----------
        xcoord : int
            X-Coordinate
        ycoord : int
            Y-Coordinate
        version : int, optional
            DHK gen version, by default 1. Options 1 or 2
        use_debug_key : bool, optional
            Use a debug key instead of in use key, by default False
        callback : Callable[[EventPacket], None], optional
            Callback to call when complete event is triggered, by default None, by default None

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If version not 1 or 2

        NOTE: Complete event not enabled for you. Please enable event if needed.
        """
        if version not in (1, 2):
            raise ValueError("DHK generate version must be 1 or 2")

        xcoords = to_le_nbyte_list(xcoord, 32)
        ycoords = to_le_nbyte_list(ycoord, 32)

        if version != 1:
            key_type = 0 if not use_debug_key else 1
        else:
            key_type = 0x4B

        params = xcoords + ycoords + [key_type]

        ocf = (
            OCF.LE_CONTROLLER.GENERATE_DHKEY
            if version == 1
            else OCF.LE_CONTROLLER.GENERATE_DHKEY_V2
        )

        if callback is not None:
            self.port.evt_callback = callback

        return self.send_le_controller_command(ocf, params)

    def convert_fips197(self, data: Union[int, str]) -> List[int]:
        """Convert data to fips197 format

        Parameters
        ----------
        data : Union[int, str]
            Integer of string

        Returns
        -------
        List[int]
            fips197 formatted data

        Raises
        ------
        ValueError
            Input is not an int or str
        ValueError
            Data cannot be represented in 16-bytes
        """
        if isinstance(data, int):
            byte_len = byte_length(data)
            data_bytes = [0] * 16
            for i in range(byte_len):
                bit_pos = 8 * (byte_len - i - 1)
                data_bytes[i] = (data >> bit_pos) & 0xFF
        elif isinstance(data, str):
            data_bytes = data.encode("utf-8")
            if len(data_bytes) < 16:
                data_bytes = data_bytes.ljust(16, b"\x00")
            data_bytes = list(data_bytes)
        else:
            raise ValueError("Input must be an integer or string")

        if len(data_bytes) > 16:
            raise ValueError("Value must be able to be represented in 16 bytes!")

        return data_bytes

    def encrypt(
        self, key: Union[bytes, int, str], plaintext: Union[int, bytes, str]
    ) -> Union[List[int], EventPacket]:
        """Encrypt data

        Parameters
        ----------
        key : Union[bytes, int, str]
            Key to encrypt plaintex with
        plaintext : Union[int, bytes, str]
            data to encrypt
            Will pad data with zeros if the block is not 16 bytes

        Returns
        -------
        Union[List[int], EventPacket]
            Ciphertext if encryption succeeded. Event packet othewise.

        Raises
        ------
        ValueError
            If key is an integer and cannot be represented in 128 bits
        ValueError
            If key is bytes or string an not 16-bytes in length
        ValueError
            If plaintext cannot be represented ins 128 bits
        ValueError
            If plaintext bytes or string and more than 16 bytes
        """
        if isinstance(key, int) and key.bit_length() > 128:
            raise ValueError("Key must be representable in 128 bits!")
        if isinstance(key, (bytes, str)) and len(key) != 16:
            raise ValueError("Key must be 128 bits if given as bytes or str!")

        if isinstance(plaintext, int) and plaintext.bit_length() > 128:
            raise ValueError("Plaintext must be representable in 128 bits!")
        if isinstance(plaintext, (bytes, str)) and len(plaintext) > 16:
            raise ValueError("Plaintext must be representable in 128 bits!")

        if isinstance(key, int):
            key = self.convert_fips197(key)
        if isinstance(key, bytes):
            key = list(key)

        if not isinstance(plaintext, bytes):
            plaintext = self.convert_fips197(plaintext)
        else:
            if len(plaintext) < 16:
                plaintext = plaintext.ljust(16, b"\x00")
            plaintext = list(plaintext)

        params = key + plaintext
        evt = self.send_le_controller_command(
            OCF.LE_CONTROLLER.ENCRYPT, params=params, return_evt=True
        )

        if evt.status == StatusCode.SUCCESS:
            return list(evt.evt_params[4:])

        return evt

    def enable_encryption(
        self,
        handle: int,
        random: Union[bytes, int, str],
        ediv: Union[bytes, int, str],
        ltk=Union[bytes, int, str],
    ) -> StatusCode:
        """Enable encryption command

        Used by the master to enable LL encryption.

        Parameters
        ----------
        handle : int
            Connection handle
        random : Union[bytes, int, str]
            64 bit random number
        ediv : Union[bytes, int, str]
            16 bit encrypted diversifier.
        ltk : Union[int, bytes, str]
            128 bit Long term Key

        Returns
        -------
        StatusCode
            Status

        Raises
        ------
        ValueError
            If ltk is an integer and cannot be represented in 128 bits
        ValueError
            If ltk is bytes or string an not 16 bytes in length
        ValueError
            If random cannot be represented ins 64 bits
        ValueError
            If random bytes or string and more than 8 bytes
        ValueError
            If ediv cannot be represented ins 16 bits
        ValueError
            If ediv bytes or string and more than 2 bytes
        """

        if isinstance(random, int) and random.bit_length() > 64:
            raise ValueError("Random must be representable in 128 bits!")
        if isinstance(random, (bytes, str)) and len(random) != 8:
            raise ValueError("Random must be 64 bits if given as bytes or str!")

        if isinstance(ediv, int) and ediv.bit_length() > 16:
            raise ValueError("Random must be representable in 16 bits!")
        if isinstance(ediv, (bytes, str)) and len(ediv) != 2:
            raise ValueError("Random must be 16 bits if given as bytes or str!")

        if isinstance(ltk, int) and ltk.bit_length() > 128:
            raise ValueError("LTK must be representable in 128 bits!")
        if isinstance(ltk, (bytes, str)) and len(ltk) != 16:
            raise ValueError("LTK must be 128 bits if given as bytes or str!")

        if isinstance(ltk, int):
            ltk = self.convert_fips197(ltk)
        if isinstance(ltk, bytes):
            ltk = list(ltk)

        params = (
            to_le_nbyte_list(handle, 2)
            + to_le_nbyte_list(random, 8)
            + to_le_nbyte_list(ediv, 2)
            + ltk
        )

        evt = self.send_le_controller_command(
            OCF.LE_CONTROLLER.START_ENCRYPTION, params=params, return_evt=True
        )

        if evt.status == StatusCode.SUCCESS:
            return list(evt.evt_params[4:])

        return evt

    def ltk_reply(self, handle: int, ltk=Union[bytes, int, str]) -> StatusCode:
        """LTK Reply command

        Used by the slave to set the LTK for a given connection.

        Parameters
        ----------
        handle : int
            Connection handle
        ltk : Union[int, bytes, str]
            128 bit Long term Key

        Returns
        -------
        StatusCode
            Status

        Raises
        ------
        ValueError
            If ltk is an integer and cannot be represented in 128 bits
        ValueError
            If ltk is bytes or string an not 16 bytes in length
        """

        if isinstance(ltk, int) and ltk.bit_length() > 128:
            raise ValueError("LTK must be representable in 128 bits!")
        if isinstance(ltk, (bytes, str)) and len(ltk) != 16:
            raise ValueError("LTK must be 128 bits if given as bytes or str!")

        if isinstance(ltk, int):
            ltk = self.convert_fips197(ltk)
        if isinstance(ltk, bytes):
            ltk = list(ltk)

        params = to_le_nbyte_list(handle, 2) + ltk

        evt = self.send_le_controller_command(
            OCF.LE_CONTROLLER.LTK_REQ_REPL, params=params, return_evt=True
        )

        if evt.status == StatusCode.SUCCESS:
            return list(evt.evt_params[4:])

        return evt

    def set_event_callback(self, callback):
        """Set callback used for event packet

        Parameters
        ----------
        callback : Callable
            Function to call on event packet
        """
        self.port.evt_callback = callback

    def set_async_callback(self, callback):
        """Set callback used for async packet

        Parameters
        ----------
        callback : Callable
            Function to call on async packet
        """
        self.port.async_callback = callback
