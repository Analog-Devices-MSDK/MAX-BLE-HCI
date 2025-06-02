# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module contains the parameter structures for ACL ATT packets.

This module contains definitions for the parameter structures
of all ACL ATT protocol packets. As it is part of an internal
package, it is not intended for external use.

"""
# pylint: disable=wildcard-import, too-many-lines, unused-wildcard-import
from typing import Dict, List
from ...packet_codes.acl import ATTProtocolCodes
from ..types import *
from ..params import HciParam, HciParamIdxRef

_ACL_ATT_PARAMS: Dict[ATTProtocolCodes, List[HciParam]] = {
    ATTProtocolCodes.ATT_ERROR_RSP: [
        HciParam("Request_Opcode_In_Error", 1, hci_hexint),
        HciParam("Attribute_Handle_In_Error", 2, hci_hexint),
        HciParam("Error_Code", 1, hci_att_error_code),
    ],
    ATTProtocolCodes.ATT_EXCHANGE_MTU_REQ: [HciParam("Client_Rx_MTU", 2, hci_uint)],
    ATTProtocolCodes.ATT_EXCHANGE_MTU_RSP: [HciParam("Server_Rx_MTU", 2, hci_uint)],
    ATTProtocolCodes.ATT_FIND_INFORMATION_REQ: [
        HciParam("Starting_Handle", 2, hci_hexint),
        HciParam("Ending_Handle", 2, hci_hexint),
    ],
    ATTProtocolCodes.ATT_FIND_INFORMATION_RSP: [HciParam("Info", None, hci_att_info)],
    ATTProtocolCodes.ATT_FIND_BY_TYPE_VALUE_REQ: [
        HciParam("Starting_Handle", 2, hci_hexint),
        HciParam("Ending_Handle", 2, hci_hexint),
        HciParam("Attribute_Type", 2, hci_hexint),
        HciParam("Attribute_Value", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_FIND_BY_TYPE_VALUE_RSP: [
        [
            HciParamIdxRef(None),
            HciParam("Found_Attribute_Handle[{}]", 2, hci_hexint),
            HciParam("Group_End_Handle[{}]", 2, hci_hexint),
        ]
    ],
    ATTProtocolCodes.ATT_READ_BY_TYPE_REQ: [
        HciParam("Starting_Handle", 2, hci_hexint),
        HciParam("Ending_Handle", 2, hci_hexint),
        HciParam("Attribute_Type", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_READ_BY_TYPE_RSP: [
        HciParam("Length", 1, hci_uint),
        [
            HciParamIdxRef(None),
            HciParam("Attribute_Data[{}]", HciParamIdxRef(0), hci_att_data),
        ],
    ],
    ATTProtocolCodes.ATT_READ_REQ: [HciParam("Attribute_Handle", 2, hci_hexint)],
    ATTProtocolCodes.ATT_READ_RSP: [HciParam("Attribute_Value", None, hci_hexint)],
    ATTProtocolCodes.ATT_READ_BLOB_REQ: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Value_Offset", 2, hci_uint),
    ],
    ATTProtocolCodes.ATT_READ_BLOB_RSP: [
        HciParam("Part_Attribute_Value", None, hci_hexint)
    ],
    ATTProtocolCodes.ATT_READ_MULTIPLE_REQ: [
        [HciParamIdxRef(None), HciParam("Handle[{}]", 2, hci_hexint)]
    ],
    ATTProtocolCodes.ATT_READ_MULTIPLE_RSP: [
        HciParam("Set_Of_Values", None, hci_hexstr)
    ],
    ATTProtocolCodes.ATT_READ_BY_GROUP_TYPE_REQ: [
        HciParam("Starting_Handle", 2, hci_hexint),
        HciParam("Ending_Handle", 2, hci_hexint),
        HciParam("Attribute_Group_Type", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_READ_BY_GROUP_TYPE_RSP: [
        HciParam("Length", 1, hci_uint),
        [
            HciParamIdxRef(None),
            HciParam("Attribute_Data[{}]", HciParamIdxRef(0), hci_att_group_data),
        ],
    ],
    ATTProtocolCodes.ATT_READ_MULTIPLE_VARIABLE_REQ: [
        [HciParamIdxRef(None), HciParam("Handle[{}]", 2, hci_hexint)]
    ],
    ATTProtocolCodes.ATT_READ_MULTIPLE_VARIABLE_RSP: [
        [
            HciParamIdxRef(None),
            HciParam("Length[{}]", 2, hci_uint),
            HciParam("Attribute_Value[{}]", HciParamIdxRef(-1), hci_hexint),
        ]
    ],
    ATTProtocolCodes.ATT_WRITE_REQ: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Attribute_Value", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_WRITE_CMD: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Attribute_Value", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_SIGNED_WRITE_CMD: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Attribute_Value", -12, hci_hexint),
        HciParam("Authentication_Signature", 12, hci_hexint),
    ],
    ATTProtocolCodes.ATT_PREPARE_WRITE_REQ: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Value_Offset", 2, hci_uint),
        HciParam("Part_Attribute_Value", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_PREPARE_WRITE_RSP: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Value_Offset", 2, hci_uint),
        HciParam("Part_Attribute_Value", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_EXECUTE_WRITE_REQ: [HciParam("Execute", 1, hci_bool)],
    ATTProtocolCodes.ATT_HANDLE_VALUE_NTF: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Attribute_Value", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_HANDLE_VALUE_IND: [
        HciParam("Attribute_Handle", 2, hci_hexint),
        HciParam("Attribute_Value", None, hci_hexint),
    ],
    ATTProtocolCodes.ATT_MULTIPLE_HANDLE_VALUE_NTF: [
        [
            HciParamIdxRef(None),
            HciParam("Attribute_Handle[{}]", 2, hci_hexint),
            HciParam("Length[{}]", 2, hci_uint),
            HciParam("Attribute_Value", HciParamIdxRef(-1), hci_hexint),
        ]
    ],
}


def get_params(code: ATTProtocolCodes) -> List[HciParam]:
    """Get packet parameter structure by code.

    Parameters
    ----------
    code : ATTProtocolCodes
        ATT protocol opcode.

    Returns
    -------
    List[HciParam]
        Packet parameter structure.

    """
    return _ACL_ATT_PARAMS.get(code, None)
