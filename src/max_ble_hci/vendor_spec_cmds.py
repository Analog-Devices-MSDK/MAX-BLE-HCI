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
Module contains definitions for ADI vendor-specific HCI commands.
"""
# pylint: disable=too-many-lines, too-many-arguments, too-many-public-methods
from typing import Optional, Tuple, Union, Dict, List

from ._hci_logger import get_formatted_logger
from ._transport import SerialUartTransport
from .constants import PhyOption, PayloadOption, PubKeyValidateMode, MAX_U32, MAX_U64
from .data_params import (
    AdvPktStats,
    DataPktStats,
    MemPktStats,
    PduPktStats,
    PoolStats,
    ScanPktStats,
    TestReport,
)
from .hci_packets import CommandPacket, EventPacket, byte_length
from .packet_codes import StatusCode
from .packet_defs import OCF, OGF
from .utils import to_le_nbyte_list


class VendorSpecificCmds:
    """Definitions for ADI vendor-specific HCI commands.

    Class contains functions used to implement Analog Devices
    vendor-specific HCI commands. Used as a parent for the full
    Analog Devices BLE HCI class.

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

    def send_vs_command(
        self, ocf: OCF, params: List[int] = None, return_evt: bool = False
    ) -> Union[EventPacket, StatusCode]:
        """Send a vendor-specific command to the test board.

        Sends a command from the OGF Vendor Specific subgroup to the DUT.

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
        cmd = CommandPacket(OGF.VENDOR_SPEC, ocf, params=params)
        if return_evt:
            return self.port.send_command(cmd)

        return self.port.send_command(cmd).status

    def set_address(self, addr: int) -> StatusCode:
        """Sets the BD address.

        Function sets the chip BD address. Address can be given
        as either a bytearray or as a list of integer values.

        Parameters
        ----------
        addr : List[int]
            Desired BD address.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = to_le_nbyte_list(addr, 6)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_BD_ADDR, params=params)

    def reset_connection_stats(self) -> StatusCode:
        """Reset accumulated connection stats.

        Sends a vendor-specific command to the DUT, telling it to
        reset all accumulated connection statisitics.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(OCF.VENDOR_SPEC.RESET_CONN_STATS)

    def enable_autogenerate_acl(self, enable: bool) -> StatusCode:
        """Enable/disable automatic generation of ACL packets.

        Sends a vendor-specific command to the DUT, telling it to
        enable or disable automatic generation of asynchronous
        connection-less packets.

        Parameters
        ----------
        enable: bool
            Enable automatic ACL packet generation?

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(
            OCF.VENDOR_SPEC.ENA_AUTO_GEN_ACL, params=int(enable)
        )

    def generate_acl(
        self, handle: int, packet_len: int, num_packets: int
    ) -> StatusCode:
        """Command board to generate ACL data.

        Sends a vendor-specific command to the DUT telling it
        to generate/send ACL data in accordance with the provided
        packet length and number of packets. A test end function
        must be called to end this process on the board.

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
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.
        ValueError
            If `packet_len` is greater than 65535.
        ValueError
            If `num_packets` is greater than 255.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )
        if num_packets > 0xFFFF:
            raise ValueError(
                f"Num packets too large ({num_packets}), must be 65535 or less."
            )
        if packet_len > 0xFF:
            raise ValueError(
                f"Packet length too large ({packet_len}), must be 255 or less."
            )

        params = to_le_nbyte_list(handle, 2)
        params.append(packet_len)
        params.extend(to_le_nbyte_list(num_packets, 2))
        return self.send_vs_command(OCF.VENDOR_SPEC.GENERATE_ACL, params=params)

    def enable_acl_sink(self, enable: bool) -> StatusCode:
        """Enable/disable ACL sink.

        Sends a vendor-specific command to the DUT, telling it to
        enable or disable asynchronous connection-less packet sink.

        Parameters
        ----------
        enable : bool
            Enable ACL sink?

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = int(enable)
        return self.send_vs_command(OCF.VENDOR_SPEC.ENA_ACL_SINK, params=params)

    def tx_test_vs(
        self,
        channel: int = 0,
        phy: Union[PhyOption, int] = PhyOption.PHY_1M,
        payload: Union[PayloadOption, int] = PayloadOption.PLD_PRBS15,
        packet_len: int = 0,
        num_packets: int = 0,
    ) -> StatusCode:
        """Start a vendor-specific transmitter test.

        Sends a vendor-specific command to the DUT, telling it to
        start a DTM transmitter test in accordance with the given
        parameters.

        Parameters
        ----------
        channel : int
            The channel on which transmission should take place.
        phy : Union[PhyOption, int]
            The PHY that should be used by the transmitter.
        payload : Union[PayloadOption, int]
            The packet payload type that should be transmitted.
        packet_len : int
            The desired length of the transmitted packets.
        num_packets : int
            The number of packets to transmit. Set to `0` to
            enable continuous transmission.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `channel` is greater than 39 or less than 0.
        ValueError
            If `packet_len` is greater than 255.
        ValueError
            If `num_packets` is greater than 65535.

        """
        if not 0 <= channel < 40:
            raise ValueError(
                f"Channel out of bandwidth ({channel}), must be in range [0, 40)."
            )
        if packet_len > 0xFF:
            raise ValueError(
                f"Packet length too large ({packet_len}), must be 255 or less."
            )
        if num_packets > 0xFFFF:
            raise ValueError(
                f"Num packets too large ({num_packets}), must be 65535 or less."
            )

        if isinstance(payload, PayloadOption):
            payload = payload.value
        if isinstance(phy, PhyOption):
            phy = phy.value

        params = [channel, packet_len, payload.value, phy.value]
        params.extend(to_le_nbyte_list(num_packets, 2))
        return self.send_vs_command(OCF.VENDOR_SPEC.TX_TEST, params=params)

    def rx_test_vs(
        self,
        channel: int = 0,
        phy: Union[PhyOption, int] = PhyOption.PHY_1M,
        num_packets: int = 0,
        modulation_idx: int = 0,
    ) -> StatusCode:
        """Start a vendor-specific receiver test.

        Sends a vendor-specific command to the DUT, telling it to
        start a DTM receiver test in accordance with the given
        parameters.

        Parameters
        ----------
        channel : int
            The channel on which the receiver should listen for packets.
        phy : Union[PhyOption, int]
            The PHY that should be used by the receiver.
        num_packets : int
            The number of packets that the receiver is expected to receive,
            i.e. the number of packets the transmitter is sending.
        modulation_idx : int
            The expected modulation index of the transmitter. Indicates
            whether the modulation index is standard (0) or stable (1).

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `channel` is greater than 39 or less than 0.
        ValueError
            if `num_packets` is greater than 65535.

        """
        if not 0 <= channel < 40:
            raise ValueError(
                f"Channel out of bandwidth ({channel}), must be in range [0, 40)."
            )
        if num_packets > 0xFFFF:
            raise ValueError(
                f"Num packets too large ({num_packets}), must be 65535 or less."
            )

        if isinstance(phy, PhyOption):
            phy = phy.value

        params = [channel, phy.value, modulation_idx]
        params.extend(to_le_nbyte_list(num_packets, 2))
        return self.send_vs_command(OCF.VENDOR_SPEC.RX_TEST, params=params)

    def reset_test_stats(self) -> StatusCode:
        """Reset accumulated test stats.

        Sends a vendor-specific command to the DUT, telling it to
        reset all accumulated test statistics.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(OCF.VENDOR_SPEC.RESET_TEST_STATS)

    def set_adv_tx_power(self, tx_power: int) -> StatusCode:
        """Set the advertising TX power.

        Sends a vendor-specific command to the DUT, telling it to
        set the advertising TX power in accordance with the given
        value.

        Parameters
        ----------
        tx_power : int
            Desired advertising TX power.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `tx_power` is greater than 127 or less than -127.

        """
        if not -127 < tx_power < 127:
            raise ValueError(
                f"TX power ({tx_power}) out of range, must be in range [-127, 127]."
            )

        return self.send_vs_command(OCF.VENDOR_SPEC.SET_ADV_TX_PWR, params=tx_power)

    def set_conn_tx_power(self, tx_power: int, handle: int = 0x0000) -> StatusCode:
        """Set the connection TX power.

        Sends a vendor-specific command to the DUT, telling it to
        set the TX power on the indicated connection in accordance
        with the given value.

        Parameters
        ----------
        tx_power : int
            Desired connection TX power.
        handle : int, optional
            The handle to the desired connection.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is more than 2 bytes in size.
        ValueError
            If `tx_power` is greater than 127 or less than -127.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )
        if not -127 < tx_power < 127:
            raise ValueError(
                f"TX power ({tx_power}) out of range, must be in range [-127, 127]."
            )

        params = to_le_nbyte_list(handle, 2)
        params.append(tx_power)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_CONN_TX_PWR, params=params)

    def set_channel_map(
        self,
        channels: Optional[Union[List[int], int]] = None,
        handle: int = 0x0000,
    ) -> StatusCode:
        """Set the channel map for an existing connection.

        Sends a vendor-specific command to the DUT, telling it to
        set the channel map for the indicated connection in
        accordance with the mask generated from the given channel
        values.

        Parameters
        ----------
        channels : Union[List[int], int], optional
            The channel(s) that should be included in the connection
            channel map.
        handle : int, optional
            The handle to the desired connection.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is more than 2 bytes in size.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )

        if channels:
            channels = channels if isinstance(channels, list) else [channels]
            channel_mask = 0x0000000000
            for chan in channels:
                if chan in [37, 38, 39]:
                    continue
                channel_mask = channel_mask | (1 << chan)
        else:
            channel_mask = 0x1FFFFFFFFF

        params = to_le_nbyte_list(handle, 2)
        params.extend(to_le_nbyte_list(channel_mask, 5))

        return self.send_vs_command(OCF.VENDOR_SPEC.SET_CHAN_MAP, params=params)

    def read_register(
        self, addr: int, length: int, print_data: bool = False
    ) -> Tuple[List[int], StatusCode]:
        """Read a number of bytes from a register.

        Sends a vendor-specific command to the DUT, telling it to
        read bytes from a register in accordance with the given
        length and register address values.

        Parameters
        ----------
        addr : int
            The address at which the read should begin.
        length : int
            The number of bytes to read.
        print_data : bool, optional
            Print read data to the console?

        Returns
        -------
        List[int]
            The read data.
        StatusCode
            The return packet status code.

        """
        params = [length]
        params.extend(to_le_nbyte_list(addr, 4))
        evt = self.send_vs_command(
            OCF.VENDOR_SPEC.REG_READ, params=params, return_evt=True
        )

        param_lens = [4] * (length // 4)
        if not length % 4 == 0:
            param_lens.append(length % 4)
        read_data = evt.get_return_params(param_lens=param_lens)

        if print_data:
            for idx, plen in enumerate(param_lens):
                if plen == 1:
                    self.logger.info("0x%08X: 0x______%02X", addr, read_data[idx])
                elif plen == 2:
                    self.logger.info("0x%08X: 0x____%04X", addr, read_data[idx])
                elif plen == 3:
                    self.logger.info("0x%08X: 0x__%06X", addr, read_data[idx])
                else:
                    self.logger.info("0x%08X: 0x%08X", addr, read_data[idx])

                addr += 4

        return read_data, evt.status

    def set_scan_channel_map(self, channel_map: int) -> StatusCode:
        """Set the channel map used for scanning.

        Sends a vendor-specific command to the DUT, telling it to
        set the channel map used for scanning in accordance with the
        given value.

        Parameters
        ----------
        channel_map : int
            Desired channel map to use for scanning.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_SCAN_CH_MAP, params=channel_map)

    def set_event_mask_vs(self, mask: int, enable: bool) -> StatusCode:
        """Enable/disable vendor specific events the board can generate.

        Sends a vendor-specific command to the DUT, telling it to
        enable/disable vendor-specific events that can be generated
        and returned to the host in accordance with the given mask.

        Parameters
        ----------
        mask : int
            Mask indicating the vendor-specific events that should
            be enabled/disabled. Events are indicated when their
            corresponding bit is set to `1`.
        enable : bool
            If true, enables the indicated events. If false, disables
            them.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = to_le_nbyte_list(mask, 8)
        params.append(int(enable))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_EVENT_MASK, params=params)

    def set_tx_test_err_pattern(self, pattern: int) -> StatusCode:
        """Set the TX test mode error pattern.

        Sends a vendor-specific command to the DUT, telling it to
        set the pattern of errors for the TX test mode in accordance
        with the given value.

        Parameters
        ----------
        pattern : int
            Desired error pattern.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `pattern` is larger than 32 bits (4 bytes) in size.

        """

        if pattern > MAX_U32:
            raise ValueError(f"Pattern ({pattern}) too large, must be 32 bits or less.")

        params = to_le_nbyte_list(pattern, 4)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_TX_TEST_ERR_PATT, params=params)

    def set_connection_op_flags(
        self, handle: int, flags: int, enable: bool
    ) -> StatusCode:
        """Set connection operational flags.

        Sends a vendor-specific command to the DUT, telling it to
        enable/disable the connection operational flags for the
        indicated connection in accordance with the values provided.

        Parameters
        ----------
        handle : int
            The handle to the desired connection.
        flags : int
            Mask indicating the desired connection operational flags
            that should be enabled/disabled. Flags are indicated when
            their corresponding bit is set to `1`.
        enable : bool
            If true, enables the indicated flags. If false, disables
            them.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes in size.
        ValueError
            If `flags` is larger than 4 bytes in size.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )
        if byte_length(flags) > 4:
            raise ValueError(f"Flags ({flags}) is too large, must be 4 bytes or less.")

        params = to_le_nbyte_list(handle, 2)
        params.extend(to_le_nbyte_list(flags, 4))
        params.append(int(enable))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_CONN_OP_FLAGS, params=params)

    def set_256_priv_key(self, priv_key: List[int]) -> StatusCode:
        """Set/clear the P-256 private key.

        Sends a vendor-specific command to the DUT, telling it to
        set or clear the P-256 private key used to generate key
        pairs and Diffie-hellman keys in accordance with the given
        value.

        Parameters
        ----------
        priv_key : list
            Desired P-256 private key. Setting to `0` will clear
            the key.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `priv_key` is larger than 32 bytes in size.

        """
        if len(priv_key) > 32:
            raise ValueError(
                f"Private key ({priv_key}) too large, must be 32 bytes or less."
            )

        return self.send_vs_command(
            OCF.VENDOR_SPEC.SET_P256_PRIV_KEY, params=priv_key[::-1]
        )

    def get_channel_map_periodic_scan_adv(
        self, handle: int, is_advertising: bool
    ) -> Tuple[int, StatusCode]:
        """Get the channel map used for periodic scanning/advertising.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the channel map used for either periodic scanning
        or periodic advertising in accordance with the given values.

        Parameters
        ----------
        handle : int
            The handle to the desired periodic scanner/advertiser.
        is_advertising : bool
            Does the handle point to a periodic advertiser?

        Returns
        -------
        int
            The channel map returned by the DUT.
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes in size.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )

        params = to_le_nbyte_list(handle, 2)
        params.append(int(is_advertising))
        evt = self.send_vs_command(
            OCF.VENDOR_SPEC.GET_PER_CHAN_MAP, params=params, return_evt=True
        )

        return evt.get_return_params(), evt.status

    def get_acl_test_report(self) -> Tuple[TestReport, StatusCode]:
        """Get ACL test report.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the current ACL test report.

        Returns
        -------
        TestReport
            The ACL test report returned by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_ACL_TEST_REPORT, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4])

        stats = TestReport(
            rx_pkt_count=data[0],
            rx_oct_count=data[1],
            gen_pkt_count=data[2],
            gen_oct_count=data[3],
        )

        return stats, evt.status

    def set_local_num_min_used_channels(
        self, phy: PhyOption, pwr_thresh: int, min_used: int
    ) -> StatusCode:
        """Set local minimum number of used channels.

        Sends a vendor-specific command to the DUT, telling it to
        set the local minimum number of used channels in accordance
        with the given PHY, power threshold, and minimum values.

        Parameters
        ----------
        phy : PhyOption
            PHY on which the process should take place.
        pwr_thresh : int
            Power threshold for the selected PHY.
        min_used : int
            Minimum number of used channels.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `pwr_thresh` is greater than 127 or less than -127.
        ValueError
            if `min_used` is greater than 37 or less than 1.

        """
        if not -127 < pwr_thresh < 127:
            raise ValueError(
                f"Thresh ({pwr_thresh}) out of range, must be in range [-127, 127]."
            )
        if not 0 < min_used <= 37:
            raise ValueError(
                f"Min used ({min_used}) out of range, must be in range [1, 37]."
            )

        if phy == PhyOption.PHY_CODED_S2:
            phy = PhyOption.PHY_CODED

        params = [phy.value, pwr_thresh, min_used]
        return self.send_vs_command(
            OCF.VENDOR_SPEC.SET_LOCAL_MIN_USED_CHAN, params=params
        )

    def get_peer_min_num_channels_used(
        self, handle: int
    ) -> Tuple[Dict[PhyOption, int], StatusCode]:
        """Get the minimum number of channels used by a peer.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the minimum number of channels used by a peer
        device as indicated by the given value.

        Parameters
        ----------
        handle : int
            Handle to the desired peer connection.

        Returns
        -------
        Dict[PhyOption, int]
            Peer minimum number of used channels by PHY type.
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes in size.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )

        params = to_le_nbyte_list(handle, 2)
        evt = self.send_vs_command(
            OCF.VENDOR_SPEC.GET_PEER_MIN_USED_CHAN, params=params, return_evt=True
        )
        data = evt.get_return_params(param_lens=[1, 1, 1])

        min_used_map = {
            PhyOption.PHY_1M: data[0],
            PhyOption.PHY_2M: data[1],
            PhyOption.PHY_CODED: data[2],
        }

        return min_used_map, evt.status

    def set_validate_pub_key_mode(self, mode: PubKeyValidateMode) -> StatusCode:
        """Set the mode used to validate the public key.

        Sends a vendor-specific command to the DUT, telling it to
        set the mode used to validate the public key in accordance
        with the given value.

        Parameters
        ----------
        mode : PubKeyValidateMode
            Desired public key validation mode.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(
            OCF.VENDOR_SPEC.VALIDATE_PUB_KEY_MODE, params=[mode.value]
        )

    def get_rand_address(self) -> Tuple[int, StatusCode]:
        """Get a random device address.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve a random device address.

        Returns
        -------
        int
            Random device address retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_RAND_ADDR, return_evt=True)

        return evt.get_return_params(), evt.status

    def set_local_feature(self, features: int) -> StatusCode:
        """Set local supported features.

        Sends a vendor-specific command to the DUT, telling it to
        set the local supported features in accordance with the
        given value.

        Parameters
        ----------
        features : int
            Mask indicating the local supported features. Setting
            a bit to `1` will enable the indicated feature. Setting
            a bit to `0` will disable it.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `features` is larger than 64 bits (8 bytes) in size.

        """
        if features > MAX_U64:
            raise ValueError(
                f"Feature mask ({features}) is too large, must be 64 bits or less."
            )

        params = to_le_nbyte_list(features, 8)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_LOCAL_FEAT, params=params)

    def set_operational_flags(self, flags: int, enable: bool) -> StatusCode:
        """Enable/disable operational flags.

        Sends a vendor-specific command to the DUT, telling it to
        enable or disable operational flags in accordance with the
        values provided.

        Parameters
        ----------
        flags : int
            Mask indicating the desired operational flags that should
            be enabled/disabled. Flags are indicated when their
            corresponding bit is set to `1`.
        enable : bool
            If true, enables the indicated flags. If false, disabled
            them.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `flags` is larger than 32 bits (4 bytes) in size.

        """
        if flags > MAX_U32:
            raise ValueError(f"Flags ({flags}) is too large, must be 32 bits or less.")

        params = to_le_nbyte_list(flags, 4)
        params.append(int(enable))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_OP_FLAGS, params=params)

    def get_pdu_filter_stats(self) -> Tuple[PduPktStats, StatusCode]:
        """Get the accumulated PDU filter stats.

        Sends a vendor-specific command to the DUT, telling it to
        retrieves the current accumulated PDU filter statistics.

        Returns
        -------
        PduPktStats
            PDU filter statistics report returned by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_PDU_FILT_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[2] * 19)

        stats = PduPktStats(
            fail_pdu=data[0],
            pass_pdu=data[1],
            fail_whitelist=data[2],
            pass_whitelist=data[3],
            fail_peer_addr_match=data[4],
            pass_peer_addr_match=data[5],
            fail_local_addr_match=data[6],
            pass_local_addr_match=data[7],
            fail_peer_rpa_verify=data[8],
            pass_peer_rpa_verify=data[9],
            fail_local_rpa_verify=data[10],
            pass_local_rpa_verify=data[11],
            fail_peer_priv_addr=data[12],
            fail_local_priv_addr=data[13],
            fail_peer_addr_res_req=data[14],
            pass_peer_addr_res_req=data[15],
            pass_local_addr_res_opt=data[16],
            peer_res_addr_pend=data[17],
            local_res_addr_pend=data[18],
        )

        return stats, evt.status

    def set_encryption_mode(
        self, handle: int, enable: bool, nonce_mode: bool
    ) -> StatusCode:
        """Set the encryption mode of an existing connection.

        Sends a vendor-specific command to the DUT, telling it to
        set the encryption mode of the indicated connection in
        accordance with the values provided.

        Parameters
        ----------
        handle : int
            Handle to the desired connection.
        enable : bool
            Enable authentication?
        nonce_mode : bool
            Enable nonce mode?

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes in size.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )

        params = [int(enable)]
        params.append(int(nonce_mode))
        params.extend(to_le_nbyte_list(handle, 2))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_ENC_MODE, params=params)

    def set_diagnostic_mode(self, enable: bool) -> StatusCode:
        """Enable/disable diagnostic mode.

        Sends a vendor-specific command to the DUT, telling it to
        enable or disable the PAL system assert trap in accordance
        with the provided value.

        Parameters
        ----------
        enable : bool
            Enable diagnostic mode?

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_DIAG_MODE, params=int(enable))

    def enable_sniffer_packet_forwarding(self, enable: bool) -> StatusCode:
        """Enable/disable sniffer packet forwarding.

        Sends a vendor-specific command to the DUT, telling it to
        enable or disable sniffer packet forwarding in accordance
        with the value provided.

        Parameters
        ----------
        enable : bool
            Enable sniffer packet forwarding?

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        out_method = 0  # HCI through tokens, only available option
        params = [out_method, int(enable)]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_SNIFFER_ENABLE, params=params)

    def get_memory_stats(self) -> Tuple[MemPktStats, StatusCode]:
        """Get memory and system stats.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the current memory and system statistics.

        Returns
        -------
        MemPktStats
            Memory and system statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_SYS_STATS, return_evt=True)
        data = evt.get_return_params(
            param_lens=[2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        )

        stats = MemPktStats(
            stack=data[0],
            sys_assert_cnt=data[1],
            free_mem=data[2],
            used_mem=data[3],
            max_connections=data[4],
            conn_ctx_size=data[5],
            cs_watermark_lvl=data[6],
            ll_watermark_lvl=data[7],
            sch_watermark_lvl=data[8],
            lhci_watermark_lvl=data[9],
            max_adv_sets=data[10],
            adv_set_ctx_size=data[11],
            ext_scan_max=data[12],
            ext_scan_ctx_size=data[13],
            max_num_ext_init=data[14],
            ext_init_ctx_size=data[15],
            max_per_scanners=data[16],
            per_scan_ctx_size=data[17],
            max_cig=data[18],
            cig_ctx_size=data[19],
            cis_ctx_size=data[20],
        )

        return stats, evt.status

    def get_adv_stats(self) -> Tuple[AdvPktStats, StatusCode]:
        """Get the accumulated advertising stats.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the current accumulated advertising statistics.

        Returns
        -------
        AdvPktStats
            Advertising statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_ADV_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 2, 4, 4, 2, 2, 2, 2])

        stats = AdvPktStats(
            tx_adv=data[0],
            rx_req=data[1],
            rx_req_crc=data[2],
            rx_req_timeout=data[3],
            tx_resp=data[4],
            err_adv=data[5],
            rx_setup=data[6],
            tx_setup=data[7],
            rx_isr=data[8],
            tx_isr=data[9],
        )

        return stats, evt.status

    def get_scan_stats(self) -> Tuple[ScanPktStats, StatusCode]:
        """Get Scan stats

        Returns
        -------
        Tuple[ScanPktStats, StatusCode]
            Accumulated scanning stats and status code
        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_SCAN_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = ScanPktStats(
            rx_adv=data[0],
            rx_adv_crc=data[1],
            rx_adv_timeout=data[2],
            tx_req=data[3],
            rx_rsp=data[4],
            rx_rsp_crc=data[5],
            rx_rsp_timeout=data[6],
            err_scan=data[7],
            rx_setup=data[8],
            tx_setup=data[9],
            rx_isr=data[10],
            tx_isr=data[11],
        )

        return stats, evt.status

    def get_conn_stats(self) -> Tuple[DataPktStats, StatusCode]:
        """Get the stats captured during a connection.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the statistics captured during a connection.

        Returns
        -------
        DataPktStats
            Connection statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_CONN_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = DataPktStats(
            rx_data=data[0],
            rx_data_crc=data[1],
            rx_data_timeout=data[2],
            tx_data=data[3],
            err_data=data[4],
            rx_setup=data[5],
            tx_setup=data[6],
            rx_isr=data[7],
            tx_isr=data[8],
        )

        return stats, evt.status

    def get_test_stats(self) -> Tuple[DataPktStats, StatusCode]:
        """Get the stats captured during test mode.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the statistics captured during DTM.

        Returns
        -------
        DataPktStats
            Test mode statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_TEST_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = DataPktStats(
            rx_data=data[0],
            rx_data_crc=data[1],
            rx_data_timeout=data[2],
            tx_data=data[3],
            err_data=data[4],
            rx_setup=data[5],
            tx_setup=data[6],
            rx_isr=data[7],
            tx_isr=data[8],
        )

        return stats, evt.status

    def get_pool_stats(self) -> Tuple[List[PoolStats], StatusCode]:
        """Get the memory pool stats captured during runtime.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the memory pool statistics captured during runtime.

        Returns
        -------
        List[PoolStats]
            Memory pool statistics reports retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_POOL_STATS, return_evt=True)
        num_pools = evt.evt_params[0]

        param_lens = [1]
        param_lens.extend([2, 1, 1, 1, 2] * num_pools)

        data = evt.get_return_params(param_lens=param_lens, use_raw=True)

        stats = []
        num_pools = data.pop(0)
        for _ in range(num_pools):
            stats.append(
                PoolStats(
                    buf_size=data.pop(0),
                    num_buf=data.pop(0),
                    num_alloc=data.pop(0),
                    max_alloc=data.pop(0),
                    max_req_len=data.pop(0),
                )
            )

        return stats, evt.status

    def set_additional_aux_ptr_offset(self, delay: int, handle: int) -> StatusCode:
        """Set auxiliary packet offset delay.

        Sends a vendor-specific command to the DUT, telling it to
        set the auxiliary packet offset delay in accordance with
        the given values.

        Parameters
        ----------
        delay : int
            Desired delay. Set to 0 to disable.
        handle : int
            Handle to the desired connection.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `delay` is larger than 4 bytes in size.

        """
        if byte_length(delay) > 4:
            raise ValueError(f"Delay ({delay}) is too large, must be 4 bytes or less.")

        params = to_le_nbyte_list(delay, 4)
        params.append(handle)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_AUX_DELAY, params=params)

    def set_ext_adv_data_fragmentation(
        self, handle: int, frag_length: int
    ) -> StatusCode:
        """Set the extended advertising fragmentation length.

        Sends a vendor-specific command to the DUT, telling it to
        set the extended advertising fragmentation length in
        accordance with the values provided.

        Parameters
        ----------
        handle : int
            Desired advertising handle.
        frag_length : int
            Desired fragmentation length.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = [handle, frag_length]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_EXT_ADV_FRAG_LEN, params=params)

    def set_extended_advertising_phy_opts(
        self, handle: int, primary: int, secondary: int
    ) -> StatusCode:
        """Set extended advertising PHY options.

        Sends a vendor-specific command to the DUT, telling it to
        set the extended advertising PHY options in accordance with
        the values provided.

        Parameters
        ----------
        handle : int
            Desired advertising handle.
        primary : int
            Desired primary advertising channel PHY options.
        secondary : int
            Desired secondary advertising channel PHY options.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        params = [handle, primary, secondary]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_EXT_ADV_PHY_OPTS, params=params)

    def set_extended_advertising_default_phy_opts(self, phy_opts: int) -> StatusCode:
        """Set the extended advertising default TX PHY options.

        Sends a vendor-specific command to the DUT, telling it to
        set the default TX PHY options for the extended advertising
        slave primary and secondary channels in accordance with the
        value provided.

        Parameters
        ----------
        phy_opts : int
            Desired PHY options.

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(
            OCF.VENDOR_SPEC.SET_EXT_ADV_DEF_PHY_OPTS, params=phy_opts
        )

    def generate_iso_packets(
        self, handle: int, packet_len: int, num_packets: int
    ) -> StatusCode:
        """Generate ISO packets.

        Sends a vendor-specific command to the DUT, telling it to
        generate ISO packets on the indicated connection in accordance
        with the parameters provided.

        Parameters
        ----------
        handle : int
            Handle to the desired connection.
        packet_len : int
            Desired packet length.
        num_packets : int
            Number of ISO packets to send.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes in size.
        ValueError
            If `packet_len` is larger than 2 bytes in size.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )
        if byte_length(packet_len) > 2:
            raise ValueError(
                f"Packet length ({packet_len}) is too large, must be 2 bytes or less."
            )

        params = to_le_nbyte_list(handle, 2)
        params.extend(to_le_nbyte_list(packet_len, 2))
        params.append(num_packets)
        return self.send_vs_command(OCF.VENDOR_SPEC.GENERATE_ISO, params=params)

    def get_iso_test_report(self) -> Tuple[TestReport, StatusCode]:
        """Get the stats collected during an ISO test.

        Sends a vendor-specific command to the DUT, telling it to
        retrieves the statistics collected during an ISO test.

        Returns
        -------
        TestReport
            The ISO test statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_ISO_TEST_REPORT, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4])

        stats = TestReport(
            rx_pkt_count=data[0],
            rx_oct_count=data[1],
            gen_pkt_count=data[2],
            gen_oct_count=data[3],
        )

        return stats, evt.status

    def enable_iso_packet_sink(self, enable: bool) -> StatusCode:
        """Enable/disable ISO packet sink.

        Sends a vendor-specific command to the DUT, telling it to
        enable or disable ISO packet sink in accordance with the
        value provided.

        Parameters
        ----------
        enable : bool
            Enable ISO packet sink?

        Returns
        -------
        StatusCode
            The return packet status code.

        """
        return self.send_vs_command(OCF.VENDOR_SPEC.ENA_ISO_SINK, params=int(enable))

    def enable_autogen_iso_packets(self, packet_len: int) -> StatusCode:
        """Enable/disable automatic generation of ISO packets.

        Sends a vendor-specific command to the DUT, telling it to
        enable or disable the automatic generation of ISO packets
        in accordance with the values provided.

        Parameters
        ----------
        packet_len : int
            Desired ISO packet length. Set to 0 to disable automatic
            generation.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `packet_len` is larger than 32 bits (4 bytes) in size.

        """
        if packet_len > MAX_U32:
            raise ValueError(
                f"Packet length ({packet_len}) is too large, must be 4 bytes or less."
            )

        params = to_le_nbyte_list(packet_len, 4)
        return self.send_vs_command(OCF.VENDOR_SPEC.ENA_AUTO_GEN_ISO, params=params)

    def get_iso_connection_stats(self) -> Tuple[DataPktStats, StatusCode]:
        """Get the stats captured during an ISO connection.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the statistics captured during an ISO connection.

        Returns
        -------
        DataPktStats
            The ISO connection statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_ISO_TEST_REPORT, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = DataPktStats(
            rx_data=data[0],
            rx_data_crc=data[1],
            rx_data_timeout=data[2],
            tx_data=data[3],
            err_data=data[4],
            rx_setup=data[5],
            tx_setup=data[6],
            rx_isr=data[7],
            tx_isr=data[8],
        )

        return stats, evt.status

    def get_aux_adv_stats(self) -> Tuple[AdvPktStats, StatusCode]:
        """Get the accumulated auxiliary advertising stats.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the current accumulated auxiliary advertising
        statistics.

        Returns
        -------
        AdvPktStats
            The auxiliary advertising statistics report retrieved
            by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_AUX_ADV_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 2, 4, 4, 4, 2, 2, 2, 2])

        stats = AdvPktStats(
            tx_adv=data[0],
            rx_req=data[1],
            rx_req_crc=data[2],
            rx_req_timeout=data[3],
            tx_resp=data[4],
            tx_chain=data[5],
            err_adv=data[6],
            rx_setup=data[7],
            tx_setup=data[8],
            rx_isr=data[9],
            tx_isr=data[10],
        )

        return stats, evt.status

    def get_aux_scan_stats(self) -> Tuple[ScanPktStats, StatusCode]:
        """Get the accumulated auxiliary scan stats.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the current accumulated auxiliary scan statistics.

        Returns
        -------
        ScanPktStats
            The auxiliary scan statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_AUX_SCAN_STATS, return_evt=True)
        data = evt.get_return_params(
            param_lens=[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2]
        )

        stats = ScanPktStats(
            rx_adv=data[0],
            rx_adv_crc=data[1],
            rx_adv_timeout=data[2],
            tx_req=data[3],
            rx_rsp=data[4],
            rx_rsp_crc=data[5],
            rx_rsp_timeout=data[6],
            rx_chain=data[7],
            rx_chain_crc=data[8],
            rx_chain_timeout=data[9],
            err_scan=data[10],
            rx_setup=data[11],
            tx_setup=data[12],
            rx_isr=data[13],
            tx_isr=data[14],
        )
        return stats, evt.status

    def get_periodic_scanning_stats(self) -> Tuple[ScanPktStats, StatusCode]:
        """Get the accumulated periodic scanning stats.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the current accumulated periodic scanning statistics.

        Returns
        -------
        ScanPktStats
            The periodic scanning statistics report retrieved by the DUT.
        StatusCode
            The return packet status code.

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_PER_SCAN_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = ScanPktStats(
            rx_adv=data[0],
            rx_adv_crc=data[1],
            rx_adv_timeout=data[2],
            rx_chain=data[3],
            rx_chain_crc=data[4],
            rx_chain_timeout=data[5],
            err_scan=data[6],
            rx_setup=data[7],
            tx_setup=data[8],
            rx_isr=data[9],
            tx_isr=data[10],
        )
        return stats, evt.status

    def set_connection_phy_tx_power(
        self, handle: int, power: int, phy: PhyOption
    ) -> StatusCode:
        """Set the connection TX power level for a specific PHY.

        Sends a vendor-specific command to the DUT, telling it to
        set the connection TX power level for the indicated connection
        and PHY in accordance with the value provided.

        Parameters
        ----------
        handle : int
            Handle to the desired connection.
        power : int
            Desired TX power.
        phy : PhyOption
            PHY on which the TX power should be set.

        Returns
        -------
        StatusCode
            The return packet status code.

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes in size.

        """
        if byte_length(handle) > 2:
            raise ValueError(
                f"Handle ({handle}) is too large, must be 2 bytes or less."
            )

        if phy == PhyOption.PHY_CODED_S2:
            phy = PhyOption.PHY_CODED

        params = to_le_nbyte_list(handle, 2)
        params.append(power)
        params.append(phy.value)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_CONN_PHY_TX_PWR, params=params)

    def get_rssi_vs(self, channel: int = 0) -> Tuple[int, StatusCode]:
        """Get the RSSI values.

        Sends a vendor-specific command to the DUT, telling it to
        retrieve the RSSI value for the indicated channel.

        Parameters
        ----------
        channel : int, optional
            Channel for which value should be retrieved.

        Returns
        -------
        int
            RSSI value for the indicated channel.
        StatusCode
            The return packet status code.


        Raises
        ------
        ValueError
            If channel is greater than 39 or less than 0.
        """
        if not 0 <= channel < 40:
            raise ValueError(
                f"Channel out of bandwidth ({channel}), must be in range [0, 40)."
            )

        evt = self.send_vs_command(
            OCF.VENDOR_SPEC.GET_RSSI, params=channel, return_evt=True
        )
        rssi = evt.get_return_params(signed=True)

        return rssi, evt.status

    def bb_enable(self) -> StatusCode:
        """Enable the baseband radio
        NOTE: Must be done before using RSSI
        Returns
        -------
        StatusCode
        """
        return self.send_vs_command(OCF.VENDOR_SPEC.BB_EN)

    def bb_disable(self) -> StatusCode:
        """Disable the baseband radio

        Returns
        -------
        StatusCode
        """
        return self.send_vs_command(OCF.VENDOR_SPEC.BB_DIS)
