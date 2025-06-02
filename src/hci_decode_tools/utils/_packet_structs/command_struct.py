# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module contains the parameter structures for HCI command packets.

This module contains definitions for the parameter structures
of all HCI command packets. As it is part of an internal
package, it is not intended for external use.

"""
# pylint: disable=wildcard-import, too-many-lines, unused-wildcard-import
from typing import Dict, List
from ...packet_codes.command import OCF, OGF
from ..types import *
from ..params import HciParam, HciParamIdxRef

_COMMAND_PACKET_PARAMS: Dict[OGF, Dict[OCF, List[HciParam]]] = {
    OGF.LINK_CONTROL: {
        OCF.LINK_CONTROL.INQUIRY: [
            HciParam("LAP", 3, hci_uint),
            HciParam("Inquiry_Length", 1, hci_time_1p28s),
            HciParam("Num_Responses", 1, hci_uint),
        ],
        OCF.LINK_CONTROL.PERIODIC_INQUIRY_MODE: [
            HciParam("Max_Period_Length", 2, hci_time_1p28s),
            HciParam("Min_Period_Length", 2, hci_time_1p28s),
            HciParam("LAP", 3, hci_uint),
            HciParam("Inquiry_Length", 1, hci_time_1p28s),
            HciParam("Num_Responses", 1, hci_uint),
        ],
        OCF.LINK_CONTROL.CREATE_CONNECTION: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Packet_Type", 2, hci_packet_type),
            HciParam("Page_Scan_Repitition_Mode", 1, hci_page_scan_repetition_mode),
            HciParam("Reserved", 1, hci_uint),
            HciParam("Clock_Offset", 2, hci_clock_offset),
            HciParam("Allow_Role_Switch", 1, hci_bool),
        ],
        OCF.LINK_CONTROL.DISCONNECT: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Reason", 1, hci_status),
        ],
        OCF.LINK_CONTROL.CREATE_CONNECTION_CANCEL: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.ACCEPT_CONNECTION_REQUEST: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Role", 1, hci_role),
        ],
        OCF.LINK_CONTROL.REJECT_CONNECTION_REQUEST: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Reason", 1, hci_status),
        ],
        OCF.LINK_CONTROL.LINK_KEY_REQUEST_REPLY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Link_Key", 16, hci_uint),
        ],
        OCF.LINK_CONTROL.LINK_KEY_REQUEST_NEGATIVE_REPLY: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.PIN_CODE_REQUEST_REPLY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("PIN_Code_Length", 1, hci_uint),
            HciParam("PIN_Code", 16, hci_str),
        ],
        OCF.LINK_CONTROL.PIN_CODE_REQUEST_NEGATIVE_REPLY: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.CHANGE_CONNECTION_PACKET_TYPE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Packet_Type", 2, hci_packet_type),
        ],
        OCF.LINK_CONTROL.AUTHENTICATION_REQUEST: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LINK_CONTROL.SET_CONNECTION_ENCRYPTION: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Encryption_Enable", 1, hci_bool),
        ],
        OCF.LINK_CONTROL.CHANGE_CONNECTION_LINK_KEY: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LINK_CONTROL.LINK_KEY_SELECTION: [HciParam("Key_Flag", 1, hci_key_flag)],
        OCF.LINK_CONTROL.REMOTE_NAME_REQUEST: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Page_Scan_Repitition_Mode", 1, hci_page_scan_repetition_mode),
            HciParam("Reserved", 1, hci_uint),
            HciParam("Clock_Offset", 2, hci_clock_offset),
        ],
        OCF.LINK_CONTROL.REMOTE_NAME_REQUEST_CANCEL: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.READ_REMOTE_SUPPORTED_FEATURES: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LINK_CONTROL.READ_REMOTE_EXTENDED_FEATURES: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Page_Number", 1, hci_uint),
        ],
        OCF.LINK_CONTROL.READ_REMOTE_VERSION_INFORMATION: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LINK_CONTROL.READ_CLOCK_OFFSET: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LINK_CONTROL.READ_LMP_HANDLE: [HciParam("Connection_Handle", 2, hci_uint)],
        OCF.LINK_CONTROL.SETUP_SYNCHRONOUS_CONNECTION: [
            # DIFF PKT TYPE
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Transmit_Bandwidth", 4, hci_uint),
            HciParam("Receive_Bandwidth", 4, hci_uint),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Voice_Setting", 2, hci_voice_setting),
            HciParam("Retransmission_Effort", 1, hci_retransmission_effort),
            HciParam("Packet_Type", 2, hci_sync_packet_type),
        ],
        OCF.LINK_CONTROL.ACCEPT_SYNCHRONOUS_CONNECTION_REQUEST: [
            # DIFF PKT TYPE
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Transmit_Bandwidth", 4, hci_uint),
            HciParam("Receive_Bandwidth", 4, hci_uint),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Voice_Setting", 2, hci_voice_setting),
            HciParam("Retransmission_Effort", 1, hci_retransmission_effort),
            HciParam("Packet_Type", 2, hci_sync_packet_type),
        ],
        OCF.LINK_CONTROL.REJECT_SYNCHRONOUS_CONNECTION_REQUEST: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Reason", 1, hci_status),
        ],
        OCF.LINK_CONTROL.IO_CAPABILITY_REQUEST_REPLY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("IO_Capability", 1, hci_io_capability),
            HciParam("OOB_Data_Present", 1, hci_oob_data_present),
            HciParam("Authentication_Requirements", 1, hci_authentication_requirements),
        ],
        OCF.LINK_CONTROL.USER_CONFIRMATION_REQUEST_REPLY: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.USER_CONFIRMATION_REQUEST_NEGATIVE_REPLY: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.USER_PASSKEY_REQUEST_REPLY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Numeric_Value", 4, hci_uint),
        ],
        OCF.LINK_CONTROL.USER_PASSKEY_REQUEST_NEGATIVE_REPLY: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.REMOTE_OOB_DATA_REQUEST_REPLY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("C", 16, hci_uint),
            HciParam("R", 16, hci_uint),
        ],
        OCF.LINK_CONTROL.REMOTE_OOB_DATA_REQUEST_NEGATIVE_REPLY: [
            HciParam("BD_ADDR", 6, hci_address)
        ],
        OCF.LINK_CONTROL.IO_CAPABILITY_REQUEST_NEGATIVE_REPLY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Reason", 1, hci_status),
        ],
        OCF.LINK_CONTROL.ENHANCED_SETUP_SYNCHRONOUS_CONNECTION: [
            # DIFF PKT TYPE
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Transmit_Bandwidth", 4, hci_uint),
            HciParam("Receive_Bandwidth", 4, hci_uint),
            HciParam("Transmit_Coding_Format", 5, hci_codec),
            HciParam("Receive_Coding_Format", 5, hci_codec),
            HciParam("Transmit_Codec_Frame_Size", 2, hci_uint),
            HciParam("Receive_Codec_Frame_Size", 2, hci_uint),
            HciParam("Input_Bandwidth", 4, hci_uint),
            HciParam("Output_Bandwidth", 4, hci_uint),
            HciParam("Input_Coding_Format", 5, hci_codec),
            HciParam("Output_Coding_Format", 5, hci_codec),
            HciParam("Input_Coded_Data_Size", 2, hci_uint),
            HciParam("Output_Coded_Data_Size", 2, hci_uint),
            HciParam("Input_PCM_Data_Format", 1, hci_pcm_data_format),
            HciParam("Output_PCM_Data_Format", 1, hci_pcm_data_format),
            HciParam("Input_PCM_Sample_Payload_MSB_Position", 1, hci_uint),
            HciParam("Output_PCM_Sample_Payload_MSB_Position", 1, hci_uint),
            HciParam("Input_Data_Path", 1, hci_uint),
            HciParam("Output_Data_Path", 1, hci_uint),
            HciParam("Input_Transport_Unit_Size", 1, hci_uint),
            HciParam("Output_Transport_Unit_Size", 1, hci_uint),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Packet_Type", 2, hci_sync_packet_type),
            HciParam("Retransmission_Effort", 1, hci_retransmission_effort),
        ],
        OCF.LINK_CONTROL.ENHANCED_ACCEPT_SYNCHRONOUS_CONNECTION_REQUEST: [
            # DIFF PKT TYPE
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Transmit_Bandwidth", 4, hci_uint),
            HciParam("Receive_Bandwidth", 4, hci_uint),
            HciParam("Transmit_Coding_Format", 5, hci_codec),
            HciParam("Receive_Coding_Format", 5, hci_codec),
            HciParam("Transmit_Codec_Frame_Size", 2, hci_uint),
            HciParam("Receive_Codec_Frame_Size", 2, hci_uint),
            HciParam("Input_Bandwidth", 4, hci_uint),
            HciParam("Output_Bandwidth", 4, hci_uint),
            HciParam("Input_Coding_Format", 5, hci_codec),
            HciParam("Output_Coding_Format", 5, hci_codec),
            HciParam("Input_Coded_Data_Size", 2, hci_uint),
            HciParam("Output_Coded_Data_Size", 2, hci_uint),
            HciParam("Input_PCM_Data_Format", 1, hci_pcm_data_format),
            HciParam("Output_PCM_Data_Format", 1, hci_pcm_data_format),
            HciParam("Input_PCM_Sample_Payload_MSB_Position", 1, hci_uint),
            HciParam("Output_PCM_Sample_Payload_MSB_Position", 1, hci_uint),
            HciParam("Input_Data_Path", 1, hci_uint),
            HciParam("Output_Data_Path", 1, hci_uint),
            HciParam("Input_Transport_Unit_Size", 1, hci_uint),
            HciParam("Output_Transport_Unit_Size", 1, hci_uint),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Packet_Type", 2, hci_sync_packet_type),
            HciParam("Retransmission_Effort", 1, hci_retransmission_effort),
        ],
        OCF.LINK_CONTROL.TRUNCATED_PAGE: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Page_Scan_Repetition_Mode", 1, hci_page_scan_repetition_mode),
            HciParam("Clock_Offset", 2, hci_clock_offset),
        ],
        OCF.LINK_CONTROL.TRUNCATED_PAGE_CANCEL: [HciParam("BD_ADDR", 6, hci_address)],
        OCF.LINK_CONTROL.SET_CONNECTIONLESS_PERIPHERAL_BROADCAST: [
            HciParam("Enable", 1, hci_bool),
            HciParam("LT_ADDR", 1, hci_uint),
            HciParam("LPO_Allowed", 1, hci_bool),
            HciParam("Packet_Type", 2, hci_packet_type),
            HciParam("Interval_Min", 2, hci_uint),
            HciParam("Interval_Max", 2, hci_uint),
            HciParam("Supervision_Timeout", 2, hci_uint),
        ],
        OCF.LINK_CONTROL.SET_CONNECTIONLESS_PERIPHERAL_BROADCASE_RECEIVE: [
            HciParam("Enable", 1, hci_bool),
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("LT_ADDR", 1, hci_uint),
            HciParam("Interval", 2, hci_uint),
            HciParam("Clock_Offset", 4, hci_uint),
            HciParam("Next_Connectionless_Peripheral_Broadcast_Clock", 4, hci_uint),
            HciParam("Supervision_Timeout", 2, hci_uint),
            HciParam("Remote_Timing_Accuracy", 1, hci_uint),
            HciParam("Skip", 1, hci_uint),
            HciParam("Packet_Type", 2, hci_packet_type),
            HciParam("AFH_Channel_Map", 10, hci_bt_channel_map),
        ],
        OCF.LINK_CONTROL.RECEIVE_SYNCHRONIZATION_TRAIN: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Sync_Scan_Timeout", 2, hci_uint),
            HciParam("Sync_Scan_Window", 2, hci_uint),
            HciParam("Sync_Scan_Interval", 2, hci_uint),
        ],
        OCF.LINK_CONTROL.REMOTE_OOB_EXTENDED_DATA_REQUEST_REPLY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("C_192", 16, hci_uint),
            HciParam("R_192", 16, hci_uint),
            HciParam("C_256", 16, hci_uint),
            HciParam("R_256", 16, hci_uint),
        ],
    },
    OGF.LINK_POLICY: {
        OCF.LINK_POLICY.HOLD_MODE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Hold_Mode_Max_Interval", 2, hci_time_p625ms),
            HciParam("Hold_Mode_Min_Interval", 2, hci_time_p625ms),
        ],
        OCF.LINK_POLICY.SNIFF_MODE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Sniff_Max_Interval", 2, hci_time_p625ms),
            HciParam("Sniff_Min_Interval", 2, hci_time_p625ms),
            HciParam("Sniff_Attempt", 2, hci_time_1p25ms),
            HciParam("Sniff_Timeout", 2, hci_time_1p25ms),
        ],
        OCF.LINK_POLICY.EXIT_SNIFF_MODE: [HciParam("Connection_Handle", 2, hci_uint)],
        OCF.LINK_POLICY.QOS_SETUP: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Unused", 1, hci_uint),
            HciParam("Service_Type", 1, hci_qos_service),
            HciParam("Token_Rate", 4, hci_uint),
            HciParam("Peak_Bandwidth", 4, hci_uint),
            HciParam("Latency", 4, hci_uint),
            HciParam("Delay_Variation", 4, hci_uint),
        ],
        OCF.LINK_POLICY.ROLE_DISCOVERY: [HciParam("Connection_Handle", 2, hci_uint)],
        OCF.LINK_POLICY.SWITCH_ROLE: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Role", 1, hci_role),
        ],
        OCF.LINK_POLICY.READ_LINK_POLICY_SETTINGS: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LINK_POLICY.WRITE_LINK_POLICY_SETTINGS: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Link_Policy_Settings", 2, hci_link_policy_settings),
        ],
        OCF.LINK_POLICY.WRITE_DEFAULT_LINK_POLICY_SETTINGS: [
            HciParam("Default_Link_Policy_Settings", 2, hci_link_policy_settings)
        ],
        OCF.LINK_POLICY.FLOW_SPECIFICATION: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Unused", 1, hci_uint),
            HciParam("Flow_Direction", 1, hci_datapath),
            HciParam("Service_Type", 1, hci_qos_service),
            HciParam("Token_Rate", 4, hci_uint),
            HciParam("Token_Bucket_Size", 4, hci_uint),
            HciParam("Peak_Bandwidth", 4, hci_uint),
            HciParam("Access_Latency", 4, hci_uint),
        ],
        OCF.LINK_POLICY.SNIFF_SUBRATING: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Max_Latency", 2, hci_time_p625ms),
            HciParam("Min_Remote_Timeout", 2, hci_time_p625ms),
            HciParam("Max_Remote_Timeout", 2, hci_time_p625ms),
        ],
    },
    OGF.CONTROLLER: {
        OCF.CONTROLLER.SET_EVENT_MASK: [HciParam("Event_Mask", 8, hci_event_mask)],
        OCF.CONTROLLER.SET_EVENT_FILTER: [
            HciParam("Event_Filter", None, hci_event_filter)
        ],
        OCF.CONTROLLER.FLUSH: [HciParam("Connection_Handle", 2, hci_uint)],
        OCF.CONTROLLER.WRITE_PIN_TYPE: [HciParam("Fixed_PIN", 1, hci_bool)],
        OCF.CONTROLLER.READ_STORED_LINK_KEY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Read_All", 1, hci_bool),
        ],
        OCF.CONTROLLER.WRITE_STORED_LINK_KEY: [
            HciParam("Num_Keys_To_Write", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("BD_ADDR[{}]", 6, hci_address),
                HciParam("Link_Key[{}]", 16, hci_uint),
            ],
        ],
        OCF.CONTROLLER.DELETE_STORED_LINK_KEY: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Delete_All", 1, hci_bool),
        ],
        OCF.CONTROLLER.WRITE_LOCAL_NAME: [HciParam("Local_Name", 248, hci_str)],
        OCF.CONTROLLER.WRITE_CONNECTION_ACCEPT_TIMEOUT: [
            HciParam("Connection_Accept_Timeout", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_PAGE_TIMEOUT: [
            HciParam("Page_Timeout", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_SCAN_ENABLE: [HciParam("Scan_Enable", 1, hci_scan_enable)],
        OCF.CONTROLLER.WRITE_PAGE_SCAN_ACTIVITY: [
            HciParam("Page_Scan_Interval", 2, hci_time_p625ms),
            HciParam("Page_Scan_Window", 2, hci_time_p625ms),
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_SCAN_ACTIVITY: [
            HciParam("Inquiry_Scan_Interval", 2, hci_time_p625ms),
            HciParam("Inquiry_Scan_Window", 2, hci_time_p625ms),
        ],
        OCF.CONTROLLER.WRITE_AUTHENTICATION_ENABLE: [
            HciParam("Authentication_Enable", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_CLASS_OF_DEVICE: [
            HciParam("Class_Of_Device", 3, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_VOICE_SETTING: [
            HciParam("Voice_Setting", 2, hci_voice_setting)
        ],
        OCF.CONTROLLER.READ_AUTOMATIC_FLUSH_TIMEOUT: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_AUTOMATIC_FLUSH_TIMEOUT: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Flush_Timeout", 2, hci_time_p625ms),
        ],
        OCF.CONTROLLER.WRITE_NUM_BROADCAST_RETRANSMISSIONS: [
            HciParam("Num_Broadcast_Retransmissions", 1, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_HOLD_MODE_ACTIVITY: [
            HciParam("Hold_Mode_Activity", 1, hci_hold_mode_activity)
        ],
        OCF.CONTROLLER.READ_TRANSMIT_POWER_LEVEL: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Type", 1, hci_power_read_mode),
        ],
        OCF.CONTROLLER.WRITE_SYNCHRONOUS_FLOW_CONTROL_ENABLE: [
            HciParam("Synchronous_Flow_Control_Enable", 1, hci_bool)
        ],
        OCF.CONTROLLER.SET_CONTROLLER_TO_HOST_FLOW_CONTROL: [
            HciParam("Flow_Control_Enable", 1, hci_flow_control_enable)
        ],
        OCF.CONTROLLER.HOST_BUFFER_SIZE: [
            HciParam("Host_ACL_Data_Packet_Length", 2, hci_uint),
            HciParam("Host_Synchronous_Data_Packet_Length", 1, hci_uint),
            HciParam("Host_Total_Num_ACL_Data_Packets", 2, hci_uint),
            HciParam("Host_Total_Num_Synchronous_Data_Packets", 2, hci_uint),
        ],
        OCF.CONTROLLER.HOST_NUMBER_OF_COMPLETED_PACKETS: [
            HciParam("Num_Handles", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Connection_Handle[{}]", 2, hci_uint),
                HciParam("Host_Num_Completed_Packets[{}]", 2, hci_uint),
            ],
        ],
        OCF.CONTROLLER.READ_LINK_SUPERVISION_TIMEOUT: [HciParam("Handle", 2, hci_uint)],
        OCF.CONTROLLER.WRITE_LINK_SUPERVISION_TIMEOUT: [
            HciParam("Handle", 2, hci_uint),
            HciParam("Link_Supervision_Timeout", 2, hci_time_p625ms),
        ],
        OCF.CONTROLLER.WRITE_CURRENT_IAC_LAP: [
            HciParam("Num_Current_IAC", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("IAC_LAP[{}]", 3, hci_uint)],
        ],
        OCF.CONTROLLER.SET_AFH_HOST_CHANNEL_CLASSIFICATION: [
            HciParam("AFH_Host_Channel_Classification", 10, hci_bt_channel_map)
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_SCAN_TYPE: [
            HciParam("Scan_Type", 1, hci_scan_mode)
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_MODE: [
            HciParam("Inquiry_Mode", 1, hci_inquiry_mode)
        ],
        OCF.CONTROLLER.WRITE_PAGE_SCAN_TYPE: [
            HciParam("Page_Scan_Type", 1, hci_scan_mode)
        ],
        OCF.CONTROLLER.WRITE_AFH_CHANNEL_ASSESSMENT_MODE: [
            HciParam("AFH_Channel_Assessment_Enabled", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_EXTENDED_INQUIRY_RESPONSE: [
            HciParam("FEC_Required", 1, hci_bool),
            HciParam("Extended_Inquiry_Response", 240, hci_uint),
        ],
        OCF.CONTROLLER.REFRESH_ENCRYPTION_KEY: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_SIMPLE_PAIRING_MODE: [
            HciParam("Simple_Pairing_Enable", 1, hci_bool)
        ],
        OCF.CONTROLLER.WRITE_INQUIRY_TRANSMIT_POWER_LEVEL: [
            HciParam("TX_Power", 1, hci_int)
        ],
        OCF.CONTROLLER.WRITE_DEFAULT_ERRONEOUS_DATA_REPORTING: [
            HciParam("Erroneous_Data_Reporting", 1, hci_bool)
        ],
        OCF.CONTROLLER.ENHANCED_FLUSH: [
            HciParam("Handle", 2, hci_uint),
            HciParam("Packet_Type", 1, hci_uint),
        ],
        OCF.CONTROLLER.SEND_KEYPRESS_NOTIFICATION: [
            HciParam("BD_ADDR", 6, hci_address),
            HciParam("Notification_Type", 1, hci_keypress_notification),
        ],
        OCF.CONTROLLER.SET_EVENT_MASK_PAGE_2: [
            HciParam("Event_Mask_Page_2", 8, hci_event_mask_page_2)
        ],
        OCF.CONTROLLER.WRITE_FLOW_CONTROL_MODE: [
            HciParam("Flow_Control_Mode", 1, hci_flow_control_mode)
        ],
        OCF.CONTROLLER.READ_ENHANCED_TRANSMIT_POWER_LEVEL: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Type", 1, hci_power_read_mode),
        ],
        OCF.CONTROLLER.WRITE_LE_HOST_SUPPORT: [
            HciParam("LE_Host_Support", 1, hci_bool),
            HciParam("Unused", 1, hci_uint),
        ],
        OCF.CONTROLLER.SET_MWS_CHANNEL_PARAMETERS: [
            HciParam("MWS_Channel_Enable", 1, hci_bool),
            HciParam("MWS_RX_Center_Frequency", 2, hci_uint),
            HciParam("MWS_TX_Center_Frequency", 2, hci_uint),
            HciParam("MWS_RX_Channel_Bandwidth", 2, hci_uint),
            HciParam("MWS_TX_Channel_Bandwidth", 2, hci_uint),
            HciParam("MWS_Channel_Type", 1, hci_mws_channel_type),
        ],
        OCF.CONTROLLER.SET_EXTERNAL_FRAME_CONFIGURATION: [
            HciParam("MWS_Frame_Duration", 2, hci_uint),
            HciParam("MWS_Frame_Sync_Assert_Offset", 2, hci_int),
            HciParam("MWS_Frame_Sync_Assert_Jitter", 2, hci_uint),
            HciParam("MWS_Num_Periods", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Period_Duration[{}]", 2, hci_uint),
                HciParam("Period_Type[{}]", 1, hci_mws_period_type),
            ],
        ],
        OCF.CONTROLLER.SET_MWS_SIGNALING: [
            HciParam("MWS_RX_Assert_Offset", 2, hci_int),
            HciParam("MWS_RX_Assert_Jitter", 2, hci_uint),
            HciParam("MWS_RX_Deassert_Offset", 2, hci_int),
            HciParam("MWS_RX_Deassert_Jitter", 2, hci_uint),
            HciParam("MWS_TX_Assert_Offset", 2, hci_int),
            HciParam("MWS_TX_Assert_Jitter", 2, hci_uint),
            HciParam("MWS_TX_Deassert_Offset", 2, hci_int),
            HciParam("MWS_TX_Deassert_Jitter", 2, hci_uint),
            HciParam("MWS_Pattern_Assert_Offset", 2, hci_int),
            HciParam("MWS_Pattern_Assert_Jitter", 2, hci_uint),
            HciParam("MWS_Inactivity_Duration_Assert_Offset", 2, hci_int),
            HciParam("MWS_Inactivity_Duration_Assert_Jitter", 2, hci_uint),
            HciParam("MWS_Scan_Frequency_Assert_Offset", 2, hci_int),
            HciParam("MWS_Scan_Frequency_Assert_Jitter", 2, hci_uint),
            HciParam("MWS_Priority_Assert_Offset_Request", 2, hci_uint),
        ],
        OCF.CONTROLLER.SET_MWS_TRANSPORT_LAYER: [
            HciParam("Transport_Layer", 1, hci_mws_transport_layer),
            HciParam("To_MWS_Baud_Rate", 4, hci_uint),
            HciParam("From_MWS_Baud_Rate", 4, hci_uint),
        ],
        OCF.CONTROLLER.SET_MWS_SCAN_FREQUENCY_TABLE: [
            HciParam("Num_Scan_Frequencies", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Scan_Frequency_Low[{}]", 2, hci_uint),
                HciParam("Scan_Frequency_High[{}]", 2, hci_uint),
            ],
        ],
        OCF.CONTROLLER.SET_MWS_PATTERN_CONFIGURATION: [
            HciParam("MWS_Pattern_Index", 1, hci_uint),
            HciParam("MWS_Pattern_Num_Intervals", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("MWS_Pattern_Interval_Duration[{}]", 2, hci_uint),
                HciParam(
                    "MWS_Pattern_Interval_Type[{}]", 1, hci_mws_pattern_interval_type
                ),
            ],
        ],
        OCF.CONTROLLER.SET_RESERVED_LT_ADDR: [HciParam("LT_ADDR", 1, hci_uint)],
        OCF.CONTROLLER.DELETE_RESERVED_LT_ADDR: [HciParam("LT_ADDR", 1, hci_uint)],
        OCF.CONTROLLER.SET_CONNECTIONLESS_PERIPHERAL_BROADCAST_DATA: [
            HciParam("LT_ADDR", 1, hci_uint),
            HciParam("Fragment", 1, hci_fragment),
            HciParam("Data_Length", 1, hci_uint),
            HciParam("Data", HciParamIdxRef(-1), hci_uint),
        ],
        OCF.CONTROLLER.WRITE_SYNCHRONIZATION_TRAIN_PARAMETERS: [
            HciParam("Interval_Min", 2, hci_uint),
            HciParam("Interval_Max", 2, hci_uint),
            HciParam("Sync_Train_Timeout", 4, hci_uint),
            HciParam("Service_Data", 1, hci_uint),
        ],
        OCF.CONTROLLER.WRITE_SECURE_CONNECTIONS_HOST_SUPPORT: [
            HciParam("Secure_Connections_Host_Support", 1, hci_bool)
        ],
        OCF.CONTROLLER.READ_AUTHENTICATED_PAYLOAD_TIMEOUT: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.CONTROLLER.WRITE_AUTHENTICATED_PAYLOAD_TIMEOUT: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Authenticated_Payload_Timeout", 2, hci_time_10ms),
        ],
        OCF.CONTROLLER.WRITE_EXTENDED_PAGE_TIMEOUT: [
            HciParam("Extended_Page_Timeout", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.WRITE_EXTENDED_INQUIRY_LENGTH: [
            HciParam("Extended_Inquiry_Length", 2, hci_time_p625ms)
        ],
        OCF.CONTROLLER.SET_ECOSYSTEM_BASE_INTERVAL: [
            HciParam("Interval", 2, hci_time_1p25ms)
        ],
        OCF.CONTROLLER.CONFIGURE_DATA_PATH: [
            HciParam("Data_Path_Direction", 1, hci_datapath),
            HciParam("Data_Path_ID", 1, hci_uint),
            HciParam("Vendor_Specific_Config_Length", 1, hci_uint),
            HciParam("Vendor_Specific_Config", HciParamIdxRef(-1), hci_uint),
        ],
        OCF.CONTROLLER.SET_MIN_ENCRYPTION_KEY_SIZE: [
            HciParam("Min_Encryption_Key_Size", 1, hci_uint)
        ],
    },
    OGF.INFORMATIONAL: {
        OCF.INFORMATIONAL.READ_LOCAL_EXTENDED_FEATURES: [
            HciParam("Page_Number", 1, hci_uint)
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_CODEC_CAPABILITIES: [
            HciParam("Codec_ID", 5, hci_codec),
            HciParam("Logical_Transport_Type", 1, hci_logical_transport_type),
            HciParam("Direction", 1, hci_datapath),
        ],
        OCF.INFORMATIONAL.READ_LOCAL_SUPPORTED_CONTROLLER_DELAY: [
            HciParam("Codec_ID", 5, hci_codec),
            HciParam("Logical_Transport_Type", 1, hci_logical_transport_type),
            HciParam("Direction", 1, hci_datapath),
            HciParam("Codec_Configuration_Length", 1, hci_uint),
            HciParam("Codec_Configuration", HciParamIdxRef(-1), hci_uint),
        ],
    },
    OGF.STATUS: {
        OCF.STATUS.READ_FAILED_CONTACT_COUNTER: [HciParam("Handle", 2, hci_uint)],
        OCF.STATUS.RESET_FAILED_CONTACT_COUNTER: [HciParam("Handle", 2, hci_uint)],
        OCF.STATUS.READ_LINK_QUALITY: [HciParam("Handle", 2, hci_uint)],
        OCF.STATUS.READ_RSSI: [HciParam("Handle", 2, hci_uint)],
        OCF.STATUS.READ_AFH_CHANNEL_MAP: [HciParam("Connection_Handle", 2, hci_uint)],
        OCF.STATUS.READ_CLOCK: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Which_Clock", 1, hci_clock_select),
        ],
        OCF.STATUS.READ_ENCRYPTION_KEY_SIZE: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.STATUS.SET_TRIGGERED_CLOCK_CAPTURE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Enable", 1, hci_bool),
            HciParam("Which_Clock", 1, hci_clock_select),
            HciParam("LPO_Allowed", 1, hci_bool),
            HciParam("Num_Clock_Captures_To_Filter", 1, hci_uint),
        ],
    },
    OGF.TESTING: {
        OCF.TESTING.WRITE_LOOPBACK_MODE: [
            HciParam("Loopback_Mode", 1, hci_loopback_mode)
        ],
        OCF.TESTING.WRITE_SIMPLE_PAIRING_DEBUG_MODE: [
            HciParam("Simple_Pairing_Debug_Mode", 1, hci_bool)
        ],
        OCF.TESTING.WRITE_SECURE_CONNECTIONS_TEST_MODE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("DM1_ACL-U_Mode", 1, hci_bool),
            HciParam("eSCO_Loopback_Mode", 1, hci_bool),
        ],
    },
    OGF.LE_CONTROLLER: {
        OCF.LE_CONTROLLER.LE_SET_EVENT_MASK: [
            HciParam("LE_Event_Mask", 8, hci_le_event_mask)
        ],
        OCF.LE_CONTROLLER.LE_SET_RANDOM_ADDRESS: [
            HciParam("Random_Address", 6, hci_address)
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_PARAMETERS: [
            HciParam("Advertising_Interval_Min", 2, hci_time_p625ms),
            HciParam("Advertising_Interval_Max", 2, hci_time_p625ms),
            HciParam("Advertising_Type", 1, hci_advertising_type),
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address", 6, hci_address),
            HciParam("Advertising_Channel_Map", 1, hci_advertising_channel_map),
            HciParam("Advertising_Filter_Policy", 1, hci_advertising_filter_policy),
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_DATA: [
            HciParam("Advertising_Data_Length", 1, hci_uint),
            HciParam("Advertising_Data", 31, hci_str),
        ],
        OCF.LE_CONTROLLER.LE_SET_SCAN_RESPONSE_DATA: [
            HciParam("Scan_Response_Data_Length", 1, hci_uint),
            HciParam("Scan_Response_Data", 31, hci_str),
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_ENABLE: [
            HciParam("Advertising_Enable", 1, hci_bool)
        ],
        OCF.LE_CONTROLLER.LE_SET_SCAN_PARAMETERS: [
            HciParam("LE_Scan_Type", 1, hci_le_scan_type),
            HciParam("LE_Scan_Interval", 2, hci_time_p625ms),
            HciParam("LE_Scan_Window", 2, hci_time_p625ms),
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Scanning_Filter_Policy", 1, hci_scan_filter_policy),
        ],
        OCF.LE_CONTROLLER.LE_SET_SCAN_ENABLE: [
            HciParam("LE_Scan_Enable", 1, hci_bool),
            HciParam("Filter_Duplicates", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_CREATE_CONNECTION: [
            HciParam("LE_Scan_Interval", 2, hci_time_p625ms),
            HciParam("LE_Scan_Window", 2, hci_time_p625ms),
            HciParam("Initiator_Use_Filter_Accept_List", 1, hci_bool),
            HciParam("Peer_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address", 6, hci_address),
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Connection_Interval_Min", 2, hci_time_1p25ms),
            HciParam("Connection_Interval_Max", 2, hci_time_1p25ms),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Supervision_Timeout", 2, hci_time_10ms),
            HciParam("Min_CE_Length", 2, hci_time_p625ms),
            HciParam("Max_CE_Length", 2, hci_time_p625ms),
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_FILTER_ACCEPT_LIST: [
            HciParam("Address_Type", 1, hci_address_type),
            HciParam("Address", 1, hci_address),
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_FILTER_ACCEPT_LIST: [
            HciParam("Address_Type", 1, hci_address_type),
            HciParam("Address", 1, hci_address),
        ],
        OCF.LE_CONTROLLER.LE_CONNECTION_UPDATE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Connection_Interval_Min", 2, hci_time_1p25ms),
            HciParam("Connection_Interval_Max", 2, hci_time_1p25ms),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Supervision_Timeout", 2, hci_time_10ms),
            HciParam("Min_CE_Length", 2, hci_time_p625ms),
            HciParam("Max_CE_Length", 2, hci_time_p625ms),
        ],
        OCF.LE_CONTROLLER.LE_SET_HOST_CHANNEL_CLASSIFICATION: [
            HciParam("Channel_Map", 5, hci_ble_channel_map)
        ],
        OCF.LE_CONTROLLER.LE_READ_CHANNEL_MAP: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_REMOTE_FEATURES: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ENCRYPT: [
            HciParam("Key", 16, hci_uint),
            HciParam("Plaintext_Data", 16, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_ENABLE_ENCRYPTION: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Random_Number", 8, hci_uint),
            HciParam("Encrypted_Diversifier", 2, hci_uint),
            HciParam("Long_Term_Key", 16, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_LONG_TERM_KEY_REQUEST_REPLY: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Long_Term_Key", 16, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_LONG_TERM_KEY_REQUEST_NEGATIVE_REPLY: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_RECEIVER_TEST_V1: [HciParam("RX_Channel", 1, hci_uint)],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V1: [
            HciParam("TX_Channel", 1, hci_uint),
            HciParam("Test_Data_Length", 1, hci_uint),
            HciParam("Packet_Payload", 1, hci_packet_payload),
        ],
        OCF.LE_CONTROLLER.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_REPLY: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Interval_Min", 2, hci_time_1p25ms),
            HciParam("Interval_Max", 2, hci_time_1p25ms),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Timeout", 2, hci_time_10ms),
            HciParam("Min_CE_Length", 2, hci_time_p625ms),
            HciParam("Max_CE_Length", 2, hci_time_p625ms),
        ],
        OCF.LE_CONTROLLER.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_NEGATIVE_REPLY: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Reason", 1, hci_status),
        ],
        OCF.LE_CONTROLLER.LE_SET_DATA_LENGTH: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("TX_Octets", 2, hci_uint),
            HciParam("TX_Time", 2, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_WRITE_SUGGESTED_DEFAULT_DATA_LENGTH: [
            HciParam("Suggested_Max_TX_Octets", 2, hci_uint),
            HciParam("Suggested_Max_TX_Time", 2, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_GENERATE_DHKEY_V1: [
            HciParam("Key_X_Coordinate", 32, hci_uint),
            HciParam("Key_Y_Coordinate", 32, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_RESOLVING_LIST: [
            HciParam("Peer_Identity_Address_Type", 1, hci_address_type),
            HciParam("Peer_Identity_Address", 6, hci_address),
            HciParam("Peer_IRK", 16, hci_uint),
            HciParam("Local_IRK", 16, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_RESOLVING_LIST: [
            HciParam("Peer_Identity_Address_Type", 1, hci_address_type),
            HciParam("Peer_Identity_Address", 6, hci_address),
        ],
        OCF.LE_CONTROLLER.LE_READ_PEER_RESOLVABLE_ADDRESS: [
            HciParam("Peer_Identity_Address_Type", 1, hci_address_type),
            HciParam("Peer_Identity_Address", 6, hci_address),
        ],
        OCF.LE_CONTROLLER.LE_READ_LOCAL_RESOLVABLE_ADDRESS: [
            HciParam("Peer_Identity_Address_Type", 1, hci_address_type),
            HciParam("Peer_Identity_Address", 6, hci_address),
        ],
        OCF.LE_CONTROLLER.LE_SET_ADDRESS_RESOLUTION_ENABLE: [
            HciParam("Address_Resolution_Enable", 1, hci_bool)
        ],
        OCF.LE_CONTROLLER.LE_SET_RESOLVABLE_PRIVATE_ADDRESS_TIMEOUT: [
            HciParam("RPA_Timeout", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_READ_PHY: [HciParam("Connection_Handle", 2, hci_uint)],
        OCF.LE_CONTROLLER.LE_SET_DEFAULT_PHY: [
            HciParam("All_PHYs", 1, hci_phy_preference),
            HciParam("TX_PHYs", 1, hci_phy_mask),
            HciParam("RX_PHYs", 1, hci_phy_mask),
        ],
        OCF.LE_CONTROLLER.LE_SET_PHY: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("All_PHYs", 1, hci_phy_preference),
            HciParam("TX_PHYs", 1, hci_phy_mask),
            HciParam("RX_PHYs", 1, hci_phy_mask),
            HciParam("PHY_Options", 2, hci_phy_options),
        ],
        OCF.LE_CONTROLLER.LE_RECEIVER_TEST_V2: [
            HciParam("RX_Channel", 1, hci_uint),
            HciParam("PHY", 1, hci_phy_select),
            HciParam("Modulation_Index", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V2: [
            HciParam("TX_Channel", 1, hci_uint),
            HciParam("Test_Data_Length", 1, hci_uint),
            HciParam("Packet_Payload", 1, hci_packet_payload),
            HciParam("PHY", 1, hci_phy_select),
        ],
        OCF.LE_CONTROLLER.LE_SET_ADVERTISING_SET_RANDOM_ADDRESS: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Random_Address", 6, hci_address),
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_PARAMETERS_V1: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam(
                "Advertising_Event_Properties", 2, hci_advertising_event_properties
            ),
            HciParam("Primary_Advertising_Interval_Min", 3, hci_time_p625ms),
            HciParam("Primary_Advertising_Interval_Max", 3, hci_time_p625ms),
            HciParam("Primary_Advertising_Channel_Map", 1, hci_advertising_channel_map),
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address", 6, hci_address),
            HciParam("Advertising_Filter_Policy", 1, hci_advertising_filter_policy),
            HciParam("Advertising_TX_Power", 1, hci_int),
            HciParam("Primary_Advertising_PHY", 1, hci_phy_select),
            HciParam("Secondary_Advertising_Max_Skip", 1, hci_uint),
            HciParam("Secondary_Advertising_PHY", 1, hci_phy_select),
            HciParam("Advertising_SID", 1, hci_uint),
            HciParam("Scan_Request_Notification_Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_DATA: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Operation", 1, hci_fragment),
            HciParam("Fragment_Preference", 1, hci_fragment_preference),
            HciParam("Advertising_Data_Length", 1, hci_uint),
            HciParam("Advertising_Data", HciParamIdxRef(-1), hci_str),
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_SCAN_RESPONSE_DATA: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Operation", 1, hci_fragment),
            HciParam("Fragment_Preference", 1, hci_fragment_preference),
            HciParam("Scan_Response_Data_Length", 1, hci_uint),
            HciParam("Scan_Response_Data", HciParamIdxRef(-1), hci_str),
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_ENABLE: [
            HciParam("Enable", 1, hci_bool),
            HciParam("Num_Sets", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Advertising_Handle[{}]", 1, hci_uint),
                HciParam("Duration[{}]", 2, hci_time_10ms),
                HciParam("Max_Extended_Advertising_Events[{}]", 1, hci_uint),
            ],
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_ADVERTISING_SET: [
            HciParam("Advertising_Handle", 1, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_PARAMETERS_V1: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Periodic_Advertising_Interval_Min", 2, hci_time_1p25ms),
            HciParam("Periodic_Advertising_Interval_Max", 2, hci_time_1p25ms),
            HciParam(
                "Periodic_Advertising_Properties",
                2,
                hci_periodic_advertising_properties,
            ),
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_DATA: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Operation", 1, hci_fragment),
            HciParam("Advertising_Data_Length", 1, hci_uint),
            HciParam("Advertising_Data", HciParamIdxRef(-1), hci_str),
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_ENABLE: [
            HciParam("Enable", 1, hci_bool),
            HciParam("Advertising_Handle", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_SCAN_PARAMETERS: [
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Scanning_Filter_Policy", 1, hci_scan_filter_policy),
            HciParam("Scanning_PHYs", 1, hci_phy_mask),
            [
                HciParamIdxRef(-1),
                HciParam("Scan_Type[{}]", 1, hci_le_scan_type),
                HciParam("Scan_Interval[{}]", 2, hci_time_p625ms),
                HciParam("Scan_Window[{}]", 2, hci_time_p625ms),
            ],
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_SCAN_ENABLE: [
            HciParam("Enable", 1, hci_bool),
            HciParam("Filter_Duplicates", 1, hci_bool),
            HciParam("Duration", 2, hci_time_10ms),
            HciParam("Period", 2, hci_time_1p28s),
        ],
        OCF.LE_CONTROLLER.LE_EXTENDED_CREATE_CONNECTION_V1: [
            HciParam("Initiator_Filter_Policy", 1, hci_connection_filter_policy),
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address", 6, hci_address),
            HciParam("Initiating_PHYs", 1, hci_phy_mask),
            [
                HciParamIdxRef(-1),
                HciParam("Scan_Interval[{}]", 2, hci_time_p625ms),
                HciParam("Scan_Window[{}]", 2, hci_time_p625ms),
                HciParam("Connection_Interval_Min[{}]", 2, hci_time_1p25ms),
                HciParam("Connection_Interval_Max[{}]", 2, hci_time_1p25ms),
                HciParam("Max_Latency[{}]", 2, hci_uint),
                HciParam("Supervision_Timeout[{}]", 2, hci_time_10ms),
                HciParam("Min_CE_Length[{}]", 2, hci_time_p625ms),
                HciParam("Max_CE_Length[{}]", 2, hci_time_p625ms),
            ],
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_CREATE_SYNC: [
            HciParam("Options", 1, hci_sync_options),
            HciParam("Advertising_SID", 1, hci_uint),
            HciParam("Advertiser_Address_Type", 1, hci_address_type),
            HciParam("Advertiser_Address", 6, hci_address),
            HciParam("Skip", 2, hci_uint),
            HciParam("Sync_Timeout", 2, hci_time_10ms),
            HciParam("Sync_CTE_Type", 1, hci_sync_cte_type),
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_TERMINATE_SYNC: [
            HciParam("Sync_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_PERIODIC_ADVERTISER_LIST: [
            HciParam("Advertiser_Address_Type", 1, hci_address_type),
            HciParam("Advertiser_Address", 6, hci_address),
            HciParam("Advertising_SID", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_PERIODIC_ADVERTISER_LIST: [
            HciParam("Advertiser_Address_Type", 1, hci_address_type),
            HciParam("Advertiser_Address", 6, hci_address),
            HciParam("Advertising_SID", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_WRITE_RF_PATH_COMPENSATION: [
            HciParam("RF_TX_Path_Compensation_Value", 2, hci_int),
            HciParam("RF_RX_Path_Compensation_Value", 2, hci_int),
        ],
        OCF.LE_CONTROLLER.LE_SET_PRIVACY_MODE: [
            HciParam("Peer_Identity_Address_Type", 1, hci_address_type),
            HciParam("Peer_Identity_Address", 6, hci_address),
            HciParam("Privacy_Mode", 1, hci_privacy_mode),
        ],
        OCF.LE_CONTROLLER.LE_RECEIVER_TEST_V3: [
            HciParam("RX_Channel", 1, hci_uint),
            HciParam("PHY", 1, hci_phy_select),
            HciParam("Modulation_Index", 1, hci_uint),
            HciParam("Expected_CTE_Length", 1, hci_uint),
            HciParam("Expected_CTE_Type", 1, hci_cte_type_select),
            HciParam("Slot_Durations", 1, hci_uint),
            HciParam("Switching_Pattern_Length", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Antenna_IDs[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V3: [
            HciParam("TX_Channel", 1, hci_uint),
            HciParam("Test_Data_Length", 1, hci_uint),
            HciParam("Packet_Payload", 1, hci_packet_payload),
            HciParam("PHY", 1, hci_phy_select),
            HciParam("CTE_Length", 1, hci_uint),
            HciParam("CTE_Type", 1, hci_cte_type_select),
            HciParam("Switching_Pattern_Length", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Antenna_IDs[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTIONLESS_CTE_TRANSMIT_PARAMETERS: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("CTE_Length", 1, hci_uint),
            HciParam("CTE_Type", 1, hci_cte_type_select),
            HciParam("CTE_Count", 1, hci_uint),
            HciParam("Switching_Pattern_Length", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Antenna_IDs[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTIONLESS_CTE_TRANSMIT_ENABLE: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("CTE_Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTIONLESS_IQ_SAMPLING_ENABLE: [
            HciParam("Sync_Handle", 2, hci_uint),
            HciParam("Sampling_Enable", 1, hci_bool),
            HciParam("Slot_Durations", 1, hci_uint),
            HciParam("Max_Samples_CTEs", 1, hci_uint),
            HciParam("Switching_Pattern_Length", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Antenna_IDs[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTION_CTE_RECEIVE_PARAMETERS: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Sampling_Enable", 1, hci_bool),
            HciParam("Slot_Durations", 1, hci_uint),
            HciParam("Switching_Pattern_Length", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Antenna_IDs[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_SET_CONNECTION_CTE_TRANSMIT_PARAMETERS: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("CTE_Types", 1, hci_cte_type_mask),
            HciParam("Switching_Pattern_Length", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Antenna_IDs[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_CONNECTION_CTE_REQUEST_ENABLE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Enable", 1, hci_bool),
            HciParam("CTE_Request_Interval", 2, hci_uint),
            HciParam("Requested_CTE_Length", 1, hci_uint),
            HciParam("Requested_CTE_Type", 1, hci_cte_type_select),
        ],
        OCF.LE_CONTROLLER.LE_CONNECTION_CTE_RESPONSE_ENABLE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_RECEIVE_ENABLE: [
            HciParam("Sync_Handle", 2, hci_uint),
            HciParam("Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_SYNC_TRANSFER: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Service_Data", 2, hci_uint),
            HciParam("Sync_Handle", 2, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_PERIODIC_ADVERTISING_SET_INFO_TRANSFER: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Service_Data", 2, hci_uint),
            HciParam("Advertising_Handle", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_SYNC_TRANSFER_PARAMETERS: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Mode", 1, hci_periodic_advertising_mode),
            HciParam("Skip", 2, hci_uint),
            HciParam("Sync_Timeout", 2, hci_time_10ms),
            HciParam("CTE_Type", 1, hci_sync_cte_type),
        ],
        OCF.LE_CONTROLLER.LE_SET_DEFAULT_PERIODIC_ADVERTISING_SYNC_TRANSFER_PARAMETERS: [
            HciParam("Mode", 1, hci_periodic_advertising_mode),
            HciParam("Skip", 2, hci_uint),
            HciParam("Sync_Timeout", 2, hci_time_10ms),
            HciParam("CTE_Type", 1, hci_sync_cte_type),
        ],
        OCF.LE_CONTROLLER.LE_GENERATE_DHKEY_V2: [
            HciParam("Key_X_Coordinate", 32, hci_uint),
            HciParam("Key_Y_Coordinate", 32, hci_uint),
            HciParam("Key_Type", 1, hci_dh_key_type),
        ],
        OCF.LE_CONTROLLER.LE_MODIFY_SLEEP_CLOCK_ACCURACY: [
            HciParam("Action", 1, hci_sleep_clock_action)
        ],
        OCF.LE_CONTROLLER.LE_READ_ISO_TX_SYNC: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SET_CIG_PARAMETERS: [
            HciParam("CIG_ID", 1, hci_uint),
            HciParam("SDU_Interval_C_To_P", 3, hci_uint),
            HciParam("SDU_Interval_P_To_C", 3, hci_uint),
            HciParam("Worst_Case_SCA", 1, hci_clock_accuracy_ranged),
            HciParam("Packing", 1, hci_packing_mode),
            HciParam("Framing", 1, hci_framing_mode),
            HciParam("Max_Transport_Latency_C_To_P", 2, hci_uint),
            HciParam("Max_Transport_Latency_P_To_C", 2, hci_uint),
            HciParam("CIS_Count", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("CIS_ID[{}]", 1, hci_uint),
                HciParam("Max_SDU_C_To_P[{}]", 2, hci_uint),
                HciParam("Max_SDU_P_To_C[{}]", 2, hci_uint),
                HciParam("PHY_C_To_P[{}]", 1, hci_phy_mask),
                HciParam("PHY_P_To_C[{}]", 1, hci_phy_mask),
                HciParam("RTN_C_To_P[{}]", 1, hci_uint),
                HciParam("RTN_P_To_C[{}]", 1, hci_uint),
            ],
        ],
        OCF.LE_CONTROLLER.LE_SET_CIG_PARAMETERS_TEST: [
            HciParam("CIG_ID", 1, hci_uint),
            HciParam("SDU_Interval_C_To_P", 3, hci_uint),
            HciParam("SDU_Interval_P_To_C", 3, hci_uint),
            HciParam("FT_C_To_P", 1, hci_uint),
            HciParam("FT_P_To_C", 1, hci_uint),
            HciParam("ISO_Interval", 2, hci_time_1p25ms),
            HciParam("Worst_Case_SCA", 1, hci_clock_accuracy_ranged),
            HciParam("Packing", 1, hci_packing_mode),
            HciParam("Framing", 1, hci_framing_mode),
            HciParam("CIS_Count", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("CIS_ID[{}]", 1, hci_uint),
                HciParam("NSE[{}]", 1, hci_uint),
                HciParam("Max_SDU_C_To_P[{}]", 2, hci_uint),
                HciParam("Max_SDU_P_To_C[{}]", 2, hci_uint),
                HciParam("Max_PDU_C_To_P[{}]", 2, hci_uint),
                HciParam("Max_PDU_P_To_C[{}]", 2, hci_uint),
                HciParam("PHY_C_To_P[{}]", 1, hci_phy_mask),
                HciParam("PHY_P_To_C[{}]", 1, hci_phy_mask),
                HciParam("BN_C_To_P[{}]", 1, hci_uint),
                HciParam("BN_P_To_C[{}]", 1, hci_uint),
            ],
        ],
        OCF.LE_CONTROLLER.LE_CREATE_CIS: [
            HciParam("CIS_Count", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("CIS_Connection_Handle[{}]", 2, hci_uint),
                HciParam("ACL_Connection_Handle[{}]", 2, hci_uint),
            ],
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_CIG: [HciParam("CIG_ID", 1, hci_uint)],
        OCF.LE_CONTROLLER.LE_ACCEPT_CIS_REQUEST: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_REJECT_CIS_REQUEST: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Reason", 1, hci_status),
        ],
        OCF.LE_CONTROLLER.LE_CREATE_BIG: [
            HciParam("BIG_Handle", 1, hci_uint),
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Num_BIS", 1, hci_uint),
            HciParam("SDU_Interval", 3, hci_uint),
            HciParam("Max_SDU", 2, hci_uint),
            HciParam("Max_Transport_Latency", 2, hci_uint),
            HciParam("RTN", 1, hci_uint),
            HciParam("PHY", 1, hci_phy_mask),
            HciParam("Packing", 1, hci_packing_mode),
            HciParam("Framing", 1, hci_framing_mode),
            HciParam("Encryption", 1, hci_bool),
            HciParam("Broadcast_Code", 16, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_CREATE_BIG_TEST: [
            HciParam("BIG_Handle", 1, hci_uint),
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Num_BIS", 1, hci_uint),
            HciParam("SDU_Interval", 3, hci_uint),
            HciParam("ISO_Interval", 2, hci_time_1p25ms),
            HciParam("NSE", 1, hci_uint),
            HciParam("Max_SDU", 2, hci_uint),
            HciParam("Max_PDU", 2, hci_uint),
            HciParam("PHY", 1, hci_phy_mask),
            HciParam("Packing", 1, hci_packing_mode),
            HciParam("Framing", 1, hci_framing_mode),
            HciParam("BN", 1, hci_uint),
            HciParam("IRC", 1, hci_uint),
            HciParam("PTO", 1, hci_uint),
            HciParam("Encryption", 1, hci_bool),
            HciParam("Broadcast_Code", 16, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_TERMINATE_BIG: [
            HciParam("BIG_Handle", 1, hci_uint),
            HciParam("Reason", 1, hci_status),
        ],
        OCF.LE_CONTROLLER.LE_BIG_CREATE_SYNC: [
            HciParam("BIG_Handle", 1, hci_uint),
            HciParam("Sync_Handle", 2, hci_uint),
            HciParam("Encryption", 1, hci_bool),
            HciParam("Broadcast_Code", 16, hci_uint),
            HciParam("MSE", 1, hci_uint),
            HciParam("BIG_Sync_Timeout", 2, hci_time_10ms),
            HciParam("Num_BIS", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("BIS[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_BIG_TERMINATE_SYNC: [HciParam("BIG_Handle", 1, hci_uint)],
        OCF.LE_CONTROLLER.LE_REQUEST_PEER_SCA: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_SETUP_ISO_DATA_PATH: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Data_Path_Direction", 1, hci_datapath),
            HciParam("Data_Path_ID", 1, hci_uint),
            HciParam("Codec_ID", 5, hci_codec),
            HciParam("Controller_Delay", 3, hci_uint),
            HciParam("Codec_Configuration_Length", 1, hci_uint),
            HciParam("Codec_Configuration", HciParamIdxRef(-1), hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_ISO_DATA_PATH: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Data_Path_Direction", 1, hci_datapath),
        ],
        OCF.LE_CONTROLLER.LE_ISO_TRANSMIT_TEST: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Payload_Type", 1, hci_iso_payload_type),
        ],
        OCF.LE_CONTROLLER.LE_ISO_RECEIVE_TEST: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Payload_Type", 1, hci_iso_payload_type),
        ],
        OCF.LE_CONTROLLER.LE_ISO_READ_TEST_COUNTERS: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ISO_TEST_END: [HciParam("Connection_Handle", 2, hci_uint)],
        OCF.LE_CONTROLLER.LE_SET_HOST_FEATURE_V1: [
            HciParam("Bit_Number", 1, hci_uint),
            HciParam("Bit_Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_READ_ISO_LINK_QUALITY: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_ENHANCED_READ_TRANSMIT_POWER_LEVEL: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("PHY", 1, hci_phy_select),
        ],
        OCF.LE_CONTROLLER.LE_READ_REMOTE_TRANSMIT_POWER_LEVEL: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("PHY", 1, hci_phy_select),
        ],
        OCF.LE_CONTROLLER.LE_SET_PATH_LOSS_REPORTING_PARAMETERS: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("High_Threshold", 1, hci_int),
            HciParam("High_Hysteresis", 1, hci_int),
            HciParam("Low_Threshold", 1, hci_int),
            HciParam("Low_Hysteresis", 1, hci_int),
            HciParam("Min_Time_Spent", 2, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_SET_PATH_LOSS_REPORTING_ENABLE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_SET_TRANSMIT_POWER_REPORTING_ENABLE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Local_Enable", 1, hci_bool),
            HciParam("Remote_Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_TRANSMITTER_TEST_V4: [
            HciParam("TX_Channel", 1, hci_uint),
            HciParam("Test_Data_Length", 1, hci_uint),
            HciParam("Packet_Payload", 1, hci_packet_payload),
            HciParam("PHY", 1, hci_phy_select),
            HciParam("CTE_Length", 1, hci_uint),
            HciParam("CTE_Type", 1, hci_cte_type_select),
            HciParam("Switching_Pattern_Length", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Antenna_IDs[{}]", 1, hci_uint)],
            HciParam("TX_Power_Level", 1, hci_int),
        ],
        OCF.LE_CONTROLLER.LE_SET_DATA_RELATED_ADDRESS_CHANGES: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Change_Reasons", 1, hci_address_change_reasons),
        ],
        OCF.LE_CONTROLLER.LE_SET_DEFAULT_SUBRATE: [
            HciParam("Subrate_Min", 2, hci_uint),
            HciParam("Subrate_Max", 2, hci_uint),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Continuation_Number", 2, hci_uint),
            HciParam("Supervision_Timeout", 2, hci_time_10ms),
        ],
        OCF.LE_CONTROLLER.LE_SUBRATE_REQUEST: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Subrate_Min", 2, hci_uint),
            HciParam("Subrate_Max", 2, hci_uint),
            HciParam("Max_Latency", 2, hci_uint),
            HciParam("Continuation_Number", 2, hci_uint),
            HciParam("Supervision_Timeout", 2, hci_time_10ms),
        ],
        OCF.LE_CONTROLLER.LE_SET_EXTENDED_ADVERTISING_PARAMETERS_V2: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam(
                "Advertising_Event_Properties", 2, hci_advertising_event_properties
            ),
            HciParam("Primary_Advertising_Interval_Min", 3, hci_time_p625ms),
            HciParam("Primary_Advertising_Interval_Max", 3, hci_time_p625ms),
            HciParam("Primary_Advertising_Channel_Map", 1, hci_advertising_channel_map),
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address", 6, hci_address),
            HciParam("Advertising_Filter_Policy", 1, hci_advertising_filter_policy),
            HciParam("Advertising_TX_Power", 1, hci_int),
            HciParam("Primary_Advertising_PHY", 1, hci_phy_select),
            HciParam("Secondary_Advertising_Max_Skip", 1, hci_uint),
            HciParam("Secondary_Advertising_PHY", 1, hci_phy_select),
            HciParam("Advertising_SID", 1, hci_uint),
            HciParam("Scan_Request_Notification_Enable", 1, hci_bool),
            HciParam("Primary_Advertising_PHY_Options", 1, hci_phy_options),
            HciParam("Secondary_Advertising_PHY_Options", 1, hci_phy_options),
        ],
        OCF.LE_CONTROLLER.LE_SET_DECISION_DATA: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Decision_Type_Flags", 1, hci_decision_flags),
            HciParam("Decision_Data_Length", 1, hci_uint),
            HciParam("Decision_Data", HciParamIdxRef(-1), hci_str),
        ],
        OCF.LE_CONTROLLER.LE_SET_DECISION_INSTRUCTIONS: [
            HciParam("Num_Tests", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Test_Flags[{}]", 1, hci_test_flags),
                HciParam("Test_Field[{}]", 1, hci_test_fields),
                HciParam("Test_Parameters[{}]", 16, hci_uint),
            ],
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_SUBEVENT_DATA: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Num_Subevents_With_Data", 1, hci_uint),
            [
                HciParamIdxRef(-1),
                HciParam("Subevent[{}]", 1, hci_uint),
                HciParam("Response_Slot_Start[{}]", 1, hci_uint),
                HciParam("Response_Slot_Count[{}]", 1, hci_uint),
                HciParam("Subevent_Data_Length[{}]", 1, hci_uint),
                HciParam("Subevent_Data[{}]", HciParamIdxRef(-1), hci_str),
            ],
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_RESPONSE_DATA: [
            HciParam("Sync_Handle", 2, hci_uint),
            HciParam("Request_Event", 2, hci_uint),
            HciParam("Request_Subevent", 1, hci_uint),
            HciParam("Response_Subevent", 1, hci_uint),
            HciParam("Response_Slot", 1, hci_uint),
            HciParam("Response_Data_Length", 1, hci_uint),
            HciParam("Response_Data", HciParamIdxRef(-1), hci_str),
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_SYNC_SUBEVENT: [
            HciParam("Sync_Handle", 2, hci_uint),
            HciParam(
                "Periodic_Advertising_Properties",
                2,
                hci_periodic_advertising_properties,
            ),
            HciParam("Num_Subevents_To_Sync", 1, hci_uint),
            [HciParamIdxRef(-1), HciParam("Subevent[{}]", 1, hci_uint)],
        ],
        OCF.LE_CONTROLLER.LE_EXTENDED_CREATE_CONNECTION_V2: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Subevent", 1, hci_uint),
            HciParam("Initiator_Filter_Policy", 1, hci_connection_filter_policy),
            HciParam("Own_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address_Type", 1, hci_address_type),
            HciParam("Peer_Address", 6, hci_address),
            HciParam("Initiating_PHYs", 1, hci_phy_mask),
            [
                HciParamIdxRef(-1),
                HciParam("Scan_Interval[{}]", 2, hci_time_p625ms),
                HciParam("Scan_Window[{}]", 2, hci_time_p625ms),
                HciParam("Connection_Interval_Min[{}]", 2, hci_time_1p25ms),
                HciParam("Connection_Interval_Max[{}]", 2, hci_time_1p25ms),
                HciParam("Max_Latency[{}]", 2, hci_uint),
                HciParam("Supervision_Timeout[{}]", 2, hci_time_10ms),
                HciParam("Min_CE_Length[{}]", 2, hci_time_p625ms),
                HciParam("Max_CE_Length[{}]", 2, hci_time_p625ms),
            ],
        ],
        OCF.LE_CONTROLLER.LE_SET_PERIODIC_ADVERTISING_PARAMETERS_V2: [
            HciParam("Advertising_Handle", 1, hci_uint),
            HciParam("Periodic_Advertising_Interval_Min", 2, hci_time_1p25ms),
            HciParam("Periodic_Advertising_Interval_Max", 2, hci_time_1p25ms),
            HciParam(
                "Periodic_Advertising_Properties",
                2,
                hci_periodic_advertising_properties,
            ),
            HciParam("Num_Subevents", 1, hci_uint),
            HciParam("Subevent_Interval", 1, hci_time_1p25ms),
            HciParam("Response_Slot_Delay", 1, hci_time_1p25ms),
            HciParam("Response_Slot_Spacing", 1, hci_time_p125ms),
            HciParam("Num_Response_Slots", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_READ_ALL_REMOTE_FEATURES: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Pages_Requested", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_CS_READ_REMOTE_SUPPORTED_CAPABILITIES: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CS_WRITE_CACHED_REMOTE_SUPPORTED_CAPABILITIES: [
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
            HciParam("T_FCS_Times_Supported", 2, hci_cs_times_fcs),
            HciParam("T_PM_Times_Supported", 2, hci_cs_times),
            HciParam("T_SW_Times_Supported", 1, hci_uint),
            HciParam("TX_SNR_Capability", 1, hci_tx_snr_capability),
        ],
        OCF.LE_CONTROLLER.LE_CS_SECURITY_ENABLE: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CS_SET_DEFAULT_SETTINGS: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Role_Enable", 1, hci_cs_role_mask),
            HciParam("CS_SYNC_Antenna_Selection", 1, hci_uint),
            HciParam("Max_TX_Power", 1, hci_int),
        ],
        OCF.LE_CONTROLLER.LE_CS_READ_REMOTE_FAE_TABLE: [
            HciParam("Connection_Handle", 2, hci_uint)
        ],
        OCF.LE_CONTROLLER.LE_CS_WRITE_CACHED_REMOTE_FAE_TABLE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Remote_FAE_Table", 72, hci_cs_fae_table),
        ],
        OCF.LE_CONTROLLER.LE_CS_CREATE_CONFIG: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Config_ID", 1, hci_uint),
            HciParam("Create_Context", 1, hci_bool),
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
        ],
        OCF.LE_CONTROLLER.LE_CS_REMOVE_CONFIG: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Config_ID", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_CS_SET_CHANNEL_CLASSIFICATION: [
            HciParam("Channel_Classification", 10, hci_cs_channel_map)
        ],
        OCF.LE_CONTROLLER.LE_CS_SET_PROCEDURE_PARAMETERS: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Config_ID", 1, hci_uint),
            HciParam("Max_Procedure_Len", 2, hci_time_p625ms),
            HciParam("Min_Procedure_Interval", 2, hci_uint),
            HciParam("Max_Procedure_Interval", 2, hci_uint),
            HciParam("Max_Procedure_Count", 2, hci_uint),
            HciParam("Min_Subevent_Len", 3, hci_uint),
            HciParam("Max_Subevent_Len", 3, hci_uint),
            HciParam("Tone_Antenna_Config_Selection", 1, hci_uint),
            HciParam("PHY", 1, hci_phy_select),
            HciParam("TX_Power_Delta", 1, hci_int),
            HciParam("Preferred_Peer_Antenna", 1, hci_antenna_select),
            HciParam("SNR_Control_Initiator", 1, hci_tx_snr_select),
            HciParam("SNR_Control_Reflector", 1, hci_tx_snr_select),
        ],
        OCF.LE_CONTROLLER.LE_CS_PROCEDURE_ENABLE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Config_ID", 1, hci_uint),
            HciParam("Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_CS_TEST: [
            HciParam("Main_Mode_Type", 1, hci_uint),
            HciParam("Sub_Mode_Type", 1, hci_uint),
            HciParam("Main_Mode_Repetition", 1, hci_uint),
            HciParam("Mode_0_Steps", 1, hci_uint),
            HciParam("Role", 1, hci_cs_role_select),
            HciParam("RTT_Type", 1, hci_rtt_type),
            HciParam("CS_SYNC_PHY", 1, hci_cs_sync_phy_select),
            HciParam("CS_SYNC_Antenna_Selection", 1, hci_uint),
            HciParam("Subevent_Len", 3, hci_uint),
            HciParam("Subevent_Interval", 2, hci_time_p625ms),
            HciParam("Max_Num_Subevents", 1, hci_uint),
            HciParam("Transmit_Power_Level", 1, hci_int),
            HciParam("T_IP1_Time", 1, hci_uint),
            HciParam("T_IP2_Time", 1, hci_uint),
            HciParam("T_FCS_Time", 1, hci_uint),
            HciParam("T_PM_Time", 1, hci_uint),
            HciParam("T_SW_Time", 1, hci_uint),
            HciParam("Tone_Antenna_Config_Selection", 1, hci_uint),
            HciParam("Reserved", 1, hci_uint),
            HciParam("SNR_Control_Initiator", 1, hci_tx_snr_select),
            HciParam("SNR_Control_Reflector", 1, hci_tx_snr_select),
            HciParam("DRBG_None", 2, hci_uint),
            HciParam("Channel_Map_Repetition", 1, hci_uint),
            HciParam("Override_Config", 2, hci_cs_override_config),
            HciParam("Override_Parameters_Length", 1, hci_uint),
            HciParam("Override_Parameters_Data", HciParamIdxRef(-1), hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_SET_HOST_FEATURE_V2: [
            HciParam("Bit_Number", 2, hci_uint),
            HciParam("Bit_Enable", 1, hci_bool),
        ],
        OCF.LE_CONTROLLER.LE_ADD_DEVICE_TO_MONITORED_ADVERTISERS_LIST: [
            HciParam("Address_Type", 1, hci_address_type),
            HciParam("Address", 6, hci_address),
            HciParam("RSSI_Threshold_Low", 1, hci_int),
            HciParam("RSSI_Threshold_High", 1, hci_int),
            HciParam("Timeout", 1, hci_uint),
        ],
        OCF.LE_CONTROLLER.LE_REMOVE_DEVICE_FROM_MONITORED_ADVERTISERS_LIST: [
            HciParam("Address_Type", 1, hci_address_type),
            HciParam("Address", 6, hci_address),
        ],
        OCF.LE_CONTROLLER.LE_ENABLE_MONITORING_ADVERTISERS: [
            HciParam("Enable", 1, hci_bool)
        ],
        OCF.LE_CONTROLLER.LE_FRAME_SPACE_UPDATE: [
            HciParam("Connection_Handle", 2, hci_uint),
            HciParam("Frame_Space_Min", 2, hci_uint),
            HciParam("Frame_Space_Max", 2, hci_uint),
            HciParam("PHYs", 1, hci_phy_mask),
            HciParam("Spacing_Types", 2, hci_spacing_types),
        ],
    },
}


def get_params(ogf: OGF, ocf: OCF) -> List[HciParam]:
    """Get packet parameter structure by OGF/OCF.

    Parameters
    ----------
    ogf : OGF
        Operation Group Field.
    ocf : OCF
        Operation Control Field.

    Returns
    -------
    List[HciParam]
        Packet parameter stucture.

    """
    return _COMMAND_PACKET_PARAMS[ogf].get(ocf, None)
