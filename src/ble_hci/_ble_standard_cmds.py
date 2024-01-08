"""DOCSTRING"""
from typing import Optional, Tuple, Union, List
from ._utils import to_le_nbyte_list, SerialUartTransport, PhyOption
from ._hci_logger import get_formatted_logger
from .data_params import AdvParams, ConnParams, ScanParams
from .hci_packets import CommandPacket, EventPacket
from .packet_codes import StatusCode
from .packet_defs import OCF, OGF


class BleStandardCmds:
    """DOCSTRING"""

    def __init__(self, port: SerialUartTransport, logger_name: str):
        self.port = port
        self.logger = get_formatted_logger(name=logger_name)

    def send_le_controller_command(
        self, ocf: OCF, params: List[int] = None, return_evt: bool = False
    ) -> Union[StatusCode, EventPacket]:
        """DOCSTRING"""
        cmd = CommandPacket(OGF.LE_CONTROLLER, ocf, params=params)
        if return_evt:
            return self.port.send_command(cmd)

        return self.port.send_command(cmd).status

    def send_link_control_command(
        self, ocf: OCF, params: List[int] = None, return_evt: bool = False
    ) -> Union[StatusCode, EventPacket]:
        """DOCSTRING"""
        cmd = CommandPacket(OGF.LINK_CONTROL, ocf, params=params)
        if return_evt:
            return self.port.send_command(cmd)

        return self.port.send_command(cmd).status

    def send_controller_command(
        self, ocf: OCF, params: List[int] = None, return_evt: bool = False
    ) -> Union[StatusCode, EventPacket]:
        """DOCSTRING"""
        cmd = CommandPacket(OGF.CONTROLLER, ocf, params=params)
        if return_evt:
            return self.port.send_command(cmd)

        return self.port.send_command(cmd).status

    def set_adv_params(self, adv_params: AdvParams = AdvParams()) -> StatusCode:
        """DOCSTRING"""
        params = [
            adv_params.interval_min,  # Advertising Interval Min.
            adv_params.interval_max,  # Advertising Interval Max.
            adv_params.adv_type,  # Advertisiing Type
            adv_params.own_addr_type,  # Own Address Type
            adv_params.peer_addr_type,  # Peer Address Type
            0x0,
            0x0,
            0x0,
            0x0,
            0x0,
            adv_params.peer_addr,  # Peer Address
            adv_params.channel_map,  # Advertising Channel Map
            adv_params.filter_policy,  # Advertising Filter Policy
        ]

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_ADV_PARAM, params=params
        )

    def enable_adv(self, enable: bool) -> StatusCode:
        """DOCSTRING"""
        return self.send_le_controller_command(OCF.LE_CONTROLLER, params=int(enable))

    def enable_scanning(
        self, enable: bool, filter_duplicates: bool = False
    ) -> StatusCode:
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
        params = [int(enable), int(filter_duplicates)]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_SCAN_ENABLE, params=params
        )

    def set_scan_params(self, scan_params: ScanParams) -> StatusCode:
        """Set parameters used for scanning

        Parameters
        ----------
        scan_params : ScanParams
            Scan paramters used for scanning

        Returns
        -------
        StatusCode

        """
        params = [scan_params.scan_type]
        params.extend(to_le_nbyte_list(scan_params.scan_interval, 2))
        params.extend(to_le_nbyte_list(scan_params.scan_window, 2))
        params.append(scan_params.addr_type)
        params.append(scan_params.filter_policy)

        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_SCAN_PARAM, params=params
        )

    def create_connection(self, conn_params: ConnParams) -> StatusCode:
        """Create a connection to peer device

        Parameters
        ----------
        conn_params : ConnParams
            Parameters to attempt connection with

        Returns
        -------
        StatusCode

        """
        params = to_le_nbyte_list(conn_params.scan_interval, 2)
        params.extend(to_le_nbyte_list(conn_params.scan_window, 2))
        params.append(conn_params.init_filter_policy)
        params.append(conn_params.peer_addr_type)
        params.extend(to_le_nbyte_list(conn_params.peer_addr, 6))
        params.append(conn_params.own_addr_type)
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
        """Set the default PHY used for tx, rx, or both

        Parameters
        ----------
        all_phys : int, optional
            Default PHY for both TX and RX, by default 0x0
        tx_phys : int, optional
            Default TX PHY, by default 0x7
        rx_phys : int, optional
            Default RX PHY, by default 0x7

        Returns
        -------
        StatusCode

        """
        params = [all_phys, tx_phys, rx_phys]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_DEF_PHY, params=params
        )

    def set_data_len(
        self, handle: int = 0x0000, tx_octets: int = 0xFB00, tx_time: int = 0x9042
    ) -> StatusCode:
        """Command board to set data length to the max value.

        Sends a command to the board, telling it to set its internal
        data length parameter to the maximum value.

        Returns
        -------
        Event
            Object containing board return data.

        """
        params = to_le_nbyte_list(handle, 2)
        params.extend(to_le_nbyte_list(tx_octets, 2))
        params.extend(to_le_nbyte_list(tx_time, 2))
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_DATA_LEN, params=params
        )

    def set_phy(
        self, phy: PhyOption = PhyOption.PHY_1M, handle: int = 0x0000
    ) -> StatusCode:
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
        params = to_le_nbyte_list(handle, 2)
        params.append(0x0)
        if phy == PhyOption.PHY_1M:
            params.append(0x0)
            params.append(0x0)
            params.extend(to_le_nbyte_list(0x0, 2))
        elif phy == PhyOption.PHY_2M:
            params.append(0x2)
            params.append(0x2)
            params.extend(to_le_nbyte_list(0x0, 2))
        elif phy == PhyOption.PHY_CODED_S8:
            params.append(0x4)
            params.append(0x4)
            params.extend(to_le_nbyte_list(0x2, 2))
        elif phy == PhyOption.PHY_CODED_S2:
            params.append(0x4)
            params.append(0x4)
            params.extend(to_le_nbyte_list(0x1, 2))
        else:
            self.logger.warning(
                "Invalid PHY selection (%s), defaulting to PHY_1M.", phy
            )

        return self.send_le_controller_command(OCF.LE_CONTROLLER.SET_PHY, params=params)

    def tx_test(
        self,
        channel: int = 0,
        phy: PhyOption = PhyOption.PHY_1M,
        payload: int = 0,
        packet_len: int = 0,
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
        params = [channel, packet_len, payload, phy.value]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.ENHANCED_TRANSMITTER_TEST, params=params
        )

    def rx_test(
        self,
        channel: int = 0,
        phy: PhyOption = PhyOption.PHY_1M,
        modulation_idx: float = 0,
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
        if phy == PhyOption.PHY_CODED_S2:
            phy = PhyOption.PHY_CODED_S8

        params = [channel, phy.value, modulation_idx]
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.ENHANCED_RECEIVER_TEST, params=params
        )

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
        evt = self.send_le_controller_command(
            OCF.LE_CONTROLLER.TEST_END, return_evt=True
        )
        rx_ok = evt.get_return_params()

        return rx_ok

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
        params = to_le_nbyte_list(handle, 2)
        params.append(reason)
        return self.send_link_control_command(
            OCF.LINK_CONTROL.DISCONNECT, params=params
        )

    def reset(self) -> StatusCode:
        """Sets log level.
        Resets the controller

        Returns
        ----------
        Event: EventPacket

        """
        return self.send_controller_command(OCF.CONTROLLER.RESET)

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
        params = to_le_nbyte_list(mask, 8)
        return self.send_le_controller_command(
            OCF.LE_CONTROLLER.SET_EVENT_MASK, params=params
        )
