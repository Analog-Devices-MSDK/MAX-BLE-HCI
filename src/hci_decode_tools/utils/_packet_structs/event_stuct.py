# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module contains the parameter structures for HCI event packets.

This module contains definitions for the parameter structures
of all HCI event packets. As it is part of an internal package,
it is not intended for external use.

"""
from typing import Dict, List, Tuple, Union
from ...packet_codes.command import OCF, OGF
from ...packet_codes.event import EventCode, SubEventCode
from ..types import *
from ..params import HciParam, HciParamIdxRef

_EVENT_PACKET_RETURN_PARAMS: Dict[EventCode, List[HciParam]] = {
    EventCode.INQUIRY_COMPLETE: [
        HciParam("Status", 1, hci_status)
    ],
    EventCode.INQUIRY_RESULT:[
        HciParam("Num_Responses", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("BD_ADDR[{}]", 6, hci_address),
            HciParam("Page_Scan_Repetition_Mode[{}]", 1, hci_page_scan_repetition_mode),
            HciParam("Reserved[{}]", 2, hci_uint),
            HciParam("Class_Of_Device[{}]", 3, hci_uint),
            HciParam("Clock_Offset[{}]", 2, hci_clock_offset)
        ]
    ],
    EventCode.CONNECTION_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Link_Type", 1, hci_link_type),
        HciParam("Encryption_Enabled", 1, hci_bool)
    ],
    EventCode.CONNECTION_REQUEST: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Class_Of_Device", 3, hci_uint),
        HciParam("Link_Type", 1, hci_link_type)
    ],
    EventCode.DISCONNECTION_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Reason", 1, hci_status)
    ],
    EventCode.AUTHENTICATION_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint)
    ],
    EventCode.REMOTE_NAME_CHANGE_REQUEST_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Remote_Name", 248, hci_str)
    ],
    EventCode.ENCRYPTION_CHANGE_V1: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Encryption_Enabled", 1, hci_bool)
    ],
    EventCode.CHANGE_CONNECTION_LINK_KEY_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint)
    ],
    EventCode.LINK_KEY_TYPE_CHANGED: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Key_Flag", 1, hci_key_flag)
    ],
    EventCode.READ_REMOTE_SUPPORTED_FEATURES_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("LMP_Features", 8, hci_lmp_features)
    ],
    EventCode.READ_REMOTE_VERSION_INFORMATION_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Version", 1, hci_uint),
        HciParam("Company_Identifier", 2, hci_uint),
        HciParam("Subversion", 2, hci_uint)
    ],
    EventCode.QOS_SETUP_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Unused", 1, hci_uint),
        HciParam("Service_Type", 1, hci_qos_service),
        HciParam("Token_Rate", 4, hci_uint),
        HciParam("Peak_Bandwidth", 4, hci_uint),
        HciParam("Latency", 4, hci_uint),
        HciParam("Delay_Variation", 4, hci_uint)
    ],
    EventCode.COMMAND_STATUS: [
        HciParam("Status", 1, hci_status),
        HciParam("Num_HCI_Command_Packets", 1, hci_uint),
        HciParam("Command_Opcode", 2, hci_uint)
    ],
    EventCode.HARDWARE_ERROR: [
        HciParam("Hardware_Code", 1, hci_uint)
    ],
    EventCode.FLUSH_OCCURED: [
        HciParam("Handle", 2, hci_uint)
    ],
    EventCode.ROLE_CHANGE: [
        HciParam("Status", 1, hci_status),
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("New_Role", 1, hci_role)
    ],
    EventCode.NUMBER_OF_COMPLETED_PACKETS: [
        HciParam("Num_Handles", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Handle[{}]", 2, hci_uint),
            HciParam("Num_Completed_Packets[{}]", 2, hci_uint)
        ]
    ],
    EventCode.MODE_CHANGE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Current_Mode", 1, hci_bt_mode),
        HciParam("Interval", 2, hci_time_p625ms)
    ],
    EventCode.RETURN_LINK_KEYS: [
        HciParam("Num_Keys", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("BD_ADDR[{}]", 6, hci_address),
            HciParam("Link_Key[{}]", 16, hci_uint)
        ]
    ],
    EventCode.PIN_CODE_REQUEST: [
        HciParam("BD_ADDR", 6, hci_address)
    ],
    EventCode.LINK_KEY_REQUEST: [
        HciParam("BD_ADDR", 6, hci_address)
    ],
    EventCode.LINK_KEY_NOTIFICATION: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Link_Key", 16, hci_uint),
        HciParam("Key_Type", 1, hci_link_key_type)
    ],
    EventCode.LOOPBACK_COMMAND: [
        HciParam("HCI_Command_Packet", None, hci_str)
    ],
    EventCode.DATA_BUFFER_OVERFLOW: [
        HciParam("Link_Type", 1, hci_link_packet_type)
    ],
    EventCode.MAX_SLOTS_CHANGE: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("LMP_Max_Slots", 1, hci_uint)
    ],
    EventCode.READ_CLOCK_OFFSET_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Clock_Offset", 2, hci_clock_offset)
    ],
    EventCode.CONNECTION_PACKET_TYPE_CHANGED: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Packet_Type", 2, hci_packet_type)
    ],
    EventCode.QOS_VIOLATION: [
        HciParam("Handle", 2, hci_uint)
    ],
    EventCode.PAGE_SCAN_REPITITION_MODE_CHANGE: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Page_Scan_Repetition_Mode", 1, hci_page_scan_repetition_mode)
    ],
    EventCode.FLOW_SPECIFICATION_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Unused", 1, hci_uint),
        HciParam("Flow_Direction", 1, hci_datapath),
        HciParam("Service_Type", 1, hci_qos_service),
        HciParam("Token_Rate", 4, hci_uint),
        HciParam("Token_Bucket_Size", 4, hci_uint),
        HciParam("Peak_Bandwidth", 4, hci_uint),
        HciParam("Access_Latency", 4, hci_uint)
    ],
    EventCode.INQUIRY_RESULT_WITH_RSSI: [
        HciParam("Num_Responses", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("BD_ADDR[{}]", 6, hci_address),
            HciParam("Page_Scan_Repetition_Mode[{}]", 1, hci_page_scan_repetition_mode),
            HciParam("Reserved[{}]", 1, hci_uint),
            HciParam("Class_Of_Device[{}]", 3, hci_uint),
            HciParam("Clock_Offset[{}]", 2, hci_clock_offset),
            HciParam("RSSI[{}]", 1, hci_int)
        ]
    ],
    EventCode.READ_REMOTE_EXTENDED_FEATURES_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Page_Number", 1, hci_uint),
        HciParam("Max_Page_Number", 1, hci_uint),
        HciParam("Extended_LMP_Features", 8, hci_lmp_features)
    ],
    EventCode.SYNCHRONOUS_CONNECTION_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Link_Type", 1, hci_link_type),
        HciParam("Transmission_Interval", 1, hci_uint),
        HciParam("Retransmission_Window", 1, hci_uint),
        HciParam("RX_Packet_Length", 2, hci_uint),
        HciParam("TX_Packet_Length", 2, hci_uint),
        HciParam("Air_Mode", 1, hci_coding_format)
    ],
    EventCode.SYNCHRONOUS_CONNECTION_CHANGED: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Transmission_Interval", 1, hci_uint),
        HciParam("Retransmission_Window", 1, hci_uint),
        HciParam("RX_Packet_Length", 2, hci_uint),
        HciParam("TX_Packet_Length", 2, hci_uint)
    ],
    EventCode.SNIFF_SUBRATING: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Max_TX_Latency", 2, hci_time_p625ms),
        HciParam("Max_RX_Latency", 2, hci_time_p625ms),
        HciParam("Min_Remote_Timeout", 2, hci_time_p625ms),
        HciParam("Min_Local_Timeout", 2, hci_time_p625ms),
    ],
    EventCode.EXTENDED_INQUIRY_RESULT: [
        HciParam("Num_Responses", 1, hci_uint),
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Page_Scan_Repetition_Mode", 1, hci_page_scan_repetition_mode),
        HciParam("Reserved", 1, hci_uint),
        HciParam("Class_Of_Device", 3, hci_uint),
        HciParam("Clock_Offset", 2, hci_clock_offset),
        HciParam("RSSI", 1, hci_int),
        HciParam("Extended_Inquiry_Response", 240, hci_str)
    ],
    EventCode.ENCRYPTION_KEY_REFRESH_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint)
    ],
    EventCode.IO_CAPABILITY_REQUEST: [
        HciParam("BD_ADDR", 6, hci_address)
    ],
    EventCode.IO_CAPABILITY_RESPONSE: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("IO_Capability", 1, hci_io_capability),
        HciParam("OOB_Data_Present", 1, hci_bool),
        HciParam("Authentication_Requirements", 1, hci_authentication_requirements)
    ],
    EventCode.USER_CONFIRMATION_REQUEST: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Numeric_Value", 4, hci_uint)
    ],
    EventCode.USER_PASSKEY_REQUEST: [
        HciParam("BD_ADDR", 6, hci_address)
    ],
    EventCode.REMOTE_OOB_DATA_REQUEST: [
        HciParam("BD_ADDR", 6, hci_address)
    ],
    EventCode.SIMPLE_PAIRING_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("BD_ADDR", 6, hci_address)
    ],
    EventCode.LINK_SUPERVISION_TIMEOUT_CHANGED: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Link_Supervision_Timeout", 2, hci_time_p625ms)
    ],
    EventCode.ENHANCED_FLUSH_COMPLETE: [
        HciParam("Handle", 2, hci_uint)
    ],
    EventCode.USER_PASSKEY_NOTIFICATION: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Passkey", 4, hci_uint)
    ],
    EventCode.KEYPRESS_NOTIFICATION: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Notification_Type", 1, hci_keypress_notification)
    ],
    EventCode.REMOTE_HOST_SUPPORTED_FEATURES_NOTIFICATION: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Host_Supported_Features", 8, hci_lmp_features)
    ],
    EventCode.NUMBER_OF_COMPLETED_DATA_BLOCKS: [
        HciParam("Total_Num_Data_Blocks", 2, hci_uint),
        HciParam("Num_Handles", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Connection_Handle[{}]", 2, hci_uint),
            HciParam("Num_Completed_Packets[{}]", 2, hci_uint),
            HciParam("Num_Completed_Blocks[{}]", 2, hci_uint)
        ]
    ],
    EventCode.TRIGGERED_CLOCK_CAPTURE: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Which_Clock", 1, hci_clock_select),
        HciParam("Clock", 4, hci_uint),
        HciParam("Slot_Offset", 2, hci_uint)
    ],
    EventCode.SYNCHRONIZATION_TRAIN_COMPLETE: [
        HciParam("Status", 1, hci_status)
    ],
    EventCode.SYNCHRONIZATION_TRAIN_RECEIVED: [
        HciParam("Status", 1, hci_status),
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("Clock_Offset", 4, hci_uint),
        HciParam("AFH_Channel_Map", 10, hci_bt_channel_map),
        HciParam("LT_ADDR", 1, hci_uint),
        HciParam("Next_Broadcast_Instant", 4, hci_uint),
        HciParam("Connectionless_Peripheral_Broadcast_Interval", 2, hci_uint),
        HciParam("Service_Data", 1, hci_uint)
    ],
    EventCode.CONNECTIONLESS_PERIPHERAL_BROADCAST_RECEIVE: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("LT_ADDR", 1, hci_uint),
        HciParam("Clock", 4, hci_uint),
        HciParam("Offset", 4, hci_uint),
        HciParam("RX_Error", 1, hci_bool),
        HciParam("Fragment", 1, hci_fragment),
        HciParam("Data_Length", 1, hci_uint),
        HciParam("Data", HciParamIdxRef(-1), hci_uint)
    ],
    EventCode.CONNECTIONLESS_PERIPHERAL_BROADCAST_TIMEOUT: [
        HciParam("BD_ADDR", 6, hci_address),
        HciParam("LT_ADDR", 1, hci_uint)
    ],
    EventCode.TRUNCATED_PAGE_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("BD_ADDR", 6, hci_address)
    ],
    EventCode.CONNECTIONLESS_PERIPHERAL_BROADCAST_CHANNEL_MAP_CHANGE: [
        HciParam("Channel_Map", 10, hci_bt_channel_map)
    ],
    EventCode.INQUIRY_RESPONSE_NOTIFICATION: [
        HciParam("LAP", 3, hci_uint),
        HciParam("RSSI", 1, hci_int)
    ],
    EventCode.AUTHENTICATED_PAYLOAD_TIMEOUT_EXPIRED: [
        HciParam("Connection_Handle", 2, hci_uint)
    ],
    EventCode.SAM_STATUS_CHANGE: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Local_SAM_Index", 1, hci_uint),
        HciParam("Local_SAM_TX_Availability", 1, hci_uint),
        HciParam("Local_SAM_RX_Availability", 1, hci_uint),
        HciParam("Remote_SAM_Index", 1, hci_uint),
        HciParam("Remote_SAM_TX_Availability", 1, hci_uint),
        HciParam("Remote_SAM_RX_Availability", 1, hci_uint)
    ],
    EventCode.ENCRYPTION_CHANGE_V2: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Encryption_Enabled", 1, hci_bool),
        HciParam("Encryption_Key_Size", 1, hci_uint)
    ]
}

_LE_META_EVENT_RETURN_PARAMS: Dict[SubEventCode, List[HciParam]] = {
    SubEventCode.LE_CONNECTION_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Role", 1, hci_role),
        HciParam("Peer_Address_Type", 1, hci_address_type),
        HciParam("Peer_Address", 6, hci_address),
        HciParam("Connection_Interval", 2, hci_time_1p25ms),
        HciParam("Peripheral_Latency", 2, hci_uint),
        HciParam("Supervision_Timeout", 2, hci_time_10ms),
        HciParam("Central_Clock_Accuracy", 1, hci_clock_accuracy)
    ],
    SubEventCode.LE_ADVERTISING_REPORT: [
        HciParam("Num_Reports", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Event_Type[{}]", 1, hci_advertising_event_type),
            HciParam("Address_Type[{}]", 1, hci_address_type),
            HciParam("Address[{}]", 6, hci_address),
            HciParam("Data_Length[{}]", 1, hci_uint),
            HciParam("Data[{}]", HciParamIdxRef(-1), hci_str),
            HciParam("RSSI[{}]", 1, hci_int),
        ]
    ],
    SubEventCode.LE_CONNECTION_UPDATE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Connection_Interval", 2, hci_time_1p25ms),
        HciParam("Peripheral_Latency", 2, hci_uint),
        HciParam("Supervision_Timeout", 2, hci_time_10ms)
    ],
    SubEventCode.LE_READ_REMOTE_FEATURES_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("LE_Features", 8, hci_le_features)
    ],
    SubEventCode.LE_LONG_TERM_KEY_REQUEST: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Random_Number", 8, hci_uint),
        HciParam("Encrypted_Diversifier", 2, hci_uint)
    ],
    SubEventCode.LE_REMOTE_CONNECTION_PARAMETER_REQUEST: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Interval_Min", 2, hci_time_1p25ms),
        HciParam("Interval_Max",2,  hci_time_1p25ms),
        HciParam("Max_Latency", 2, hci_uint),
        HciParam("Timeout", 2, hci_time_10ms)
    ],
    SubEventCode.LE_DATA_LENGTH_CHANGE: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Max_TX_Octets", 2, hci_uint),
        HciParam("Max_TX_Time", 2, hci_uint),
        HciParam("Max_RX_Octets", 2, hci_uint),
        HciParam("Max_RX_Time", 2, hci_uint)
    ],
    SubEventCode.LE_READ_LOCAL_P256_PUBLIC_KEY_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Key_X_Coordinate", 32, hci_uint),
        HciParam("Key_Y_Coordinate", 32, hci_uint)
    ],
    SubEventCode.LE_GENERATE_DHKEY_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("DH_Key", 32, hci_uint),
    ],
    SubEventCode.LE_ENHANCED_CONNECTION_COMPLETE_V1: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Role", 1, hci_role),
        HciParam("Peer_Address_Type", 1, hci_address_type),
        HciParam("Peer_Address", 6, hci_address),
        HciParam("Local_Resolvable_Private_Address", 6, hci_address),
        HciParam("Peer_Resolvable_Private_Address", 6, hci_address),
        HciParam("Connection_Interval", 2, hci_time_1p25ms),
        HciParam("Peripheral_Latency", 2, hci_uint),
        HciParam("Supervision_Timeout", 2, hci_time_10ms),
        HciParam("Central_Clock_Accuracy", 1, hci_clock_accuracy)
    ],
    SubEventCode.LE_DIRECTED_ADVERTISING_REPORT: [
        HciParam("Num_Reports", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Event_Type[{}]", 1, hci_advertising_event_type),
            HciParam("Address_Type[{}]", 1, hci_address_type),
            HciParam("Address[{}]", 6, hci_address),
            HciParam("Direct_Address_Type[{}]", 1, hci_address_type),
            HciParam("Direct_Address[{}]", 6, hci_address),
            HciParam("RSSI[{}]", 1, hci_int)
        ]
    ],
    SubEventCode.LE_PHY_UPDATE_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("TX_PHY", 1, hci_phy_mask),
        HciParam("RX_PHY", 1, hci_phy_mask)
    ],
    SubEventCode.LE_EXTENDED_ADVERTISING_REPORT: [
        HciParam("Num_Reports", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Event_Type[{}]", 1, hci_ext_advertising_event_type),
            HciParam("Address_Type[{}]", 1, hci_address_type),
            HciParam("Address[{}]", 6, hci_address),
            HciParam("Primary_PHY[{}]", 1, hci_phy_select),
            HciParam("Secondary_PHY[{}]", 1, hci_phy_select),
            HciParam("Advertising_SID[{}]", 1, hci_uint),
            HciParam("TX_Power[{}]", 1, hci_int),
            HciParam("RSSI[{}]", 1, hci_int),
            HciParam("Periodic_Advertising_Interval[{}]", 2, hci_time_1p25ms),
            HciParam("Direct_Address_Type[{}]", 1, hci_address_type),
            HciParam("Direct_Address[{}]", 6, hci_address),
            HciParam("Data_Length[{}]", 1, hci_uint),
            HciParam("Data[{}]", HciParamIdxRef(-1), hci_str)
        ]
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_SYNC_ESTABLISHED_V1: [
        HciParam("Status", 1, hci_status),
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("Advertising_SID", 1, hci_uint),
        HciParam("Advertiser_Address_Type", 1, hci_address_type),
        HciParam("Advertiser_Address", 6, hci_address),
        HciParam("Advertiser_PHY", 1, hci_phy_select),
        HciParam("Periodic_Advertising_Interval", 2, hci_time_1p25ms),
        HciParam("Advertiser_Clock_Accuracy", 1, hci_clock_accuracy)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_REPORT_V1: [
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("TX_Power", 1, hci_int),
        HciParam("RSSI", 1, hci_int),
        HciParam("CTE_Type", 1, hci_cte_type_select),
        HciParam("Data_Status", 1, hci_data_status),
        HciParam("Data_Length", 1, hci_uint),
        HciParam("Data", HciParamIdxRef(-1), hci_str)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_SYNC_LOST: [
        HciParam("Sync_Handle", 2, hci_uint)
    ],
    SubEventCode.LE_ADVERTISING_SET_TERMINATED: [
        HciParam("Status", 1, hci_status),
        HciParam("Advertising_Handle", 1, hci_uint),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Num_Completed_Extended_Advertising_Events", 1, hci_uint)
    ],
    SubEventCode.LE_SCAN_REQUEST_RECEIVED: [
        HciParam("Advertising_Handle", 1, hci_uint),
        HciParam("Scanner_Address_Type", 1, hci_address_type),
        HciParam("Scanner_Address", 6, hci_address)
    ],
    SubEventCode.LE_CHANNEL_SELECTION_ALGORITHM: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Channel_Selection_Algorithm", 1, hci_csa_type)
    ],
    SubEventCode.LE_CONNECTIONLESS_IQ_REPORT: [
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("Channel_Index", 1, hci_uint),
        HciParam("RSSI", 2, hci_int),
        HciParam("RSSI_Antenna_ID", 1, hci_uint),
        HciParam("CTE_Type", 1, hci_cte_type_select),
        HciParam("Slot_Durations", 1, hci_uint),
        HciParam("Packet_Status", 1, hci_packet_status),
        HciParam("Periodic_Event_Counter", 2, hci_uint),
        HciParam("Sample_Count", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("I_Sample[{}]", 1, hci_int),
            HciParam("Q_Sample[{}]", 1, hci_int)
        ]
    ],
    SubEventCode.LE_CONNECTION_IQ_REPORT: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("RX_PHY", 1, hci_phy_select),
        HciParam("Data_Channel_Index", 1, hci_uint),
        HciParam("RSSI", 2, hci_int),
        HciParam("RSSI_Antenna_ID", 1, hci_uint),
        HciParam("CTE_Type", 1, hci_cte_type_select),
        HciParam("Slot_Durations", 1, hci_uint),
        HciParam("Packet_Status", 1, hci_packet_status),
        HciParam("Connection_Event_Counter", 2, hci_uint),
        HciParam("Sample_Count", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("I_Sample[{}]", 1, hci_int),
            HciParam("Q_Sample[{}]", 1, hci_int)
        ]
    ],
    SubEventCode.LE_CTE_REQUEST_FAILED: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_SYNC_TRANSFER_RECEIVED_V1: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Service_Data", 2, hci_uint),
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("Advertising_SID", 1, hci_uint),
        HciParam("Advertiser_Address_Type", 1, hci_address_type),
        HciParam("Advertiser_Address", 6, hci_address),
        HciParam("Advertiser_PHY", 1, hci_phy_select),
        HciParam("Periodic_Advertising_Interval", 2, hci_time_1p25ms),
        HciParam("Advertiser_Clock_Accuracy", 1, hci_clock_accuracy)
    ],
    SubEventCode.LE_CIS_ESTABLISHED_V1: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("CIG_Sync_Delay", 3, hci_uint),
        HciParam("CIS_Sync_Delay", 3, hci_uint),
        HciParam("Transport_Latency_C_To_P", 3, hci_uint),
        HciParam("Transport_Latency_P_To_C", 3, hci_uint),
        HciParam("PHY_C_To_P", 1, hci_phy_select),
        HciParam("PHY_P_To_C", 1, hci_phy_select),
        HciParam("NSE", 1, hci_uint),
        HciParam("BN_C_To_P", 1, hci_uint),
        HciParam("BN_P_To_C", 1, hci_uint),
        HciParam("FT_C_To_P", 1, hci_uint),
        HciParam("FT_P_To_C", 1, hci_uint),
        HciParam("Max_PDU_C_To_P", 2, hci_uint),
        HciParam("Max_PDU_P_To_C", 2, hci_uint),
        HciParam("ISO_Interval", 2, hci_time_1p25ms)
    ],
    SubEventCode.LE_CIS_REQUEST: [
        HciParam("ACL_Connection_Handle", 2, hci_uint),
        HciParam("CIS_Connection_Handle", 2, hci_uint),
        HciParam("CIG_ID", 1, hci_uint),
        HciParam("CIS_ID", 1, hci_uint)
    ],
    SubEventCode.LE_CREATE_BIG_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("BIG_Handle", 1, hci_uint),
        HciParam("BIG_Sync_Delay", 3, hci_uint),
        HciParam("Transport_Latency_BIG", 3, hci_uint),
        HciParam("PHY", 1, hci_phy_select),
        HciParam("NSE", 1, hci_uint),
        HciParam("BN", 1, hci_uint),
        HciParam("PTO", 1, hci_uint),
        HciParam("IRC", 1, hci_uint),
        HciParam("Max_PDU", 2, hci_uint),
        HciParam("ISO_Interval", 2, hci_time_1p25ms),
        HciParam("Num_BIS", 2, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Connection_Handle[{}]", 2, hci_uint)
        ]
    ],
    SubEventCode.LE_TERMINATE_BIG_COMPLETE: [
        HciParam("BIG_Handle", 1, hci_uint),
        HciParam("Reason", 1, hci_status)
    ],
    SubEventCode.LE_BIG_SYNC_ESTABLISHED: [
        HciParam("Status", 1, hci_status),
        HciParam("BIG_Handle", 1, hci_uint),
        HciParam("Transport_Latency_BIG", 3, hci_uint),
        HciParam("NSE", 1, hci_uint),
        HciParam("BN", 1, hci_uint),
        HciParam("PTO", 1, hci_uint),
        HciParam("IRC", 1, hci_uint),
        HciParam("Max_PDU", 2, hci_uint),
        HciParam("ISO_Interval", 2, hci_time_1p25ms),
        HciParam("Num_BIS", 2, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Connection_Handle[{}]", 2, hci_uint)
        ]
    ],
    SubEventCode.LE_BIG_SYNC_LOST: [
        HciParam("BIG_Handle", 1, hci_uint),
        HciParam("Reason", 1, hci_status)
    ],
    SubEventCode.LE_REQUEST_PEER_SCA_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Peer_Clock_Accuracy", 1, hci_clock_accuracy_ranged)
    ],
    SubEventCode.LE_PATH_LOSS_THRESHOLD: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Current_Path_Loss", 1, hci_uint),
        HciParam("Zone_Entered", 1, hci_path_loss_zone)
    ],
    SubEventCode.LE_TRANSMIT_POWER_REPORTING: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Reason", 1, hci_tx_power_reporting_reason),
        HciParam("PHY", 1, hci_phy_select),
        HciParam("TX_Power_Level", 1, hci_int),
        HciParam("TX_Power_Level_Flag", 1, hci_power_read_mode),
        HciParam("Delta", 1, hci_int)
    ],
    SubEventCode.LE_BIGINFO_ADVERTISING_REPORT: [
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("Num_BIS", 1, hci_uint),
        HciParam("NSE", 1, hci_uint),
        HciParam("ISO_Interval", 2, hci_uint),
        HciParam("BN", 1, hci_uint),
        HciParam("PTO", 1, hci_uint),
        HciParam("IRC", 1, hci_uint),
        HciParam("Max_PDU", 2, hci_uint),
        HciParam("SDU_Interval", 3, hci_uint),
        HciParam("Max_SDU", 2, hci_uint),
        HciParam("PHY", 1, hci_phy_select),
        HciParam("Framing", 1, hci_framing_mode),
        HciParam("Encryption", 1, hci_bool)
    ],
    SubEventCode.LE_SUBRATE_CHANGE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Subrate_Factor", 2, hci_uint),
        HciParam("Peripheral_Latency", 2, hci_uint),
        HciParam("Continuation_Number", 2, hci_uint),
        HciParam("Supervision_Timeout", 2, hci_time_10ms)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_SYNC_ESTABLISHED_V2: [
        HciParam("Status", 1, hci_status),
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("Advertising_SID", 1, hci_uint),
        HciParam("Advertiser_Address_Type", 1, hci_address_type),
        HciParam("Advertiser_Address", 6, hci_address),
        HciParam("Advertiser_PHY", 1, hci_phy_select),
        HciParam("Periodic_Advertising_Interval", 2, hci_time_1p25ms),
        HciParam("Advertiser_Clock_Accuracy", 1, hci_clock_accuracy),
        HciParam("Num_Subevents", 1, hci_uint),
        HciParam("Subevent_Interval", 1, hci_time_1p25ms),
        HciParam("Response_Slot_Delay", 1, hci_time_1p25ms),
        HciParam("Response_Slot_Spacing", 1, hci_time_p125ms)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_REPORT_V2: [
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("TX_Power", 1, hci_int),
        HciParam("RSSI", 1, hci_int),
        HciParam("CTE_Type", 1, hci_cte_type_select),
        HciParam("Periodic_Event_Counter", 2, hci_uint),
        HciParam("Subevent", 1, hci_uint),
        HciParam("Data_Status", 1, hci_data_status),
        HciParam("Data_Length", 1, hci_uint),
        HciParam("Data", HciParamIdxRef(-1), hci_str)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_SYNC_TRANSFER_RECEIVED_V2: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Service_Data", 2, hci_uint),
        HciParam("Sync_Handle", 2, hci_uint),
        HciParam("Advertising_SID", 1, hci_uint),
        HciParam("Advertiser_Address_Type", 1, hci_address_type),
        HciParam("Advertiser_Address", 6, hci_address),
        HciParam("Advertiser_PHY", 1, hci_phy_select),
        HciParam("Periodic_Advertising_Interval", 2, hci_time_1p25ms),
        HciParam("Advertiser_Clock_Accuracy", 1, hci_clock_accuracy),
        HciParam("Num_Subevents", 1, hci_uint),
        HciParam("Subevent_Interval", 1, hci_time_1p25ms),
        HciParam("Response_Slot_Delay", 1, hci_time_1p25ms),
        HciParam("Response_Slot_Spacing", 1, hci_time_p125ms)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_SUBEVENT_DATA_REQUEST: [
        HciParam("Advertising_Handle", 1, hci_uint),
        HciParam("Subevent_Start", 1, hci_uint),
        HciParam("Subevent_Data_Count", 1, hci_uint)
    ],
    SubEventCode.LE_PERIODIC_ADVERTISING_RESPONSE_REPORT: [
        HciParam("Advertising_Handle", 1, hci_uint),
        HciParam("Subevent", 1, hci_uint),
        HciParam("TX_Status", 1, hci_tx_status),
        HciParam("Num_Responses", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("TX_Power[{}]", 1, hci_int),
            HciParam("RSSI[{}]", 1, hci_int),
            HciParam("CTE_Type[{}]", 1, hci_cte_type_select),
            HciParam("Response_Slot[{}]", 1, hci_uint),
            HciParam("Data_Status[{}]", 1, hci_data_status),
            HciParam("Data_Length[{}]", 1, hci_uint),
            HciParam("Data[{}]", HciParamIdxRef(-1), hci_str)
        ]
    ],
    SubEventCode.LE_ENHANCED_CONNECTION_COMPLETE_V2: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Role", 1, hci_role),
        HciParam("Peer_Address_Type", 1, hci_address_type),
        HciParam("Peer_Address", 6, hci_address),
        HciParam("Local_Resolvable_Private_Address", 6, hci_address),
        HciParam("Peer_Resolvable_Private_Address", 6, hci_address),
        HciParam("Connection_Interval", 2, hci_time_1p25ms),
        HciParam("Peripheral_Latency", 2, hci_uint),
        HciParam("Supervision_Timeout", 2, hci_time_10ms),
        HciParam("Central_Clock_Accuracy", 1, hci_clock_accuracy),
        HciParam("Advertising_Handle", 1, hci_uint),
        HciParam("Sync_Handle", 2, hci_uint)
    ],
    SubEventCode.LE_CIS_ESTABLISHED_V2: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("CIG_Sync_Delay", 3, hci_uint),
        HciParam("CIS_Sync_Delay", 3, hci_uint),
        HciParam("Transport_Latency_C_To_P", 3, hci_uint),
        HciParam("Transport_Latency_P_To_C", 3, hci_uint),
        HciParam("PHY_C_To_P", 1, hci_phy_select),
        HciParam("PHY_P_To_C", 1, hci_phy_select),
        HciParam("NSE", 1, hci_uint),
        HciParam("BN_C_To_P", 1, hci_uint),
        HciParam("BN_P_To_C", 1, hci_uint),
        HciParam("FT_C_To_P", 1, hci_uint),
        HciParam("FT_P_To_C", 1, hci_uint),
        HciParam("Max_PDU_C_To_P", 2, hci_uint),
        HciParam("Max_PDU_P_To_C", 2, hci_uint),
        HciParam("ISO_Interval", 2, hci_time_1p25ms),
        HciParam("Sub_Interval", 3, hci_uint),
        HciParam("Max_SDU_C_To_P", 2, hci_uint),
        HciParam("Max_SDU_P_To_C", 2, hci_uint),
        HciParam("SDU_Interval_C_To_P", 3, hci_uint),
        HciParam("SDU_Interval_P_To_C", 3, hci_uint),
        HciParam("Framing", 1, hci_bool)
    ],
    SubEventCode.LE_READ_ALL_REMOTE_FEATURES_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Max_Remote_Page", 1, hci_uint),
        HciParam("Max_Valid_Page", 1, hci_uint),
        HciParam("LE_Features", 248, hci_le_features)
    ],
    SubEventCode.LE_CS_READ_REMOTE_SUPPORTED_CAPABILITIES_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Num_Config_Supported", 1, hci_uint),
        HciParam("Max_Consecutive_Procedures_Supported", 2, hci_uint),
        HciParam("Num_Antennas_Supported", 1, hci_uint),
        HciParam("Max_Antenna_Paths_Supported", 1, hci_uint),
        HciParam("Roles_Supported", 1, hci_cs_role_mask),
        HciParam("Modes_Supported", 1, hci_cs_mode),
        HciParam("RTT_Capability", 1, hci_rtt_capability),
        HciParam("RTT_AA_Only_N", 1, hci_uint),
        HciParam("RTT_Sounding_N", 1, hci_uint),
        HciParam("RTT_Random_Payload_N", 1, hci_uint),
        HciParam("NADM_Sounding_Capability", 2, hci_nadm_sounding_capability),
        HciParam("NADM_Random_Capability", 2, hci_nadm_random_capability),
        HciParam("CS_SYNC_PHYs_Supported", 1, hci_cs_sync_phy_mask),
        HciParam("Subfeatures_Supported", 2, hci_cs_subfeatures),
        HciParam("T_IP1_Times_Supported", 2, hci_cs_times),
        HciParam("T_IP2_Times_Supported", 2, hci_cs_times),
        HciParam("T_FSC_Times_Supported", 2, hci_cs_times_fcs),
        HciParam("T_PM_Times_Supported", 2, hci_cs_times),
        HciParam("T_SW_Times_Supported", 1, hci_uint),
        HciParam("TX_SNR_Capability", 1, hci_tx_snr_capability)
    ],
    SubEventCode.LE_CS_READ_REMOTE_FAE_TABLE_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Remote_FAE_Table", 72, hci_cs_channel_map)
    ],
    SubEventCode.LE_CS_SECURITY_ENABLE_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
    ],
    SubEventCode.LE_CS_CONFIG_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Config_ID", 1, hci_uint),
        HciParam("Action", 1, hci_cs_config_action),
        HciParam("Main_Mode_Type", 1, hci_uint),
        HciParam("Sub_Mode_Type", 1, hci_uint),
        HciParam("Min_Main_Mode_Steps", 1, hci_uint),
        HciParam("Max_Main_Mode_Steps", 1, hci_uint),
        HciParam("Main_Mode_Repetition", 1, hci_uint),
        HciParam("Mode_0_Steps", 1, hci_uint),
        HciParam("Role", 1, hci_cs_role_select),
        HciParam("RTT_Type", 1, hci_rtt_type),
        HciParam("CS_SYNC_PHY", 1, hci_cs_sync_phy_select),
        HciParam("Channel_Map", 10, hci_cs_channel_map),
        HciParam("Channel_Map_Repetition", 1, hci_uint),
        HciParam("Channel_Selection_Type", 1, hci_cs_csa_type),
        HciParam("Ch3c_Shape", 1, hci_cs_ch3c_shape),
        HciParam("Ch3c_Jump", 1, hci_uint),
        HciParam("Reserved", 1, hci_uint),
        HciParam("T_IP1_Time", 1, hci_uint),
        HciParam("T_IP2_Time", 1, hci_uint),
        HciParam("T_FCS_Time", 1, hci_uint),
        HciParam("T_PM_Time", 1, hci_uint)
    ],
    SubEventCode.LE_CS_PROCEDURE_ENABLE_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Config_ID", 1, hci_uint),
        HciParam("State", 1, hci_bool),
        HciParam("Tone_Antenna_Config_Selection", 1, hci_uint),
        HciParam("Selected_TX_Power", 1, hci_int),
        HciParam("Subevent_Len", 3, hci_uint),
        HciParam("Subevents_Per_Event", 1, hci_uint),
        HciParam("Subevent_Interval", 2, hci_time_p625ms),
        HciParam("Event_Interval", 2, hci_uint),
        HciParam("Procedure_Interval", 2, hci_uint),
        HciParam("Procedure_Count", 2, hci_uint),
        HciParam("Max_Procedure_Len", 2, hci_time_p625ms)
    ],
    SubEventCode.LE_CS_SUBEVENT_RESULT: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Config_ID", 1, hci_uint),
        HciParam("Start_ACL_Conn_Event_Counter", 2, hci_uint),
        HciParam("Procedure_Counter", 2, hci_uint),
        HciParam("Frequency_Compensation", 2, hci_int),
        HciParam("Reference_Power_Level", 1, hci_int),
        HciParam("Procedure_Done_Status", 1, hci_cs_procedure_done_status),
        HciParam("Subevent_Done_Status", 1, hci_cs_procedure_done_status),
        HciParam("Abort_Reason", 1, hci_cs_abort_reason),
        HciParam("Num_Antenna_Paths", 1, hci_uint),
        HciParam("Num_Steps_Reported", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Step_Mode[{}]", 1, hci_uint),
            HciParam("Step_Channel[{}]", 1, hci_uint),
            HciParam("Step_Data_Length[{}]", 1, hci_uint),
            HciParam("Step_Data[{}]", HciParamIdxRef(-1), hci_uint)
        ]
    ],
    SubEventCode.LE_CS_SUBEVENT_RESULT_CONTINUE: [
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Config_ID", 1, hci_uint),
        HciParam("Procedure_Done_Status", 1, hci_cs_procedure_done_status),
        HciParam("Subevent_Done_Status", 1, hci_cs_procedure_done_status),
        HciParam("Abort_Reason", 1, hci_cs_abort_reason),
        HciParam("Num_Antenna_Paths", 1, hci_uint),
        HciParam("Num_Steps_Reported", 1, hci_uint),
        [
            HciParamIdxRef(-1),
            HciParam("Step_Mode[{}]", 1, hci_uint),
            HciParam("Step_Channel[{}]", 1, hci_uint),
            HciParam("Step_Data_Length[{}]", 1, hci_uint),
            HciParam("Step_Data[{}]", HciParamIdxRef(-1), hci_uint)
        ]
    ],
    SubEventCode.LE_CS_TEST_END_COMPLETE: [
        HciParam("Status", 1, hci_status)
    ],
    SubEventCode.LE_MONITORED_ADVERTISERS_REPORT: [
        HciParam("Address_Type", 1, hci_address_type),
        HciParam("Address", 6, hci_address),
        HciParam("Condition", 1, hci_monitor_condition)
    ],
    SubEventCode.LE_FRAME_SPACE_UPDATE_COMPLETE: [
        HciParam("Status", 1, hci_status),
        HciParam("Connection_Handle", 2, hci_uint),
        HciParam("Initiator", 1, hci_initiator),
        HciParam("Frame_Space", 2, hci_uint),
        HciParam("PHYs", 1, hci_phy_mask),
        HciParam("Spacing_Types", 1, hci_spacing_types)
    ]
}

_COMMAND_COMPLETE_EVENT_RETURN_PARAMS: Dict[OGF, Dict[OCF, List[HciParam]]] = {
    OGF.LINK_CONTROL: {
        OCF.LINK_CONTROL.INQUIRY_CANCEL: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LINK_CONTROL.PERIODIC_INQUIRY_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LINK_CONTROL.EXIT_PERIODIC_INQUIRY_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LINK_CONTROL.CREATE_CONNECTION_CANCEL: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.LINK_KEY_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.LINK_KEY_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.PIN_CODE_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.PIN_CODE_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.REMOTE_NAME_REQUEST_CANCEL: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.READ_LMP_HANDLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("LMP_Handle", 1, hci_uint),
            HciParam("Reserved", 4, hci_uint)
        ],
        OCF.LINK_CONTROL.IO_CAPABILITY_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.USER_CONFIRMATION_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.USER_CONFIRMATION_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.USER_PASSKEY_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.USER_PASSKEY_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.REMOTE_OOB_DATA_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.REMOTE_OOB_DATA_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.IO_CAPABILITY_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.TRUNCATED_PAGE_CANCEL: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.SET_CONNECTIONLESS_PERIPHERAL_BROADCAST: [
            HciParam("Status", 1, hci_status),
            HciParam("LT_ADDR", 1, hci_uint),
            HciParam("Interval", 2, hci_uint)
        ],
        OCF.LINK_CONTROL.SET_CONNECTIONLESS_PERIPHERAL_BROADCASE_RECEIVE: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("LT_ADDR", 1, hci_uint)
        ],
        OCF.LINK_CONTROL.REMOTE_OOB_EXTENDED_DATA_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ]
    },
    OGF.LINK_POLICY: {
        OCF.LINK_POLICY.ROLE_DISCOVERY: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Current_Role", 1, hci_role)
        ],
        OCF.LINK_POLICY.READ_LINK_POLICY_SETTINGS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Link_Policy_Settings", 2, hci_link_policy_settings)
        ],
        OCF.LINK_POLICY.WRITE_LINK_POLICY_SETTINGS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LINK_POLICY.READ_DEFAULT_LINK_POLICY_SETTINGS: [
            HciParam("Status", 1, hci_status),
            HciParam("Default_Link_Policy_Settings", 2, hci_link_policy_settings)
        ],
        OCF.LINK_POLICY.WRITE_DEFAULT_LINK_POLICY_SETTINGS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LINK_POLICY.SNIFF_SUBRATING: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ]
    },
    OGF.CONTROLLER: {
        OCF.CONTROLLER.SET_EVENT_MASK: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.RESET: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_EVENT_FILTER: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.FLUSH: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.CONTROLLER.READ_PIN_TYPE: [
            HciParam("Status", 1, hci_status),
            HciParam("Fixed_PIN", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_PIN_TYPE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_STORED_LINK_KEY: [
            HciParam("Status", 1, hci_status),
            HciParam("Max_Num_Keys", 2, hci_uint),
            HciParam("Num_Keys_Read", 2, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_STORED_LINK_KEY: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Keys_Written", 1, hci_uint)
        ],
        OCF.CONTROLLER.DELETE_STORED_LINK_KEY: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Keys_Deleted", 2, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_LOCAL_NAME: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_LOCAL_NAME: [
            HciParam("Status", 1, hci_status),
            HciParam("Local_Name", 248, hci_str)
        ],
        OCF.CONTROLLER.READ_CONNECTION_ACCEPT_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Accept_Timeout", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_CONNECTION_ACCEPT_TIMEOUT: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_PAGE_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Page_Timeout", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_PAGE_TIMEOUT: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_SCAN_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Scan_Enable", 1, hci_scan_enable)
        ],
        OCF.CONTROLLER.WRITE_SCAN_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_PAGE_SCAN_ACTIVITY: [
            HciParam("Status", 1, hci_status),
            HciParam("Page_Scan_Interval", 2, hci_time_p625ms),
            HciParam("Page_Scan_Window", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_PAGE_SCAN_ACTIVITY: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_INQUIRY_SCAN_ACTIVITY: [
            HciParam("Status", 1, hci_status),
            HciParam("Page_Scan_Interval", 2, hci_time_p625ms),
            HciParam("Page_Scan_Window", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_SCAN_ACTIVITY: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_AUTHENTICATION_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Authentication_Enable", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_AUTHENTICATION_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_CLASS_OF_DEVICE: [
            HciParam("Status", 1, hci_status),
            HciParam("Class_Of_Device", 3, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_CLASS_OF_DEVICE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_VOICE_SETTING: [
            HciParam("Status", 1, hci_status),
            HciParam("Voice_Setting", 2, hci_voice_setting)
        ],
        OCF.CONTROLLER.WRITE_VOICE_SETTING: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_AUTOMATIC_FLUSH_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Flush_Timeout", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_AUTOMATIC_FLUSH_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.CONTROLLER.READ_NUM_BROADCAST_RETRANSMISSIONS: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Broadcast_Retransmissions", 1, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_NUM_BROADCAST_RETRANSMISSIONS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_HOLD_MODE_ACTIVITY: [
            HciParam("Status", 1, hci_status),
            HciParam("Hold_Mode_Activity", 1, hci_hold_mode_activity)
        ],
        OCF.CONTROLLER.WRITE_HOLD_MODE_ACTIVITY: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_TRANSMIT_POWER_LEVEL: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("TX_Power", 1, hci_int)
        ],
        OCF.CONTROLLER.READ_SYNCHRONOUS_FLOW_CONTROL_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Synchronous_Flow_Control_Enable", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_SYNCHRONOUS_FLOW_CONTROL_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_CONTROLLER_TO_HOST_FLOW_CONTROL: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.HOST_BUFFER_SIZE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_LINK_SUPERVISION_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Handle", 2, hci_uint),
            HciParam("Link_Supervision_Timeout", 1, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_LINK_SUPERVISION_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Handle", 2, hci_uint),
        ],
        OCF.CONTROLLER.READ_NUMBER_OF_SUPPORTED_IAC: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Supported_IAC", 1, hci_uint)
        ],
        OCF.CONTROLLER.READ_CURRENT_IAC_LAP: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Current_IAC", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("IAC_LAP[{}]", 3, hci_uint)
            ]
        ],
        OCF.CONTROLLER.WRITE_CURRENT_IAC_LAP: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_AFH_HOST_CHANNEL_CLASSIFICATION: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_INQUIRY_SCAN_TYPE: [
            HciParam("Status", 1, hci_status),
            HciParam("Inquiry_Scan_Type", 1, hci_scan_mode)
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_SCAN_TYPE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_INQUIRY_MODE: [
            HciParam("Status", 1, hci_status),
            HciParam("Inquiry_Mode", 1, hci_inquiry_mode)
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_PAGE_SCAN_TYPE: [
            HciParam("Status", 1, hci_status),
            HciParam("Page_Scan_Type", 1, hci_scan_mode)
        ],
        OCF.CONTROLLER.WRITE_PAGE_SCAN_TYPE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_AFH_CHANNEL_ASSESSMENT_MODE: [
            HciParam("Status", 1, hci_status),
            HciParam("AFH_Channel_Assessment_Enabled", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_AFH_CHANNEL_ASSESSMENT_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_EXTENDED_INQUIRY_RESPONSE: [
            HciParam("Status", 1, hci_status),
            HciParam("FEC_Required", 1, hci_bool),
            HciParam("Extended_Inquiry_Response", 240, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_EXTENDED_INQUIRY_RESPONSE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_SIMPLE_PAIRING_MODE: [
            HciParam("Status", 1, hci_status),
            HciParam("Simple_Pairing_Enable", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_SIMPLE_PAIRING_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_LOCAL_OOB_DATA: [
            HciParam("Status", 1, hci_status),
            HciParam("C", 16, hci_uint),
            HciParam("R", 16, hci_uint)
        ],
        OCF.CONTROLLER.READ_INQUIRY_RESPONSE_TRANSMIT_POWER_LEVEL: [
            HciParam("Status", 1, hci_status),
            HciParam("TX_Power", 1, hci_int)
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_TRANSMIT_POWER_LEVEL: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_DEFAULT_ERRONEOUS_DATA_REPORTING: [
            HciParam("Status", 1, hci_status),
            HciParam("Erroneous_Data_Reporting", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_DEFAULT_ERRONEOUS_DATA_REPORTING: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SEND_KEYPRESS_NOTIFICATION: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.CONTROLLER.SET_EVENT_MASK_PAGE_2: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_FLOW_CONTROL_MODE: [
            HciParam("Status", 1, hci_status),
            HciParam("Flow_Control_Mode", 1, hci_flow_control_mode)
        ],
        OCF.CONTROLLER.WRITE_FLOW_CONTROL_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_ENHANCED_TRANSMIT_POWER_LEVEL: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("TX_Power_Level_GFSK", 1, hci_int),
            HciParam("TX_Power_Level_DQPSK", 1, hci_int),
            HciParam("TX_Power_Level_8DPSK", 1, hci_int)
        ],
        OCF.CONTROLLER.READ_LE_HOST_SUPPORT: [
            HciParam("Status", 1, hci_status),
            HciParam("LE_Supported_Host", 1, hci_bool),
            HciParam("Unused", 1, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_LE_HOST_SUPPORT: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_MWS_CHANNEL_PARAMETERS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_EXTERNAL_FRAME_CONFIGURATION: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_MWS_SIGNALING: [
            HciParam("Status", 1, hci_status),
            HciParam("Bluetooth_RX_Priority_Assert_Offset", 2, hci_int),
            HciParam("Bluetooth_RX_Priority_Assert_Jitter", 2, hci_uint),
            HciParam("Bluetooth_RX_Priority_Deassert_Offset", 2, hci_int),
            HciParam("Bluetooth_RX_Priority_Deassert_Jitter", 2, hci_uint),
            HciParam("802_RX_Priority_Assert_Offset", 2, hci_int),
            HciParam("802_RX_Priority_Assert_Jitter", 2, hci_uint),
            HciParam("802_RX_Priority_Deassert_Offset", 2, hci_int),
            HciParam("802_RX_Priority_Deassert_Jitter", 2, hci_uint),
            HciParam("Bluetooth_TX_On_Assert_Offset", 2, hci_int),
            HciParam("Bluetooth_TX_On_Assert_Jitter", 2, hci_uint),
            HciParam("Bluetooth_TX_On_Deassert_Offset", 2, hci_int),
            HciParam("Bluetooth_TX_On_Deassert_Jitter", 2, hci_uint),
            HciParam("802_TX_On_Assert_Offset", 2, hci_int),
            HciParam("802_TX_On_Assert_Jitter", 2, hci_uint),
            HciParam("802_TX_On_Deassert_Offset", 2, hci_int),
            HciParam("802_TX_On_Deassert_Jitter", 2, hci_uint)
        ],
        OCF.CONTROLLER.SET_MWS_TRANSPORT_LAYER: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_MWS_SCAN_FREQUENCY_TABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_MWS_PATTERN_CONFIGURATION: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.SET_RESERVED_LT_ADDR: [
            HciParam("Status", 1, hci_status),
            HciParam("LT_ADDR", 1, hci_uint)
        ],
        OCF.CONTROLLER.DELETE_RESERVED_LT_ADDR: [
            HciParam("Status", 1, hci_status),
            HciParam("LT_ADDR", 1, hci_uint)
        ],
        OCF.CONTROLLER.SET_CONNECTIONLESS_PERIPHERAL_BROADCAST_DATA: [
            HciParam("Status", 1, hci_status),
            HciParam("LT_ADDR", 1, hci_uint)
        ],
        OCF.CONTROLLER.READ_SYNCHRONIZATION_TRAIN_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Sync_Train_Interval", 2, hci_uint),
            HciParam("Sync_Train_Timeout", 4, hci_uint),
            HciParam("Service_Data", 1, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_SYNCHRONIZATION_TRAIN_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Sync_Train_Interval", 2, hci_uint)
        ],
        OCF.CONTROLLER.READ_SECURE_CONNECTIONS_HOST_SUPPORT: [
            HciParam("Status", 1, hci_status),
            HciParam("Secure_Connections_Host_Support", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_SECURE_CONNECTIONS_HOST_SUPPORT: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.CONTROLLER.READ_AUTHENTICATED_PAYLOAD_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Authenticated_Payload_Timeout", 2, hci_time_10ms)
        ],
        OCF.CONTROLLER.WRITE_AUTHENTICATED_PAYLOAD_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.CONTROLLER.READ_LOCAL_OOB_EXTENDED_DATA: [
            HciParam("Status", 1, hci_status),
            HciParam("C_192", 16, hci_uint),
            HciParam("R_192", 16, hci_uint),
            HciParam("C_256", 16, hci_uint),
            HciParam("R_256", 16, hci_uint)
        ],
        OCF.CONTROLLER.READ_EXTENDED_PAGE_TIMEOUT: [
            HciParam("Status", 1, hci_status),
            HciParam("Extended_Page_Timeout", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_EXTENDED_PAGE_TIMEOUT: [
            HciParam("Status", 1, hci_status),
        ],
        OCF.CONTROLLER.READ_EXTENDED_INQUIRY_LENGTH: [
            HciParam("Status", 1, hci_status),
            HciParam("Extended_Inquiry_Length", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_EXTENDED_INQUIRY_LENGTH: [
            HciParam("Status", 1, hci_status),
        ],
        OCF.CONTROLLER.SET_ECOSYSTEM_BASE_INTERVAL: [
            HciParam("Status", 1, hci_status),
        ],
        OCF.CONTROLLER.CONFIGURE_DATA_PATH: [
            HciParam("Status", 1, hci_status),
        ],
        OCF.CONTROLLER.SET_MIN_ENCRYPTION_KEY_SIZE: [
            HciParam("Status", 1, hci_status),
        ]
    },
    OGF.INFORMATIONAL: {
        OCF.INFORMATIONAL.READ_LOCAL_VERSION_INFORMATION: [
            HciParam("Status", 1, hci_status),
            HciParam("HCI_Version", 1, hci_uint),
            HciParam("HCI_Subversion", 2, hci_uint),
            HciParam("LMP_Version", 1, hci_uint),
            HciParam("Company_Identifier", 2, hci_uint),
            HciParam("LMP_Subversion", 2, hci_uint)
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_COMMANDS: [
            HciParam("Status", 1, hci_status),
            HciParam("Supported_Commands", 64, hci_uint)
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_FEATURES: [
            HciParam("Status", 1, hci_status),
            HciParam("LMP_Features", 8, hci_lmp_features)
        ],
        OCF.INFORMATIONAL.READ_LOCAL_EXTENDED_FEATURES: [
            HciParam("Status", 1, hci_status),
            HciParam("Page_Number", 1, hci_uint),
            HciParam("Max_Page_Number", 1, hci_uint),
            HciParam("Extended_LMP_Features", 8, hci_lmp_features)
        ],
        OCF.INFORMATIONAL.READ_BUFFER_SIZE: [
            HciParam("Status", 1, hci_status),
            HciParam("ACL_Data_Packet_Length", 2, hci_uint),
            HciParam("Synchronous_Data_Packet_Length", 1, hci_uint),
            HciParam("Total_Num_ACL_Data_Packets", 2, hci_uint),
            HciParam("Total_Num_Synchronous_Data_Packets", 2, hci_uint)
        ],
        OCF.INFORMATIONAL.READ_BD_ADDR: [
            HciParam("Status", 1, hci_status),
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.INFORMATIONAL.READ_DATA_BLOCK_SIZE: [
            HciParam("Status", 1, hci_status),
            HciParam("Max_ACL_Data_Packet_Length", 2, hci_uint),
            HciParam("Data_Block_Length", 2, hci_uint),
            HciParam("Total_Num_Data_Blocks", 2, hci_uint)
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_CODECS_V1: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Supported_Standard_Codecs", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Standard_Codec_ID[{}]", 1, hci_uint)
            ],
            HciParam("Num_Supported_Vendor_Specific_Codecs", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Vendor_Specific_Codec[{}]", 4, hci_codec)
            ]
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SIMPLE_PAIRING_OPTIONS: [
            HciParam("Status", 1, hci_status),
            HciParam("Simple_Pairing_Options", 1, hci_simple_pairing_options),
            HciParam("Max_Encryption_Key_Size", 1, hci_uint)
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_CODECS_V2: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Supported_Standard_Codecs", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Standard_Codec_ID[{}]", 1, hci_uint),
                HciParam("Standard_Codec_Transport[{}]", 1, hci_codec_transport)
            ],
            HciParam("Num_Supported_Vendor_Specific_Codecs", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Vendor_Specific_Codec[{}]", 4, hci_codec),
                HciParam("Vendor_Specific_CodecTransport[{}]", 1, hci_codec_transport)
            ]
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_CODEC_CAPABILITIES: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Codec_Capabilities", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Codec_Capability_Length[{}]", 1, hci_uint),
                HciParam("Codec_Capability[{}]", HciParamIdxRef(-1), hci_uint)
            ]
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_CONTROLLER_DELAY: [
            HciParam("Status", 1, hci_status),
            HciParam("Min_Controller_Delay", 3, hci_uint),
            HciParam("Max_Controller_Delay", 3, hci_uint)
        ]
    },
    OGF.STATUS: {
        OCF.STATUS.READ_FAILED_CONTACT_COUNTER: [
            HciParam("Status", 1, hci_status),
            HciParam("Handle", 2, hci_uint),
            HciParam("Failed_Contact_Counter", 2, hci_uint)
        ],
        OCF.STATUS.RESET_FAILED_CONTACT_COUNTER: [
            HciParam("Status", 1, hci_status),
            HciParam("Handle", 2, hci_uint)
        ],
        OCF.STATUS.READ_LINK_QUALITY: [
            HciParam("Status", 1, hci_status),
            HciParam("Handle", 2, hci_uint),
            HciParam("Link_Quality", 1, hci_uint)
        ],
        OCF.STATUS.READ_RSSI: [
            HciParam("Status", 1, hci_status),
            HciParam("Handle", 2, hci_uint),
            HciParam("RSSI", 1, hci_int)
        ],
        OCF.STATUS.READ_AFH_CHANNEL_MAP: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("AFH_Mode", 1, hci_bool),
            HciParam("AFH_Channel_Map", 10, hci_bt_channel_map)
        ],
        OCF.STATUS.READ_CLOCK: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Clock", 4, hci_uint),
            HciParam("Accuracy", 2, hci_time_p3125ms)
        ],
        OCF.STATUS.READ_ENCRYPTION_KEY_SIZE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Key_Size", 1, hci_uint)
        ],
        OCF.STATUS.GET_MWS_TRANSPORT_LAYER_CONFIGURATION: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Transports", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Transport_Layer[{}]", 1, hci_mws_transport_layer),
                HciParam("Num_Baud_Rates[{}]", 1, hci_uint),
                [
                    HciParamIdxRef(-1),
                    HciParam("To_MWS_Baud_Rate[{}]", 4, hci_uint),
                    HciParam("From_MWS_Baud_Rate[{}]", 4, hci_uint)
                ]
            ]
        ],
        OCF.STATUS.SET_TRIGGERED_CLOCK_CAPTURE: [
            HciParam("Status", 1, hci_status)
        ]
    },
    OGF.TESTING: {
        OCF.TESTING.READ_LOOPBACK_MODE: [
            HciParam("Status", 1, hci_status),
            HciParam("Loopback_Mode", 1, hci_loopback_mode)
        ],
        OCF.TESTING.WRITE_LOOPBACK_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.TESTING.ENABLE_DEVICE_UNDER_TEST_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.TESTING.WRITE_SIMPLE_PAIRING_DEBUG_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.TESTING.WRITE_SECURE_CONNECTIONS_TEST_MODE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ]
    },
    OGF.LE_CONTROLLER: {
        OCF.LE_CONTROLLER.LE_SET_EVENT_MASK: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_BUFFER_SIZE_V1: [
            HciParam("Status", 1, hci_status),
            HciParam("LE_ACL_Data_Packet_Length", 2, hci_uint),
            HciParam("Total_Num_LE_ACL_Data_Packets", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_LOCAL_SUPPORTED_FEATURES: [
            HciParam("Status", 1, hci_status),
            HciParam("LE_Features", 8, hci_le_features)
        ],
        OCF.LE_CONTROLLER.LE_SET_RANDOM_ADDRESS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_PARAMETERS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_ADVERTISING_PHYSICAL_CHANNEL_TX_POWER: [
            HciParam("Status", 1, hci_status),
            HciParam("TX_Power_Level", 1, hci_int)
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_DATA: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_SCAN_RESPONSE_DATA: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_SCAN_PARAMETERS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_SCAN_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_CREATE_CONNECTION_CANCEL: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_FILTER_ACCEPT_LIST_SIZE: [
            HciParam("Status", 1, hci_status),
            HciParam("Filter_Accept_List_Size", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CLEAR_FILTER_ACCEPT_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_FILTER_ACCEPT_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_FILTER_ACCEPT_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_HOST_CHANNEL_CLASSIFICATION: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_CHANNEL_MAP: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Channel_Map", 5, hci_ble_channel_map)
        ],
        OCF.LE_CONTROLLER.LE_ENCRYPT: [
            HciParam("Status", 1, hci_status),
            HciParam("Encrypted_Data", 16, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_RAND: [
            HciParam("Status", 1, hci_status),
            HciParam("Random_Number", 8, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_LONG_TERM_KEY_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_LONG_TERM_KEY_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_SUPPORTED_STATES: [
            HciParam("Status", 1, hci_status),
            HciParam("LE_States", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_RECEIVER_TEST_V1: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V1: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_TEST_END: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Packets", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_NEGATIVE_REPLY: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_DATA_LENGTH: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_SUGGESTED_DEFAULT_DATA_LENGTH: [
            HciParam("Status", 1, hci_status),
            HciParam("Suggested_Max_TX_Octets", 2, hci_uint),
            HciParam("Suggested_Max_TX_Time", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_WRITE_SUGGESTED_DEFAULT_DATA_LENGTH: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_RESOLVING_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_RESOLVING_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_CLEAR_RESOLVING_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_RESOLVING_LIST_SIZE: [
            HciParam("Status", 1, hci_status),
            HciParam("Resolving_List_Size", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_PEER_RESOLVABLE_ADDRESS: [
            HciParam("Status", 1, hci_status),
            HciParam("Peer_Resolvable_Address", 6, hci_address)
        ],
        OCF.LE_CONTROLLER.LE_READ_LOCAL_RESOLVABLE_ADDRESS: [
            HciParam("Status", 1, hci_status),
            HciParam("Local_Resolvable_Address", 6, hci_address)
        ],
        OCF.LE_CONTROLLER.LE_SET_ADDRESS_RESOLUTION_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_RESOLVABLE_PRIVATE_ADDRESS_TIMEOUT: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_MAXIMUM_DATA_LENGTH: [
            HciParam("Status", 1, hci_status),
            HciParam("Supported_Max_TX_Octets", 2, hci_uint),
            HciParam("Supported_Max_TX_Time", 2, hci_uint),
            HciParam("Supported_Max_RX_Octets", 2, hci_uint),
            HciParam("Supported_Max_RX_Time", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_PHY: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("TX_PHY", 1, hci_phy_select),
            HciParam("RX_PHY", 1, hci_phy_select)
        ],
        OCF.LE_CONTROLLER.LE_SET_DEFAULT_PHY: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_RECEIVER_TEST_V2: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V2: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_SET_RANDOM_ADDRESS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_PARAMETERS_V1: [
            HciParam("Status", 1, hci_status),
            HciParam("Selected_TX_Power", 1, hci_int)
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_DATA: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_SCAN_RESPONSE_DATA: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_MAXIMUM_ADVERTISING_DATA_LENGTH: [
            HciParam("Status", 1, hci_status),
            HciParam("Max_Advertising_Data_Length", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_NUMBER_OF_SUPPORTED_ADVERTISING_SETS: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Supported_Advertising_Sets", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_ADVERTISING_SET: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_CLEAR_ADVERTISING_SETS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_PARAMETERS_V1: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_DATA: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_SCAN_PARAMETERS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_SCAN_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_CREATE_SYNC_CANCEL: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_TERMINATE_SYNC: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_PERIODIC_ADVERTISER_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_PERIODIC_ADVERTISER_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_CLEAR_PERIODIC_ADVERTISER_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_PERIODIC_ADVERTISER_LIST_SIZE: [
            HciParam("Status", 1, hci_status),
            HciParam("Periodic_Advertiser_List_Size", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_TRANSMIT_POWER: [
            HciParam("Status", 1, hci_status),
            HciParam("Min_TX_Power", 1, hci_int),
            HciParam("Max_TX_Power", 1, hci_int)
        ],
        OCF.LE_CONTROLLER.LE_READ_RF_PATH_COMPENSATION: [
            HciParam("Status", 1, hci_status),
            HciParam("RF_TX_Path_Compensation_Value", 2, hci_int),
            HciParam("RF_RX_Path_Compensation_Value", 2, hci_int)
        ],
        OCF.LE_CONTROLLER.LE_WRITE_RF_PATH_COMPENSATION: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_PRIVACY_MODE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_RECEIVER_TEST_V3: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V3: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTIONLESS_CTE_TRANSMIT_PARAMETERS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTIONLESS_CTE_TRANSMIT_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTIONLESS_IQ_SAMPLING_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Sync_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTION_CTE_RECEIVE_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTION_CTE_TRANSMIT_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CONNECTION_CTE_REQUEST_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CONNECTION_CTE_RESPONSE_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_ANTENNA_INFORMATION: [
            HciParam("Status", 1, hci_status),
            HciParam("Supported_Switching_Sampling_Rates", 1, hci_switching_sampling_rate),
            HciParam("Num_Antennae", 1, hci_uint),
            HciParam("Max_Switching_Pattern_Length", 1, hci_uint),
            HciParam("Max_CTE_Length", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_RECEIVE_ENABLE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_SYNC_TRANSFER: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_SET_INFO_TRANSFER: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_SYNC_TRANSFER_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_DEFAULT_PERIODIC_ADVERTISING_SYNC_TRANSFER_PARAMETERS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_MODIFY_SLEEP_CLOCK_ACCURACY: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_BUFFER_SIZE_V2: [
            HciParam("Status", 1, hci_status),
            HciParam("LE_ACL_Data_Packet_Length", 2, hci_uint),
            HciParam("Total_Num_LE_ACL_Data_Packets", 1, hci_uint),
            HciParam("ISO_Data_Packet_Length", 2, hci_uint),
            HciParam("Total_Num_ISO_Data_Packets", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_ISO_TX_SYNC: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Packet_Sequence_Number", 2, hci_uint),
            HciParam("TX_Time_Stamp", 4, hci_uint),
            HciParam("Time_Offset", 3, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_CIG_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("CIG_ID", 1, hci_uint),
            HciParam("CIS_Count", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Connection_Handle[{}]", 2, hci_uint)
            ]
        ],
        OCF.LE_CONTROLLER.LE_SET_CIG_PARAMETERS_TEST: [
            HciParam("Status", 1, hci_status),
            HciParam("CIG_ID", 1, hci_uint),
            HciParam("CIS_Count", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Connection_Handle[{}]", 2, hci_uint)
            ]
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_CIG: [
            HciParam("Status", 1, hci_status),
            HciParam("CIG_ID", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_REJECT_CIS_REQUEST: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_BIG_TERMINATE_SYNC: [
            HciParam("Status", 1, hci_status),
            HciParam("BIG_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SETUP_ISO_DATA_PATH: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_ISO_DATA_PATH: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ISO_TRANSMIT_TEST: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ISO_RECEIVE_TEST: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ISO_READ_TEST_COUNTERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Received_SDU_Count", 4, hci_uint),
            HciParam("Missed_SDU_Count", 4, hci_uint),
            HciParam("Failed_SDU_Count", 4, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ISO_TEST_END: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Received_SDU_Count", 4, hci_uint),
            HciParam("Missed_SDU_Count", 4, hci_uint),
            HciParam("Failed_SDU_Count", 4, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_HOST_FEATURE_V1: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_ISO_LINK_QUALITY: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("TX_UnACKed_Packets", 4, hci_uint),
            HciParam("TX_Flushed_Packets", 4, hci_uint),
            HciParam("TX_Last_Subevent_Packets", 4, hci_uint),
            HciParam("Retransmitted_Packets", 4, hci_uint),
            HciParam("CRC_Error_Packets", 4, hci_uint),
            HciParam("RX_Unreceived_Packets", 4, hci_uint),
            HciParam("Duplicate_Packets", 4, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ENHANCED_READ_TRANSMIT_POWER_LEVEL: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("PHY", 1, hci_phy_select),
            HciParam("Current_TX_Power_Level", 1, hci_int),
            HciParam("Max_TX_Power_Level", 1, hci_int)
        ],
        OCF.LE_CONTROLLER.LE_SET_PATH_LOSS_REPORTING_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_PATH_LOSS_REPORTING_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_TRANSMIT_POWER_REPORTING_ENABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V4: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_DATA_RELATED_ADDRESS_CHANGES: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_DEFAULT_SUBRATE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_PARAMETERS_V2: [
            HciParam("Status", 1, hci_status),
            HciParam("Selected_TX_Power", 1, hci_int)
        ],
        OCF.LE_CONTROLLER.LE_SET_DECISION_DATA: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_DECISION_INSTRUCTIONS: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_SUBEVENT_DATA: [
            HciParam("Status", 1, hci_status),
            HciParam("Advertising_Handle", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_RESPONSE_DATA: [
            HciParam("Status", 1, hci_status),
            HciParam("Sync_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_SYNC_SUBEVENT: [
            HciParam("Status", 1, hci_status),
            HciParam("Sync_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_PARAMETERS_V2: [
            HciParam("Status", 1, hci_status),
            HciParam("Advertising_Handle", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_ALL_LOCAL_SUPPORTED_FEATURES: [
            HciParam("Status", 1, hci_status),
            HciParam("Max_Page", 1, hci_uint),
            HciParam("LE_Features", 248, hci_le_features)
        ],
        OCF.LE_CONTROLLER.LE_CS_READ_LOCAL_SUPPORTED_CAPABILITIES: [
            HciParam("Status", 1, hci_status),
            HciParam("Num_Config_Supported", 1, hci_uint),
            HciParam("Max_Consecutive_Procedures_Supported", 2, hci_uint),
            HciParam("Num_Antennas_Supported", 1, hci_uint),
            HciParam("Max_Antenna_Paths_Supported", 1, hci_uint),
            HciParam("Roles_Supported", 1, hci_cs_role_mask),
            HciParam("Modes_Supported", 1, hci_cs_mode),
            HciParam("RTT_Capability", 1, hci_rtt_capability),
            HciParam("RTT_AA_Only_N", 1, hci_uint),
            HciParam("RTT_Sounding_N", 1, hci_uint),
            HciParam("RTT_Random_Payload_N", 1, hci_uint),
            HciParam("NADM_Sounding_Capability", 2, hci_nadm_sounding_capability),
            HciParam("NADM_Random_Capability", 2, hci_nadm_random_capability),
            HciParam("CS_SYNC_PHYs_Supported", 1, hci_cs_sync_phy_mask),
            HciParam("Subfeatures_Supported", 2, hci_cs_subfeatures),
            HciParam("T_IP1_Times_Supported", 2, hci_cs_times),
            HciParam("T_IP2_Times_Supported", 2, hci_cs_times),
            HciParam("T_FCS_Times_Supported", 2, hci_cs_times_fcs),
            HciParam("T_PM_Times_Supported", 2, hci_cs_times),
            HciParam("T_SW_Times_Supported", 1, hci_uint),
            HciParam("TX_SNR_Capability", 1, hci_tx_snr_capability)
        ],
        OCF.LE_CONTROLLER.LE_CS_WRITE_CACHED_REMOTE_SUPPORTED_CAPABILITIES: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CS_SET_DEFAULT_SETTINGS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CS_WRITE_CACHED_REMOTE_FAE_TABLE: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CS_SET_CHANNEL_CLASSIFICATION: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_CS_SET_PROCEDURE_PARAMETERS: [
            HciParam("Status", 1, hci_status),
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CS_TEST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_SET_HOST_FEATURE_V2: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_MONITORED_ADVERTISERS_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_MONITORED_ADVERTISERS_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_CLEAR_MONITORED_ADVERTISERS_LIST: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_READ_MONITORED_ADVERTISERS_LIST_SIZE: [
            HciParam("Status", 1, hci_status)
        ],
        OCF.LE_CONTROLLER.LE_ENABLE_MONITORING_ADVERTISERS: [
            HciParam("Status", 1, hci_status)
        ]
    }
}

def get_params(code: Union[EventCode, SubEventCode, Tuple[OGF, OCF]]) -> List[HciParam]:
    """Get packet parameter structure by code.

    Parameters
    ----------
    code : Union[EventCode, SubEventCode, Tuple[OGF, OCF]]
        Packet event code, subevent code, or OGF/OCF.

    Returns
    -------
    List[HciParam]
        Packet parameter stucture.

    """
    if isinstance(code, EventCode):
        return _EVENT_PACKET_RETURN_PARAMS.get(code, None)
    if isinstance(code, SubEventCode):
        return _LE_META_EVENT_RETURN_PARAMS.get(code, None)
    return _COMMAND_COMPLETE_EVENT_RETURN_PARAMS[code[0]].get(code[1], None)
