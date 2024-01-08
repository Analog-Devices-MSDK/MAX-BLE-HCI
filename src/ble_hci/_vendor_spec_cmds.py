from typing import Optional, Tuple, Union, Dict, List
import datetime
from ._utils import (
    _MAX_U16,
    _MAX_U32,
    _MAX_U64,
    to_le_nbyte_list,
    le_list_to_int,
    PhyOption,
    SerialUartTransport
)
from ._hci_logger import get_formatted_logger
from .data_params import (
    DataPktStats,
    ScanPktStats,
    AdvPktStats,
    MemPktStats,
    PduPktStats,
    TestReport,
    PoolStats
)
from .hci_packets import (
    AsyncPacket,
    CommandPacket,
    Endian,
    EventPacket,
    ExtendedPacket,
    _byte_length
)
from .packet_codes import EventCode, StatusCode
from .packet_defs import ADI_PORT_BAUD_RATE, OCF, OGF, PacketType, PubKeyValidateMode

class VendorSpecificCmds:
    def __init__(self, port: SerialUartTransport, logger_name: str):
        self.port = port
        self.logger = get_formatted_logger(name=logger_name)

    def send_vs_command(
            self,
            ocf: OCF,
            params: List[int] = None,
            return_evt: bool = False
    ) -> Union[EventPacket, StatusCode]:
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
        addr : Union[List[int], bytearray]
            Desired BD address.

        Returns
        -------
        EventPacket
            Object containing board return data.

        """
        params = to_le_nbyte_list(addr, 6)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_BD_ADDR, params=params)
    
    def reset_connection_stats(self) -> StatusCode:
        """Reset accumulated connection stats

        Returns
        -------
        StatusCode

        """
        return self.send_vs_command(OCF.VENDOR_SPEC.RESET_CONN_STATS)
    
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
        return self.send_vs_command(OCF.VENDOR_SPEC.GENERATE_ACL, params=int(enable))
    
    def generate_acl(
        self, handle: int, packet_len: int, num_packets: int
    ) -> StatusCode:
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
            If `handle` is larger than 2 bytes.
        ValueError
            If `packet_len` is greater than 65535.
        ValueError
            If `num_packets` is greater than 255.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")
        if num_packets > 0xFFFF:
            raise ValueError(f"Num packets too large ({num_packets}), must be 65535 or less.")
        if packet_len > 0xFF:
            raise ValueError(f"Packet length too large ({packet_len}), must be 255 or less.")

        params = to_le_nbyte_list(handle, 2)
        params.append(packet_len)
        params.extend(to_le_nbyte_list(num_packets, 2))
        return self.send_vs_command(OCF.VENDOR_SPEC.GENERATE_ACL, params=params)
    
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
        params = int(enable)
        return self.send_vs_command(OCF.VENDOR_SPEC.ENA_ACL_SINK, params=params)
        
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

        Raises
        ------
        ValueError
            If `handle` is greater than 65535.
        ValueError
            If `packet_len` is greater than 65535.
        ValueError
            If `num_packets` is greater than 255.

        """
        if not 0 <= channel < 40:
            raise ValueError(f"Channel (channel) out of bandwidth, must be in range [0, 40).")
        if packet_len > 0xFF:
            raise ValueError(f"Packet length too large ({packet_len}), must be 255 or less.")
        if num_packets > 0xFFFF:
            raise ValueError(f"Num packets too large ({num_packets}), must be 65535 or less.")


        params = [channel, packet_len, payload, phy]
        params.extend(to_le_nbyte_list(num_packets, 2))
        return self.send_vs_command(OCF.VENDOR_SPEC.TX_TEST, params=params)
    
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

        Raises
        ------
        ValueError
            If `handle` is greater than 65535.
        ValueError
            If `num_packets` is greater than 255.

        """
        if not 0 <= channel < 40:
            raise ValueError(f"Channel (channel) out of bandwidth, must be in range [0, 40).")
        if num_packets > 0xFFFF:
            raise ValueError(f"Num packets too large ({num_packets}), must be 65535 or less.")


        params = [channel, phy, modulation_idx]
        params.extend(to_le_nbyte_list(num_packets, 2))
        return self.send_vs_command(OCF.VENDOR_SPEC.RX_TEST, params=params)

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
        return self.send_vs_command(OCF.VENDOR_SPEC.RESET_TEST_STATS)
    
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
            If `tx_power` is not between -127dBm and 127dBm

        """
        if not -127 < tx_power < 127:
            raise ValueError(f"TX power ({tx_power}) out of range, must be in range [-127, 127].")

        return self.send_vs_command(OCF.VENDOR_SPEC.SET_ADV_TX_PWR, params=tx_power)
    
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
            If `handle` is larger than 2 bytes.
        ValueError
            If `tx_power` is not between -127dBm and 127dBm

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")
        if not -127 < tx_power < 127:
            raise ValueError(f"TX power ({tx_power}) out of range, must be in range [-127, 127].")

        params = to_le_nbyte_list(handle, 2)
        params.append(tx_power)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_CONN_TX_PWR, params=params)
    
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

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")

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
            self,
            addr: int,
            length: int,
            print_data: bool = False
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
        params = [length]
        params.extend(to_le_nbyte_list(addr, 4))
        evt = self.send_vs_command(OCF.VENDOR_SPEC.REG_READ, params=params, return_evt=True)

        param_lens = [4]*(length // 4)
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

        return evt.status, read_data
    
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
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_SCAN_CH_MAP, params=channel_map)
    
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
        params = to_le_nbyte_list(mask, 8)
        params.append(int(enable))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_EVENT_MASK, params=params)
    
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
            If `pattern` is larger than 32 bits.
        """

        if pattern > _MAX_U32:
            raise ValueError(f"Pattern ({pattern}) too large, must be 32 bits or less.")

        params = to_le_nbyte_list(pattern, 4)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_TX_TEST_ERR_PATT, params=params)
    
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
        
        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.
        ValueError
            If `flags` is larger than 4 bytes.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")
        if _byte_length(flags) > 4:
            raise ValueError(f"Flags ({flags}) is too large, must be 4 bytes or less.")

        params = to_le_nbyte_list(handle, 2)
        params.extend(to_le_nbyte_list(flags, 4))
        params.append(int(enable))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_CONN_OP_FLAGS, params=params)

    def set_256_priv_key(self, priv_key: int) -> StatusCode:
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
            If `priv_key` is larger than 32 bytes.
        """
        if _byte_length(priv_key) > 32:
            raise ValueError(f"Private key ({priv_key}) too large, must be 32 bytes or less.")

        params = to_le_nbyte_list(priv_key, 32)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_P256_PRIV_KEY, params=params)
    
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

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")

        params = to_le_nbyte_list(handle, 2)
        params.append(int(is_advertising))
        evt = self.send_vs_command(
            OCF.VENDOR_SPEC.GET_PER_CHAN_MAP, params=params, return_evt=True)
        
        return evt.status, evt.get_return_params()
    
    def get_acl_test_report(self) -> Tuple[TestReport, StatusCode]:
        """Get ACL Test Report

        Returns
        -------
        Dict[str, int]
            ACL Test Report

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_ACL_TEST_REPORT)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4])

        stats = TestReport(
            rx_pkt_count=data[0],
            rx_oct_count=data[1],
            gen_pkt_count=data[2],
            gen_oct_count=data[3]
        )

        return stats, evt.status
    
    def set_local_num_min_used_channels(
        self, phy: PhyOption, pwr_thresh: int, min_used: int
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
            If `min_used` is not in range [1, 37].
        ValueError
            If `pwr_thresh` is not in range [-127, 127].

        """
        if not -127 < pwr_thresh < 127:
            raise ValueError(f"Thresh ({pwr_thresh}) out of range, must be in range [-127, 127].")
        if not 0 < min_used <= 37:
            raise ValueError(f"Min used ({min_used}) out of range, must be in range [1, 37].")

        params = [phy.value, pwr_thresh, min_used]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_LOCAL_MIN_USED_CHAN, params=params)
    
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

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")

        params = to_le_nbyte_list(handle, 2)
        evt = self.send_vs_command(
            OCF.VENDOR_SPEC.GET_PEER_MIN_USED_CHAN, params=params, return_evt=True)
        data = evt.get_return_params(param_lens=[1, 1, 1])

        min_used_map = {
            PhyOption.P1M: data[0],
            PhyOption.P2M: data[1],
            PhyOption.PCODED: data[2]
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
        return self.send_vs_command(OCF.VENDOR_SPEC.VALIDATE_PUB_KEY_MODE, params=[mode.value])
    
    def get_rand_address(self) -> Tuple[int, StatusCode]:
        """Gets a randomly generated address

        Returns
        -------
        List[int]
            6 Byte address

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_RAND_ADDR, return_evt=True)
        return evt.get_return_params(), evt.status
    
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
            If `features` is greater than 2^64.

        """
        if features > 2**64:
            raise ValueError(f"Feature mask ({features}) is too large, must be 64 bits or less.")

        params = to_le_nbyte_list(features, 8)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_LOCAL_FEAT, params=params)
    
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
            If `flags` is larger than 32 bits.

        """
        if flags > _MAX_U32:
            raise ValueError(f"Flags ({flags}) is too large, must be 32 bits or less.")

        params = to_le_nbyte_list(flags, 4)
        params.append(int(enable))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_OP_FLAGS, params=params)
    
    def get_pdu_filter_stats(self) -> Tuple[PduPktStats, StatusCode]:
        """Get PDU Filter Stats

        Returns
        -------
        Dict[str, int]
            Filter stats

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_PDU_FILT_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[2]*19)

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
            fail_peer_priv_addr=data[10],
            pass_peer_priv_addr=data[11],
            fail_local_priv_addr=data[12],
            pass_local_priv_addr=data[13],
            fail_peer_addr_res_req=data[14],
            pass_peer_addr_res_req=data[15],
            pass_local_addr_res_opt=data[16],
            peer_res_addr_pend=data[17],
            local_res_addr_pend=data[18]
        )

        return stats, evt.status
    
    def set_encryption_mode(
        self, handle: int, enable: bool, nonce_mode: bool
    ) -> StatusCode:
        """Set encryption mode

        Parameters
        ----------
        handle : int
            handle to connection
        enable : bool
            True to enable, False to disable
        nonce_mode : bool
            True for Noonce mode, False otherwise

        Returns
        -------
        EventCode

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")

        params = to_le_nbyte_list(handle, 2)
        params.append(int(enable))
        params.append(int(nonce_mode))
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_ENC_MODE, params=params)
    
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
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_DIAG_MODE, params=int(enable))
    
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
        out_method = 0 # HCI through tokens, only available option
        params = [out_method, int(enable)]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_SNIFFER_ENABLE, params=params)

    def get_memory_stats(self) -> Tuple[MemPktStats, StatusCode]:
        """Get memory use stats

        Returns
        -------
        Dict[str, int]
            Memory use stats

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_SYS_STATS, return_evt=True)
        data = evt.get_return_params(
            param_lens=[2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        
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
            exit_init_ctx_size=data[15],
            max_per_scanners=data[16],
            per_scan_ctx_size=data[17],
            max_cig=data[18],
            cig_ctx_size=data[19],
            cis_ctx_size=data[20]
        )

        return stats, evt.status
    
    def get_adv_stats(self) -> Tuple[AdvPktStats, StatusCode]:
        """Get advertising stats

        Returns
        -------
        Dict[str, int]
            Advertising stats

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
            tx_isr=data[9]
        )

        return stats, evt.status
    
    def get_conn_stats(self) -> Tuple[DataPktStats, StatusCode]:
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
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_CONN_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = DataPktStats(
            rx_data=data[0],
            rx_data_crc=data[1],
            rx_timeout=data[2],
            tx_data=data[3],
            err_data=data[4],
            rx_setup=data[5],
            tx_setup=data[6],
            rx_isr=data[7],
            tx_isr=data[8]
        )

        return stats, evt.status
    
    def get_test_stats(self) -> Tuple[DataPktStats, StatusCode]:
        """Get test stats

        Returns
        -------
        Dict[str, int]
            Test stats

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_TEST_STATS, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4, 4, 2, 2, 2, 2])

        stats = DataPktStats(
            rx_data=data[0],
            rx_data_crc=data[1],
            rx_timeout=data[2],
            tx_data=data[3],
            err_data=data[4],
            rx_setup=data[5],
            tx_setup=data[6],
            rx_isr=data[7],
            tx_isr=data[8]
        )

        return stats, evt.status
    
    def get_pool_stats(self) -> Tuple[List[PoolStats], StatusCode]:
        """Get memory pool stats

        Returns
        -------
        Dict[str, int]
            memory pool stats

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_POOL_STATS, return_evt=True)
        num_pools = evt.evt_params[0]

        param_lens = [1]
        param_lens.extend([2, 1, 1, 1, 2]*num_pools)

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
                    max_req_len=data.pop(0)
                )
            )

        return stats, evt.status
    
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

        Raises
        ------
        ValueError
            If `delay` is larger than 4 bytes.

        """
        if _byte_length(delay) > 4:
            raise ValueError(f"Delay ({delay}) is too large, must be 4 bytes or less.")

        params = to_le_nbyte_list(delay, 4)
        params.append(handle)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_AUX_DELAY, params=params)

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

        Returns
        -------
        EventCode

        """
        params = [handle, frag_length]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_EXT_ADV_FRAG_LEN, params=params)
    
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
        params = [handle, primary, secondary]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_EXT_ADV_DEF_PHY_OPTS, params=params)

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
        params = [handle, primary, secondary]
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_EXT_ADV_DEF_PHY_OPTS, params=params)
    
    def generate_iso_packets(
        self, handle: int, packet_len: int, num_packets: int
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

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.
        ValueError
            If `packet_len` is larger than 2 bytes.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")
        if _byte_length(packet_len) > 2:
            raise ValueError(
                f"Packet length ({packet_len}) is too large, must be 2 bytes or less.")

        params = to_le_nbyte_list(handle, 2)
        params.extend(to_le_nbyte_list(packet_len, 2))
        params.append(num_packets)
        return self.send_vs_command(OCF.VENDOR_SPEC.GENERATE_ISO, params=params)

    def get_iso_test_report(self) -> Tuple[TestReport, StatusCode]:
        """Get ISO test report

        Returns
        -------
        Dict[str, int]
            ISO test report

        """
        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_ISO_TEST_REPORT, return_evt=True)
        data = evt.get_return_params(param_lens=[4, 4, 4, 4])

        stats = TestReport(
            rx_pkt_count=data[0],
            rx_oct_count=data[1],
            gen_pkt_count=data[2],
            gen_oct_count=data[3]
        )
        
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
        return self.send_vs_command(OCF.VENDOR_SPEC.ENA_ISO_SINK, params=int(enable))
    
    def enable_autogen_iso_packets(self, packet_len: int) -> StatusCode:
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
            If `packet_len` is larger than 4 bytes.

        """
        if packet_len > _MAX_U32:
            raise ValueError(
                f"Packet length ({packet_len}) is too large, must be 4 bytes or less.")
        
        params = to_le_nbyte_list(packet_len, 4)
        return self.send_vs_command(OCF.VENDOR_SPEC.ENA_AUTO_GEN_ISO, params=params)
    
    def get_iso_connection_stats(self) -> Tuple[DataPktStats, StatusCode]:
        """Get ISO connection stats

        Returns
        -------
        Dict[str, int]
            ISO connection stats
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
            tx_isr=data[8]
        )

        return stats, evt.status
    
    def get_aux_adv_stats(self) -> Tuple[AdvPktStats, StatusCode]:
        """Get auxillary advertising stats

        Returns
        -------
        Dict[str, int]
            AUX adv stats

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
            tx_isr=data[10]
        )

        return stats, evt.status
    
    def get_aux_scan_stats(self) -> Tuple[ScanPktStats, StatusCode]:
        """Get auxillary scanning stats

        Returns
        -------
        Dict[str, int]
            Aux scan stats

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
            tx_isr=data[14]
        )
        return stats, evt.status
    
    def get_periodic_scanning_stats(self) -> Tuple[ScanPktStats, StatusCode]:
        """Get periodic scanning stats

        Returns
        -------
        Dict[str, int]
            Periodic scanning stats

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
            tx_isr=data[10]
        )
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

        Raises
        ------
        ValueError
            If `handle` is larger than 2 bytes.

        """
        if _byte_length(handle) > 2:
            raise ValueError(f"Handle ({handle}) is too large, must be 2 bytes or less.")

        params = to_le_nbyte_list(handle, 2)
        params.append(power)
        params.append(phy.value)
        return self.send_vs_command(OCF.VENDOR_SPEC.SET_CONN_PHY_TX_PWR, params=params)
    
    def get_rssi_vs(self, channel: int = 0):
        if channel > 39:
            raise ValueError("Channel must be between 0-39")

        evt = self.send_vs_command(OCF.VENDOR_SPEC.GET_RSSI, params=channel, return_evt=True)
        rssi = evt.get_return_params(signed=True)

        return rssi, evt.status
