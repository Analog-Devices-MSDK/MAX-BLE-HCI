# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module contains the parameter structures for HCI ACL packets.

This module contains definitions for the parameter structures
of all HCI ACL L2CAP signaling packets. As it is part of an
internal package, it is not intended for external use.

"""
from typing import Dict, Iterator, List
from ...packet_codes.acl import L2CAPSignalingCodes
from ..types import *
from ..params import HciParam, HciParamIdxRef

_ACL_PACKET_PARAMS: Dict[L2CAPSignalingCodes, List[HciParam]] = {
    L2CAPSignalingCodes.L2CAP_COMMAND_REJECT_RSP: [
        HciParam("Reason", 2, hci_l2cap_reason),
        HciParam("Reason_Data", None, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_CONNECTION_REQ: [
        HciParam("PSM", -2, hci_uint),
        HciParam("Source_CID", 2, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_CONNECTION_RSP: [
        HciParam("Destination_CID", 2, hci_uint),
        HciParam("Source_CID", 2, hci_uint),
        HciParam("Result", 2, hci_l2cap_connection_result),
        HciParam("Status", 2, hci_l2cap_status)
    ],
    L2CAPSignalingCodes.L2CAP_CONFIGURATION_REQ: [
        HciParam("Source_CID", 2, hci_uint),
        HciParam("Flags", 2, hci_uint),
        HciParam("Configuration_Options", None, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_CONFIGURATION_RSP: [
        HciParam("Source_CID", 2, hci_uint),
        HciParam("Flags", 2, hci_uint),
        HciParam("Result", 2, hci_l2cap_configure_result),
        HciParam("Config", None, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_DISCONNECTION_REQ: [
        HciParam("Destination_CID", 2, hci_uint),
        HciParam("Source_CID", 2, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_DISCONNECTION_RSP: [
        HciParam("Destination_CID", 2, hci_uint),
        HciParam("Source_CID", 2, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_ECHO_REQ: [
        HciParam("Echo_Data", None, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_ECHO_RSP: [
        HciParam("Echo_Data", None, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_INFORMATION_REQ: [
        HciParam("Info_Type", 2, hci_l2cap_info_type)
    ],
    L2CAPSignalingCodes.L2CAP_INFORMATION_RSP: [
        HciParam("Info_Type", 2, hci_l2cap_info_type),
        HciParam("Supported", 2, hci_bool),
        HciParam("Info", None, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_CONNECTION_PARAMETER_UPDATE_REQ: [
        HciParam("Interval_Min", 2, hci_uint),
        HciParam("Interval_Max", 2, hci_uint),
        HciParam("Latency", 2, hci_uint),
        HciParam("Timeout", 2, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_CONNECTION_PARAMETER_UPDATE_RSP: [
        HciParam("Parameters_OK", 2, hci_bool)
    ],
    L2CAPSignalingCodes.L2CAP_LE_CREDIT_BASED_CONNECTION_REQ: [
        HciParam("SPSM", 2, hci_uint),
        HciParam("Source_CID", 2, hci_uint),
        HciParam("MTU", 2, hci_uint),
        HciParam("MPS", 2, hci_uint),
        HciParam("Initial_Credits", 2, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_LE_CREDIT_BASED_CONNECTION_RSP: [
        HciParam("Destination_CID", 2, hci_uint),
        HciParam("MTU", 2, hci_uint),
        HciParam("MPS", 2, hci_uint),
        HciParam("Initial_Credits", 2, hci_uint),
        HciParam("Result", 2, hci_l2cap_credit_connection_result)
    ],
    L2CAPSignalingCodes.L2CAP_FLOW_CONTROL_CREDIT_IND: [
        HciParam("CID", 2, hci_uint),
        HciParam("Credits", 2, hci_uint)
    ],
    L2CAPSignalingCodes.L2CAP_CREDIT_BASED_CONNECTION_REQ: [
        HciParam("SPSM", 2, hci_uint),
        HciParam("MTU", 2, hci_uint),
        HciParam("MPS", 2, hci_uint),
        HciParam("Initial_Credits", 2, hci_uint),
        [
            HciParamIdxRef(None),
            HciParam("Source_CID[{}]", 2, hci_uint)
        ]
    ],
    L2CAPSignalingCodes.L2CAP_CREDIT_BASED_CONNECTION_RSP: [
        HciParam("MTU", 2, hci_uint),
        HciParam("MPS", 2, hci_uint),
        HciParam("Initial_Credits", 2, hci_uint),
        HciParam("Result", 2, hci_l2cap_credit_connection_result),
        [
            HciParamIdxRef(None),
            HciParam("Destination_CID[{}]", 2, hci_uint)
        ]
    ],
    L2CAPSignalingCodes.L2CAP_CREDIT_BASED_RECONFIGURE_REQ: [
        HciParam("MTU", 2, hci_uint),
        HciParam("MPS", 2, hci_uint),
        [
            HciParamIdxRef(None),
            HciParam("Destination_CID[{}]", 2, hci_uint)
        ]
    ],
    L2CAPSignalingCodes.L2CAP_CREDIT_BASED_RECONFIGURE_RSP: [
        HciParam("Result", 2, hci_l2cap_credit_reconfigure_result)
    ]
}

def get_params(code: L2CAPSignalingCodes) -> List[HciParam]:
    """Get packet parameter structure by code.

    Parameters
    ----------
    code : L2CAPSignalingCodes
        L2CAP signaling code.

    Returns
    -------
    List[HciParam]
        Packet parameter structure.

    """
    return _ACL_PACKET_PARAMS.get(code, None)
