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
"""DOCSTRING"""
from enum import Enum
from dataclasses import dataclass

ADI_PORT_BAUD_RATE = 115200


class PacketType(Enum):
    """
    BT Standard Packet Types
    """

    COMMAND = 0x1
    ASYNC = 0x2
    SYNC = 0x3
    EVENT = 0x4
    EXTENDED = 0x9


class OGF(Enum):
    """
    BLE Specified Command OFG Values
    """

    NOP = 0x00
    LINK_CONTROL = 0x01
    LINK_POLICY = 0x02
    CONTROLLER = 0x03
    INFORMATIONAL = 0x04
    STATUS = 0x05
    TESTING = 0x06
    LE_CONTROLLER = 0x08
    VENDOR_SPEC = 0x3F


class _NOpOCF(Enum):
    """DOCSTRING"""

    NOP = 0x00


class _LinkControlOCF(Enum):
    """
    BLE Specified Link Control Command OCF Values
    """

    DISCONNECT = 0x06
    READ_REMOTE_VER_INFO = 0x1D


class _ControllerOCF(Enum):
    """DOCSTRING"""

    SET_EVENT_MASK = 0x01
    RESET = 0x03
    READ_TX_PWR_LVL = 0x2D
    SET_CONTROLLER_TO_HOST_FC = 0x31
    HOST_BUFFER_SIZE = 0x33
    HOST_NUM_CMPL_PKTS = 0x35
    SET_EVENT_MASK_PAGE2 = 0x63
    READ_AUTH_PAYLOAD_TO = 0x7B
    WRITE_AUTH_PAYLOAD_TO = 0x7C
    CONFIG_DATA_PATH = 0x83


class _InformationalOCF(Enum):
    """DOCSTRING"""

    READ_LOCAL_VER_INFO = 0x01
    READ_LOCAL_SUP_CMDS = 0x02
    READ_LOCAL_SUP_FEAT = 0x03
    READ_BUF_SIZE = 0x05
    READ_BD_ADDR = 0x09
    READ_LOCAL_SUP_CODECS = 0x0D
    READ_LOCAL_SUP_CODEC_CAP = 0x0E
    READ_LOCAL_SUP_CONTROLLER_DLY = 0x0F


class _StatusOCF(Enum):
    """DOCSTRING"""

    READ_RSSI = 0x05


class _LEControllerOCF(Enum):
    """DOCSTRING"""

    SET_EVENT_MASK = 0x01
    READ_BUF_SIZE = 0x02
    READ_LOCAL_SUP_FEAT = 0x03
    SET_RAND_ADDR = 0x05
    SET_ADV_PARAM = 0x06
    READ_ADV_TX_POWER = 0x07
    SET_ADV_DATA = 0x08
    SET_SCAN_RESP_DATA = 0x09
    SET_ADV_ENABLE = 0x0A
    SET_SCAN_PARAM = 0x0B
    SET_SCAN_ENABLE = 0x0C
    CREATE_CONN = 0x0D
    CREATE_CONN_CANCEL = 0x0E
    READ_WHITE_LIST_SIZE = 0x0F
    CLEAR_WHITE_LIST = 0x10
    ADD_DEV_WHITE_LIST = 0x11
    REMOVE_DEV_WHITE_LIST = 0x12
    CONN_UPDATE = 0x13
    SET_HOST_CHAN_CLASS = 0x14
    READ_CHAN_MAP = 0x15
    READ_REMOTE_FEAT = 0x16
    ENCRYPT = 0x17
    RAND = 0x18
    START_ENCRYPTION = 0x19
    LTK_REQ_REPL = 0x1A
    LTK_REQ_NEG_REPL = 0x1B
    READ_SUP_STATES = 0x1C
    RECEIVER_TEST = 0x1D
    TRANSMITTER_TEST = 0x1E
    TEST_END = 0x1F
    REM_CONN_PARAM_REP = 0x20
    REM_CONN_PARAM_NEG_REP = 0x21
    SET_DATA_LEN = 0x22
    READ_DEF_DATA_LEN = 0x23
    WRITE_DEF_DATA_LEN = 0x24
    READ_LOCAL_P256_PUB_KEY = 0x25
    GENERATE_DHKEY = 0x26
    ADD_DEV_RES_LIST = 0x27
    REMOVE_DEV_RES_LIST = 0x28
    CLEAR_RES_LIST = 0x29
    READ_RES_LIST_SIZE = 0x2A
    READ_PEER_RES_ADDR = 0x2B
    READ_LOCAL_RES_ADDR = 0x2C
    SET_ADDR_RES_ENABLE = 0x2D
    SET_RES_PRIV_ADDR_TO = 0x2E
    READ_MAX_DATA_LEN = 0x2F
    READ_PHY = 0x30
    SET_DEF_PHY = 0x31
    SET_PHY = 0x32
    ENHANCED_RECEIVER_TEST = 0x33
    ENHANCED_TRANSMITTER_TEST = 0x34
    SET_ADV_SET_RAND_ADDR = 0x35
    SET_EXT_ADV_PARAM = 0x36
    SET_EXT_ADV_DATA = 0x37
    SET_EXT_SCAN_RESP_DATA = 0x38
    SET_EXT_ADV_ENABLE = 0x39
    READ_MAX_ADV_DATA_LEN = 0x3A
    READ_NUM_SUP_ADV_SETS = 0x3B
    REMOVE_ADV_SET = 0x3C
    CLEAR_ADV_SETS = 0x3D
    SET_PER_ADV_PARAM = 0x3E
    SET_PER_ADV_DATA = 0x3F
    SET_PER_ADV_ENABLE = 0x40
    SET_EXT_SCAN_PARAM = 0x41
    SET_EXT_SCAN_ENABLE = 0x42
    EXT_CREATE_CONN = 0x43
    PER_ADV_CREATE_SYNC = 0x44
    PER_ADV_CREATE_SYNC_CANCEL = 0x45
    PER_ADV_TERM_SYNC = 0x46
    ADD_DEV_PER_ADV_LIST = 0x47
    REMOVE_DEV_PER_ADV_LIST = 0x48
    CLEAR_PER_ADV_LIST = 0x49
    READ_PER_ADV_LIST_SIZE = 0x4A
    READ_TX_POWER = 0x4B
    READ_RF_PATH_COMP = 0x4C
    WRITE_RF_PATH_COMP = 0x4D
    SET_PRIVACY_MODE = 0x4E
    RECEIVER_TEST_V3 = 0x4F
    TRANSMITTER_TEST_V3 = 0x50
    SET_CONNLESS_CTE_TX_PARAMS = 0x51
    SET_CONNLESS_CTE_TX_ENABLE = 0x52
    SET_CONNLESS_IQ_SAMP_ENABLE = 0x53
    SET_CONN_CTE_RX_PARAMS = 0x54
    SET_CONN_CTE_TX_PARAMS = 0x55
    CONN_CTE_REQ_ENABLE = 0x56
    CONN_CTE_RSP_ENABLE = 0x57
    READ_ANTENNA_INFO = 0x58
    SET_PER_ADV_RCV_ENABLE = 0x59
    PER_ADV_SYNC_TRANSFER = 0x5A
    PER_ADV_SET_INFO_TRANSFER = 0x5B
    SET_PAST_PARAM = 0x5C
    SET_DEFAULT_PAST_PARAM = 0x5D
    GENERATE_DHKEY_V2 = 0x5E
    MODIFY_SLEEP_CLK_ACC = 0x5F
    READ_BUF_SIZE_V2 = 0x60
    READ_ISO_TX_SYNC = 0x61
    SET_CIG_PARAMS = 0x62
    SET_CIG_PARAMS_TEST = 0x63
    CREATE_CIS = 0x64
    REMOVE_CIG = 0x65
    ACCEPT_CIS_REQ = 0x66
    REJECT_CIS_REQ = 0x67
    CREATE_BIG = 0x68
    CREATE_BIG_TEST = 0x69
    TERMINATE_BIG = 0x6A
    BIG_CREATE_SYNC = 0x6B
    BIG_TERMINATE_SYNC = 0x6C
    REQUEST_PEER_SCA = 0x6D
    SETUP_ISO_DATA_PATH = 0x6E
    REMOVE_ISO_DATA_PATH = 0x6F
    ISO_TX_TEST = 0x70
    ISO_RX_TEST = 0x71
    ISO_READ_TEST_COUNTERS = 0x72
    ISO_TEST_END = 0x73
    SET_HOST_FEATURE = 0x74
    READ_ISO_LINK_QUAL = 0x75
    READ_ENHANCED_TX_POWER = 0x76
    READ_REMOTE_TX_POWER = 0x77
    SET_PATH_LOSS_REPORTING_PARAMS = 0x78
    SET_PATH_LOSS_REPORTING_ENABLE = 0x79
    SET_TX_POWER_REPORT_ENABLE = 0x7A


class _VendorSpecificOCF(Enum):
    """DOCSTRING"""

    SET_SCAN_CH_MAP = 0x3E0
    SET_EVENT_MASK = 0x3E1
    SET_RSRC_MGR_MODE = 0x3E2
    ENA_ACL_SINK = 0x3E3
    GENERATE_ACL = 0x3E4
    ENA_AUTO_GEN_ACL = 0x3E5
    SET_TX_TEST_ERR_PATT = 0x3E6
    SET_CONN_OP_FLAGS = 0x3E7
    SET_P256_PRIV_KEY = 0x3E8
    GET_PER_CHAN_MAP = 0x3DE
    SET_HCI_SUP_CMD = 0x3DF
    GET_ACL_TEST_REPORT = 0x3E9
    SET_LOCAL_MIN_USED_CHAN = 0x3EA
    GET_PEER_MIN_USED_CHAN = 0x3EB
    VALIDATE_PUB_KEY_MODE = 0x3EC
    SET_BD_ADDR = 0x3F0
    GET_RAND_ADDR = 0x3F1
    SET_LOCAL_FEAT = 0x3F2
    SET_OP_FLAGS = 0x3F3
    SET_ADV_TX_PWR = 0x3F5
    SET_CONN_TX_PWR = 0x3F6
    SET_ENC_MODE = 0x3F7
    SET_CHAN_MAP = 0x3F8
    SET_DIAG_MODE = 0x3F9
    SET_SNIFFER_ENABLE = 0x3CD
    GET_PDU_FILT_STATS = 0x3F4
    GET_SYS_STATS = 0x3FA
    GET_ADV_STATS = 0x3FB
    GET_SCAN_STATS = 0x3FC
    GET_CONN_STATS = 0x3FD
    GET_TEST_STATS = 0x3FE
    GET_POOL_STATS = 0x3FF
    SET_AUX_DELAY = 0x3D0
    SET_EXT_ADV_FRAG_LEN = 0x3D1
    SET_EXT_ADV_PHY_OPTS = 0x3D2
    SET_EXT_ADV_DEF_PHY_OPTS = 0x3D3
    SET_EXT_SCAN_PHY_OPTS = 0x3D4
    GENERATE_ISO = 0x3D5
    GET_ISO_TEST_REPORT = 0x3D6
    ENA_ISO_SINK = 0x3D7
    ENA_AUTO_GEN_ISO = 0x3D8
    GET_CIS_STATS = 0x3D9
    GET_AUX_ADV_STATS = 0x3DA
    GET_AUX_SCAN_STATS = 0x3DB
    GET_PER_SCAN_STATS = 0x3DC
    SET_CONN_PHY_TX_PWR = 0x3DD
    REG_WRITE = 0x300
    REG_READ = 0x301
    RESET_CONN_STATS = 0x302
    TX_TEST = 0x303
    RESET_TEST_STATS = 0x304
    RX_TEST = 0x305
    GET_RSSI = 0x306
    PHY_EN = 0x307
    PHY_DIS = 0x308


class PubKeyValidateMode(Enum):
    """DOCSTRING"""

    ALT1 = 0x0
    ALT2 = 0x1


@dataclass
class OCF:
    """DOCSTRING"""

    NOP = _NOpOCF
    LINK_CONTROL = _LinkControlOCF
    LINK_POLICY = None
    CONTROLLER = _ControllerOCF
    INFORMATIONAL = _InformationalOCF
    STATUS = _StatusOCF
    TESTING = None
    LE_CONTROLLER = _LEControllerOCF
    VENDOR_SPEC = _VendorSpecificOCF
