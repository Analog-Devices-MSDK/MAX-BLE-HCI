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
from dataclasses import dataclass
from enum import Enum


class PacketType(Enum):
    """BT standard packet types."""

    COMMAND = 0x1
    """Command packet type."""

    ASYNC = 0x2
    """Asynchronous Connection-Less packet type."""

    SYNC = 0x3
    """Synchronous packet type.
    
    .. note::
        Synchronous data packets are not used in BLE.
    
    """

    EVENT = 0x4
    """Event packet type."""

    EXTENDED = 0x9
    """Extended command packet type."""


class OGF(Enum):
    """BLE-defined Opcode Group Field values."""

    NOP = 0x00
    """No operation."""

    LINK_CONTROL = 0x01
    """Link control group field."""

    LINK_POLICY = 0x02
    """Link policy group field."""

    CONTROLLER = 0x03
    """Controller group field."""

    INFORMATIONAL = 0x04
    """Informational group field."""

    STATUS = 0x05
    """Status group field."""

    TESTING = 0x06
    """Testing group field."""

    LE_CONTROLLER = 0x08
    """LE controller group field."""

    VENDOR_SPEC = 0x3F
    """Vendor specific group field."""


class NOpOCF(Enum):
    """BLE-defined NOP group Opcode Command Field values."""

    NOP = 0x00
    """No operation."""


class LinkControlOCF(Enum):
    """BLE-defined Link Control group Opcode Command Field values"""

    DISCONNECT = 0x06
    """Disconnect command."""

    READ_REMOTE_VER_INFO = 0x1D
    """Read remote version info command."""


class ControllerOCF(Enum):
    """BLE-defined Controller group Opcode Command Field values."""

    SET_EVENT_MASK = 0x01
    """Set event mask command."""

    RESET = 0x03
    """Reset command."""

    READ_TX_PWR_LVL = 0x2D
    """Read TX power level command."""

    SET_CONTROLLER_TO_HOST_FC = 0x31
    """Set controller to host flow control command."""

    HOST_BUFFER_SIZE = 0x33
    """Host buffer size command."""

    HOST_NUM_CMPL_PKTS = 0x35
    """Host number of completed packets command."""

    SET_EVENT_MASK_PAGE2 = 0x63
    """Set event mask page 2 command."""

    READ_AUTH_PAYLOAD_TO = 0x7B
    """Read authenticated payload timeout command."""

    WRITE_AUTH_PAYLOAD_TO = 0x7C
    """Write authenticated payload timeout command."""

    CONFIG_DATA_PATH = 0x83
    """Configure data path command."""


class InformationalOCF(Enum):
    """BLE-defined Information group Opcode Command Field values."""

    READ_LOCAL_VER_INFO = 0x01
    """Read local version information command."""

    READ_LOCAL_SUP_CMDS = 0x02
    """Read local supported commands command."""

    READ_LOCAL_SUP_FEAT = 0x03
    """Read local supported features command."""

    READ_BUF_SIZE = 0x05
    """Read buffer size command."""

    READ_BD_ADDR = 0x09
    """Read BD address command."""

    READ_LOCAL_SUP_CODECS = 0x0D
    """Read local supported codecs command."""

    READ_LOCAL_SUP_CODEC_CAP = 0x0E
    """Read local supported codec capabilities command."""

    READ_LOCAL_SUP_CONTROLLER_DLY = 0x0F
    """Read local supported controller delay command."""


class StatusOCF(Enum):
    """BLE-defined Status group Opcode Command Field values."""

    READ_RSSI = 0x05
    """Read RSSI command."""


class LEControllerOCF(Enum):
    """BLE-defined LE Controller group Opcode Command Field values."""

    SET_EVENT_MASK = 0x01
    """Set event mask command."""

    READ_BUF_SIZE = 0x02
    """Read buffer size command."""

    READ_LOCAL_SUP_FEAT = 0x03
    """Read local supported features command."""

    SET_RAND_ADDR = 0x05
    """Set random address command."""

    SET_ADV_PARAM = 0x06
    """Set advertising parameters command."""

    READ_ADV_TX_POWER = 0x07
    """Read advertising physical channel TX power command."""

    SET_ADV_DATA = 0x08
    """Set advertising data command."""

    SET_SCAN_RESP_DATA = 0x09
    """Set scan response data command."""

    SET_ADV_ENABLE = 0x0A
    """Set advertising enable command."""

    SET_SCAN_PARAM = 0x0B
    """Set scan parameters command."""

    SET_SCAN_ENABLE = 0x0C
    """Set scan enable command."""

    CREATE_CONN = 0x0D
    """Create connection command."""

    CREATE_CONN_CANCEL = 0x0E
    """Create connection cancel command."""

    READ_WHITE_LIST_SIZE = 0x0F
    """Read fileter accept list size command."""

    CLEAR_WHITE_LIST = 0x10
    """Clear filter accept list command."""

    ADD_DEV_WHITE_LIST = 0x11
    """Add device to filter accept list command."""

    REMOVE_DEV_WHITE_LIST = 0x12
    """Remove device from filter accept list command."""

    CONN_UPDATE = 0x13
    """Connection update command."""

    SET_HOST_CHAN_CLASS = 0x14
    """Set host channel classification command."""

    READ_CHAN_MAP = 0x15
    """Read channel map command."""

    READ_REMOTE_FEAT = 0x16
    """Read remove features command."""

    ENCRYPT = 0x17
    """Encrypt command."""

    RAND = 0x18
    """Rand command."""

    START_ENCRYPTION = 0x19
    """Enable encryption command."""

    LTK_REQ_REPL = 0x1A
    """Long term key requency reply command."""

    LTK_REQ_NEG_REPL = 0x1B
    """Long term key request negative reply command."""

    READ_SUP_STATES = 0x1C
    """Read supported states command."""

    RECEIVER_TEST = 0x1D
    """Receiver test command."""

    TRANSMITTER_TEST = 0x1E
    """Transmitter test command."""

    TEST_END = 0x1F
    """Test end command."""

    REM_CONN_PARAM_REP = 0x20
    """Remote connection parameter request reply command."""

    REM_CONN_PARAM_NEG_REP = 0x21
    """Remote connection parameter request negative reply command."""

    SET_DATA_LEN = 0x22
    """Set data length command."""

    READ_DEF_DATA_LEN = 0x23
    """Read suggested default data length command."""

    WRITE_DEF_DATA_LEN = 0x24
    """Write suggested default data length command."""

    READ_LOCAL_P256_PUB_KEY = 0x25
    """Read local P-256 public key command."""

    GENERATE_DHKEY = 0x26
    """Generate DHKey command."""

    ADD_DEV_RES_LIST = 0x27
    """Add device to resolving list command."""

    REMOVE_DEV_RES_LIST = 0x28
    """Remove device from resolving list command."""

    CLEAR_RES_LIST = 0x29
    """Clear resolving list command."""

    READ_RES_LIST_SIZE = 0x2A
    """Read resolving list size command."""

    READ_PEER_RES_ADDR = 0x2B
    """Read peer resolvable address command."""

    READ_LOCAL_RES_ADDR = 0x2C
    """Read local resolvable address command."""

    SET_ADDR_RES_ENABLE = 0x2D
    """Set address resolution enable command."""

    SET_RES_PRIV_ADDR_TO = 0x2E
    """Set resolvable private address timeout command."""

    READ_MAX_DATA_LEN = 0x2F
    """Read maximum data length command."""

    READ_PHY = 0x30
    """Read PHY command."""

    SET_DEF_PHY = 0x31
    """Set default PHY command."""

    SET_PHY = 0x32
    """Set PHY command."""

    ENHANCED_RECEIVER_TEST = 0x33
    """Enhanced receiver test command."""

    ENHANCED_TRANSMITTER_TEST = 0x34
    """Enhanced transmitter test command."""

    SET_ADV_SET_RAND_ADDR = 0x35
    """Set advertising set random address command."""

    SET_EXT_ADV_PARAM = 0x36
    """Set extended advertising parameters command."""

    SET_EXT_ADV_DATA = 0x37
    """Set extended advertising data command."""

    SET_EXT_SCAN_RESP_DATA = 0x38
    """Set extended scan response data command."""

    SET_EXT_ADV_ENABLE = 0x39
    """Set extended advertising enable command."""

    READ_MAX_ADV_DATA_LEN = 0x3A
    """Read maximum advertising data length command."""

    READ_NUM_SUP_ADV_SETS = 0x3B
    """Read number of supported advertising sets command."""

    REMOVE_ADV_SET = 0x3C
    """Remove advertising set command."""

    CLEAR_ADV_SETS = 0x3D
    """Clear advertising sets command."""

    SET_PER_ADV_PARAM = 0x3E
    """Set periodic advertising parameters command."""

    SET_PER_ADV_DATA = 0x3F
    """Set periodic advertising data command."""

    SET_PER_ADV_ENABLE = 0x40
    """Set periodic advertising enable command."""

    SET_EXT_SCAN_PARAM = 0x41
    """Set extended scan parameters command."""

    SET_EXT_SCAN_ENABLE = 0x42
    """Set extended scan enable command."""

    EXT_CREATE_CONN = 0x43
    """Extended create connection command."""

    PER_ADV_CREATE_SYNC = 0x44
    """Periodic advertising create sync command."""

    PER_ADV_CREATE_SYNC_CANCEL = 0x45
    """Periodic advertising create sync cancel command."""

    PER_ADV_TERM_SYNC = 0x46
    """Periodic advertising terminate sync command."""

    ADD_DEV_PER_ADV_LIST = 0x47
    """Add devoce to periodic advertiser list command."""

    REMOVE_DEV_PER_ADV_LIST = 0x48
    """Remove device from periodic advertiser list command."""

    CLEAR_PER_ADV_LIST = 0x49
    """Clear periodic advertiser list command."""

    READ_PER_ADV_LIST_SIZE = 0x4A
    """Read periodic advertising list size command."""

    READ_TX_POWER = 0x4B
    """Read TX power command."""

    READ_RF_PATH_COMP = 0x4C
    """Read RF path compensation command."""

    WRITE_RF_PATH_COMP = 0x4D
    """Write RF path compensation command."""

    SET_PRIVACY_MODE = 0x4E
    """Set privacy mode command."""

    RECEIVER_TEST_V3 = 0x4F
    """Receiver test version3 command."""

    TRANSMITTER_TEST_V3 = 0x50
    """Transmitter test version3 command."""

    SET_CONNLESS_CTE_TX_PARAMS = 0x51
    """Set connectionless CTE transmit parameters command."""

    SET_CONNLESS_CTE_TX_ENABLE = 0x52
    """Set connectionless CTE transmit enable command."""

    SET_CONNLESS_IQ_SAMP_ENABLE = 0x53
    """Set connectionless IQ sampling enable command."""

    SET_CONN_CTE_RX_PARAMS = 0x54
    """Set connection CTE receive parameters command."""

    SET_CONN_CTE_TX_PARAMS = 0x55
    """Set connection CTE transmit parameters command."""

    CONN_CTE_REQ_ENABLE = 0x56
    """Connection CTE request enable command."""

    CONN_CTE_RSP_ENABLE = 0x57
    """Connection CTE response enable command."""

    READ_ANTENNA_INFO = 0x58
    """Read antenna information command."""

    SET_PER_ADV_RCV_ENABLE = 0x59
    """Set periodic advertising receive enable command."""

    PER_ADV_SYNC_TRANSFER = 0x5A
    """Periodic advertising sync transfer command."""

    PER_ADV_SET_INFO_TRANSFER = 0x5B
    """Periodic advertising set info transfer command."""

    SET_PAST_PARAM = 0x5C
    """Set periodic advertising sync transfer parameters command."""

    SET_DEFAULT_PAST_PARAM = 0x5D
    """Set default periodic advertising sync transfer parameters command."""

    GENERATE_DHKEY_V2 = 0x5E
    """Generate DHKey version2 command."""

    MODIFY_SLEEP_CLK_ACC = 0x5F
    """Modify sleep clock accuracy command."""

    READ_BUF_SIZE_V2 = 0x60
    """Read buffer size version2 command."""

    READ_ISO_TX_SYNC = 0x61
    """Read ISO TX sync command."""

    SET_CIG_PARAMS = 0x62
    """Set CIG parameters command."""

    SET_CIG_PARAMS_TEST = 0x63
    """Set CIG parameters test command."""

    CREATE_CIS = 0x64
    """Create CIS command."""

    REMOVE_CIG = 0x65
    """Remove CIG command."""

    ACCEPT_CIS_REQ = 0x66
    """Accept CIS request command."""

    REJECT_CIS_REQ = 0x67
    """Reject CIS request command."""

    CREATE_BIG = 0x68
    """Create BIG command."""

    CREATE_BIG_TEST = 0x69
    """Create BIG test command."""

    TERMINATE_BIG = 0x6A
    """Terminate BIG command."""

    BIG_CREATE_SYNC = 0x6B
    """BIG create sync command."""

    BIG_TERMINATE_SYNC = 0x6C
    """BIG terminate sync command."""

    REQUEST_PEER_SCA = 0x6D
    """Request peer SCA command."""

    SETUP_ISO_DATA_PATH = 0x6E
    """Setup ISO data path command."""

    REMOVE_ISO_DATA_PATH = 0x6F
    """Remove ISO data path command."""

    ISO_TX_TEST = 0x70
    """ISO TX test command."""

    ISO_RX_TEST = 0x71
    """ISO RX test command."""

    ISO_READ_TEST_COUNTERS = 0x72
    """ISO read test counters command."""

    ISO_TEST_END = 0x73
    """ISO test end command."""

    SET_HOST_FEATURE = 0x74
    """Set host feature command."""

    READ_ISO_LINK_QUAL = 0x75
    """Read ISO link quality command."""

    READ_ENHANCED_TX_POWER = 0x76
    """Enhanced read TX power level command."""

    READ_REMOTE_TX_POWER = 0x77
    """Read remote TX power command."""

    SET_PATH_LOSS_REPORTING_PARAMS = 0x78
    """Set path loss repoting parameters command."""

    SET_PATH_LOSS_REPORTING_ENABLE = 0x79
    """Set path loss reporting enable command."""

    SET_TX_POWER_REPORT_ENABLE = 0x7A
    """Set TX power reporting enable command."""

    SET_DATA_RELATED_ADDRESS_CHANGES = 0x7C
    """Set data related address changes command."""

    SET_DEF_SUBRATE = 0x7D
    """Set default subrate command."""

    SUBRATE_REQ = 0x7E
    """Subrate request command."""


class VendorSpecificOCF(Enum):
    """ADI Vendor Specific group Opcode Command Field values."""

    SET_SCAN_CH_MAP = 0x3E0
    """Set scan channel map command."""

    SET_EVENT_MASK = 0x3E1
    """Set event mask command."""

    ENA_ACL_SINK = 0x3E3
    """Enable ACL sink command."""

    GENERATE_ACL = 0x3E4
    """Generate ACL command."""

    ENA_AUTO_GEN_ACL = 0x3E5
    """Enable autogenerate ACL command."""

    SET_TX_TEST_ERR_PATT = 0x3E6
    """Set TX test error pattern command."""

    SET_CONN_OP_FLAGS = 0x3E7
    """Set connection operational flags command."""

    SET_P256_PRIV_KEY = 0x3E8
    """Set P-256 private key command."""

    GET_PER_CHAN_MAP = 0x3DE
    """Get periodic scan/advertising channel map command."""

    GET_ACL_TEST_REPORT = 0x3E9
    """Get ACL test report command."""

    SET_LOCAL_MIN_USED_CHAN = 0x3EA
    """Set local minimum number of used channels command."""

    GET_PEER_MIN_USED_CHAN = 0x3EB
    """Get peer minimum number of used channels command."""

    VALIDATE_PUB_KEY_MODE = 0x3EC
    """Set validate public key mode command."""

    SET_BD_ADDR = 0x3F0
    """Set BD address command."""

    GET_RAND_ADDR = 0x3F1
    """Get random address command."""

    SET_LOCAL_FEAT = 0x3F2
    """Set local features command."""

    SET_OP_FLAGS = 0x3F3
    """Set operational flags command."""

    SET_ADV_TX_PWR = 0x3F5
    """Set advertising TX power command."""

    SET_CONN_TX_PWR = 0x3F6
    """Set connection TX power command."""

    SET_ENC_MODE = 0x3F7
    """Set encryption mode command."""

    SET_CHAN_MAP = 0x3F8
    """Set channel map command."""

    SET_DIAG_MODE = 0x3F9
    """Set diagnostic mode command."""

    SET_SNIFFER_ENABLE = 0x3CD
    """Set sniffer packet forwarding enable command."""

    GET_PDU_FILT_STATS = 0x3F4
    """Get PDU filter statistics command."""

    GET_SYS_STATS = 0x3FA
    """Get system statistics command."""

    GET_ADV_STATS = 0x3FB
    """Get advertising statistics command."""

    GET_SCAN_STATS = 0x3FC
    """Get scan statistics command."""

    GET_CONN_STATS = 0x3FD
    """Get connection statistics command."""

    GET_TEST_STATS = 0x3FE
    """Get test statistics command."""

    GET_POOL_STATS = 0x3FF
    """Get pool statistics command."""

    SET_AUX_DELAY = 0x3D0
    """Set auxiliary packet offset delay command."""

    SET_EXT_ADV_FRAG_LEN = 0x3D1
    """Set extended advertising data fragmentation length command."""

    SET_EXT_ADV_PHY_OPTS = 0x3D2
    """Set extended advertising PHY options command."""

    SET_EXT_ADV_DEF_PHY_OPTS = 0x3D3
    """Set extended advertising default PHY options command."""

    GENERATE_ISO = 0x3D5
    """Generate ISO packets command."""

    GET_ISO_TEST_REPORT = 0x3D6
    """Get ISO test report command."""

    ENA_ISO_SINK = 0x3D7
    """Enable ISO sink command."""

    ENA_AUTO_GEN_ISO = 0x3D8
    """Enable autogenerate ISO packets command."""

    GET_CIS_STATS = 0x3D9
    """Get CIS statistics command."""

    GET_AUX_ADV_STATS = 0x3DA
    """Get auxiliary advertising statistics command."""

    GET_AUX_SCAN_STATS = 0x3DB
    """Get auxiliary scan statistics command."""

    GET_PER_SCAN_STATS = 0x3DC
    """Get periodic scan statistics command."""

    SET_CONN_PHY_TX_PWR = 0x3DD
    """Set connection PHY TX power command."""

    REG_WRITE = 0x300
    """Register write command."""

    REG_READ = 0x301
    """Register read command."""

    RESET_CONN_STATS = 0x302
    """Reset connection statistics command."""

    TX_TEST = 0x303
    """Transmitter test command."""

    RESET_TEST_STATS = 0x304
    """Reset test statistics command."""

    RX_TEST = 0x305
    """Receiver test command."""

    GET_RSSI = 0x306
    """Get RSSI command."""

    BB_EN = 0x307
    """PHY enable command."""

    BB_DIS = 0x308
    """PHY disable command."""


@dataclass
class OCF:
    """Supported Opcode Command Field values."""

    NOP = NOpOCF
    """NOP ground OCF values."""

    LINK_CONTROL = LinkControlOCF
    """Link Control group OCF values."""

    LINK_POLICY = None
    """Link Policy group OCF values."""

    CONTROLLER = ControllerOCF
    """Controller group OCF values."""

    INFORMATIONAL = InformationalOCF
    """Informational group OCF values."""

    STATUS = StatusOCF
    """Status group OCF values."""

    TESTING = None
    """Testing group OCF values."""

    LE_CONTROLLER = LEControllerOCF
    """LE Controller group OCF values."""

    VENDOR_SPEC = VendorSpecificOCF
    """ADI Vendor Specific group OCF values."""
