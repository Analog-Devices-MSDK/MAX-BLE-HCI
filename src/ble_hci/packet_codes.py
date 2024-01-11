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
"""Contains definitions for BLE standard codes utilized in HCI packet creation/parsing."""
from enum import Enum


class EventCode(Enum):
    """Supported HCI Event Codes"""

    DICON_COMPLETE = 0x05
    """Disconnection complete event."""

    ENC_CHANGE = 0x08
    """Encryption change event."""

    READ_REMOTE_VERSION_INFO_COMPLETE = 0x0C
    """Read remote version information complete event."""

    COMMAND_COMPLETE = 0x0E
    """Command complete event."""

    COMMAND_STATUS = 0x0F
    """Command status event."""

    HARDWARE_ERROR = 0x10
    """Hardware error event."""

    NUM_COMPLETED_PACKETS = 0x13
    """Number of completed packets event."""

    DATA_BUFF_OVERFLOW = 0x1A
    """Data buffer overflow event."""

    ENC_KEY_REFRESH_COMPLETE = 0x30
    """Encryption key refresh complete event."""

    LE_META = 0x3E
    """LE meta event."""

    AUTH_PAYLOAD_TIMEOUT_EXPIRED = 0x57
    """Authenticated payload timeout expired event."""

    VENDOR_SPEC = 0xFF
    """Vendor specific event."""


class EventSubcode(Enum):
    """Supported LE Meta event subcodes."""

    CONNECTION_COMPLETE = 0x1
    """Connection complete event."""

    ADVERTISING_REPORT = 0x2
    """Advertising report event."""

    CONNECTION_UPDATE = 0x3
    """Connection update complete event."""

    READ_REMOTE_FEATURES_COMPLETE = 0x4
    """Read remote feature complete event."""

    LONG_TERM_KEY_REQUEST = 0x5
    """Long term key request event."""

    REMOTE_CONNECTION_PARAMETER_REQUEST = 0x6
    """Remote connection parameter request event."""

    DATA_LENGTH_CHANGE = 0x7
    """Data length change event."""

    READ_LOCAL_P256_PUBLIC_KEY_COMPLETE = 0x8
    """Read local P-256 public key complete event."""

    GENERATE_DHKEY_COMPLETE = 0x9
    """Generate DHKey complete event."""

    ENHANCED_CONNECTION_COMPLETE = 0xA
    """Enhanced connection complete event."""

    DIRECTED_ADVERTISIING_REPORT = 0xB
    """Directed advertising report event."""

    PHY_UPDATE_COMPLETE = 0xC
    """PHY update complete event."""

    EXTENDED_ADVERTISING_REPORT = 0xD
    """Extended advertising report event."""

    PERIODIC_ADVERTISING_SYNC_ESTABLISHED = 0xE
    """Periodic advertising sync established event."""

    PERIODIC_ADVERTISING_REPORT = 0xF
    """Periodic advertising report event."""

    PERIODIC_ADVERTISING_SYNC_LOST = 0x10
    """Periodic advertising sync lost event."""

    SCAN_TIMEOUT = 0x11
    """Scan timeout event."""

    ADVERTISING_SET_TERMINATED = 0x12
    """Advertising set terminated event."""

    SCAN_REQUEST_RECEIVED = 0x13
    """Scan request received event."""

    CHANNEL_SELECTION_ALGORITHM = 0x14
    """Channel selection algorithm event."""

    CONNECTIONLESS_IQ_REPORT = 0x15
    """Connectionless IQ report event."""

    CONNECTION_IQ_REPORT = 0x16
    """Connection IQ report event."""

    CTE_REQUEST_FAILED = 0x17
    """CTE request failed event."""

    PERIODIC_ADVERTISING_SYNC_TRANSER_RECEIVED = 0x18
    """Periodic advertising sync transfer received event."""

    CIS_ESTABLISHED = 0x19
    """CIS established event."""

    CIS_REQUEST = 0x1A
    """CIS request event."""

    CREATE_BIG_COMPLETE = 0x1B
    """Create BIG complete event."""

    TERMINATE_BIG_COMPLETE = 0x1C
    """Terminate BIG complete event."""

    BIG_SYNC_ESTABLISHED = 0x1D
    """BIG sync established event."""

    BIG_SYNC_LOST = 0x1E
    """BIG sync list event."""

    REQUEST_PEER_SCA_COMPLETE = 0x1F
    """Request peeer SCA complete event."""

    PATH_LOSS_THRESHOLD = 0x20
    """Path loss threshold event."""

    TRANSMIT_POWER_REPORTING = 0x21
    """Transmit power reporting event."""

    BIGINFO_ADVERTISING_REPORT = 0x22
    """BIGInfo advertising report event."""


class StatusCode(Enum):
    """BLE-defined status codes."""

    SUCCESS = 0x00
    """Success."""

    ERROR_CODE_UNKNOWN_HCI_CMD = 0x01
    """Unknown HCI command error."""

    ERROR_CODE_UNKNOWN_CONN_ID = 0x2
    """Unknown connection identifier."""

    ERROR_CODE_HW_FAILURE = 0x03
    """Hardware failure."""

    ERROR_CODE_PAGE_TIMEOUT = 0x04
    """Page timeout."""

    ERROR_CODE_AUTH_FAILURE = 0x05
    """Authentication failure."""

    ERROR_CODE_PIN_KEY_MISSING = 0x06
    """PIN or key missing."""

    ERROR_CODE_MEM_CAP_EXCEEDED = 0x07
    """Memory capacity exceeded."""

    ERROR_CODE_CONN_TIMEOUT = 0x08
    """Connection timeout."""

    ERROR_CODE_CONN_LIMIT_EXCEEDED = 0x09
    """Connection limit exceeded."""

    ERROR_CODE_SYNCH_CONN_LIMIT_EXCEEDED = 0x0A
    """Synchronous connection limit to a device exceeded."""

    ERROR_CODE_ACL_CONN_ALREADY_EXISTS = 0x0B
    """Connection already exists."""

    ERROR_CODE_CMD_DISALLOWED = 0x0C
    """Command disallowed."""

    ERROR_CODE_CONN_REJ_LIMITED_RESOURCES = 0x0D
    """connection rejection due to limited resources."""

    ERROR_CODE_CONN_REJECTED_SECURITY_REASONS = 0x0E
    """Connection rejected due to security reasons."""

    ERROR_CODE_CONN_REJECTED_UNACCEPTABLE_BDADDR = 0x0F
    """Connection rejected dur to unacceptable BD address."""

    ERROR_CODE_CONN_ACCEPT_TIMEOUT_EXCEEDED = 0x10
    """Connection accept timeout exceeded."""

    ERROR_CODE_UNSUPPORTED_FEATURE_PARAM_VALUE = 0x11
    """Unsupported feature or parameter value."""

    ERROR_CODE_INVALID_HCI_CMD_PARAMS = 0x12
    """Invalid HCI command parameters."""

    ERROR_CODE_REMOTE_USER_TERM_CONN = 0x13
    """Remote user terminated connection."""

    ERROR_CODE_REMOTE_DEVICE_TERM_CONN_LOW_RESOURCES = 0x14
    """Remote device terminated connection due to low resources."""

    ERROR_CODE_REMOTE_DEVICE_TERM_CONN_POWER_OFF = 0x15
    """Remote device terminated connection due to power off."""

    ERROR_CODE_CONN_TERM_BY_LOCAL_HOST = 0x16
    """Connection terminated by local host."""

    ERROR_CODE_REPEATED_ATTEMPTS = 0x17
    """Repeated attempts."""

    ERROR_CODE_PAIRING_NOT_ALLOWED = 0x18
    """Pairing not allowed."""

    ERROR_CODE_UNKNOWN_LMP_PDU = 0x19
    """Unknown LMP PDU."""

    ERROR_CODE_UNSUPPORTED_REMOTE_FEATURE = 0x1A
    """Unsupported remote feature."""

    ERROR_CODE_SCO_OFFSET_REJ = 0x1B
    """SCO offset rejected."""

    ERROR_CODE_SCO_INTERVAL_REJ = 0x1C
    """SCO interval rejected."""

    ERROR_CODE_SCO_AIR_MODE_REJ = 0x1D
    """SCO air mode rejected."""

    ERROR_CODE_INVALID_LMP_PARAMS = 0x1E
    """Invalid LMP parameters / Invalid LL parameters."""

    ERROR_CODE_UNSPECIFIED_ERROR = 0x1F
    """Unspecified error."""

    ERROR_CODE_UNSUPPORTED_LMP_PARAM_VAL = 0x20
    """Unsupported LMP parameter value / Unsupported LL parameter value."""

    ERROR_CODE_ROLE_CHANGE_NOT_ALLOWED = 0x21
    """Role change not allowed."""

    ERROR_CODE_LMP_LL_RESP_TIMEOUT = 0x22
    """LMP response timeout / LL response timeout."""

    ERROR_CODE_LMP_ERR_TRANSACTION_COLLISION = 0x23
    """LMP error transaction collision / LL procedure collision."""

    ERROR_CODE_LMP_PDU_NOT_ALLOWED = 0x24
    """LMP PDU not allowed."""

    ERROR_CODE_ENCRYPT_MODE_NOT_ACCEPTABLE = 0x25
    """Encryption mode not acceptable."""

    ERROR_CODE_LINK_KEY_CAN_NOT_BE_CHANGED = 0x26
    """Link key cannot be changed."""

    ERROR_CODE_REQ_QOS_NOT_SUPPORTED = 0x27
    """Requested QoS not supported."""

    ERROR_CODE_INSTANT_PASSED = 0x28
    """Instance passed."""

    ERROR_CODE_PAIRING_WITH_UNIT_KEY_NOT_SUPPORTED = 0x29
    """Pairing with unit key not supported."""

    ERROR_CODE_DIFFERENT_TRANSACTION_COLLISION = 0x2A
    """Different transaction collision."""

    ERROR_CODE_RESERVED1 = 0x2B
    """Reserved for future use."""

    ERROR_CODE_QOS_UNACCEPTABLE_PARAM = 0x2C
    """QoS unacceptable parameter."""

    ERROR_CODE_QOS_REJ = 0x2D
    """QoS rejected."""

    ERROR_CODE_CHAN_ASSESSMENT_NOT_SUPPORTED = 0x2E
    """Channel classification not supported error."""

    ERROR_CODE_INSUFFICIENT_SECURITY = 0x2F
    """Insufficient security."""

    ERROR_CODE_PARAM_OUT_OF_MANDATORY_RANGE = 0x30
    """Parameter out of mandatory range."""

    ERROR_CODE_RESERVED2 = 0x31
    """Reserved for future use."""

    ERROR_CODE_ROLE_SWITCH_PENDING = 0x32
    """Role switch pending."""

    ERROR_CODE_RESERVED3 = 0x33
    """Reserved for future use."""

    ERROR_CODE_RESERVED_SLOT_VIOLATION = 0x34
    """Reserved slot violation."""

    ERROR_CODE_ROLE_SWITCH_FAILED = 0x35
    """Role switch failed."""

    ERROR_CODE_EXTENDED_INQUIRY_RESP_TOO_LARGE = 0x36
    """Extended inquiry response too large."""

    ERROR_CODE_SIMPLE_PAIRING_NOT_SUPPORTED_BY_HOST = 0x37
    """Secure simple pairing not supported by host."""

    ERROR_CODE_HOST_BUSY_PAIRING = 0x38
    """Host busy - pairing."""

    ERROR_CODE_CONN_REJ_NO_SUITABLE_CHAN_FOUND = 0x39
    """Connection rejected dur to no suitable channel found."""

    ERROR_CODE_CONTROLLER_BUSY = 0x3A
    """Controller busy."""

    ERROR_CODE_UNACCEPTABLE_CONN_INTERVAL = 0x3B
    """Unacceptable connection parameters."""

    ERROR_CODE_ADV_TIMEOUT = 0x3C
    """Advertising timeout."""

    ERROR_CODE_CONN_TERM_MIC_FAILURE = 0x3D
    """Connection terminated due to MIC failure."""

    ERROR_CODE_CONN_FAILED_TO_ESTABLISH = 0x3E
    """Connection failed to be established / Synchronization timeout."""

    ERROR_CODE_MAC_CONN_FAILED = 0x3F
    """MAC connection failed [previously used]."""

    ERROR_CODE_COARSE_CLK_ADJ_REJ = 0x40
    """
    Coarse cloack adjustment rejected but will try to adjust clock
    using clock dragging.
    """

    ERROR_CODE_TYPE0_SUBMAP_NOT_DEF = 0x41
    """Type0 submap noot defined."""

    ERROR_CODE_UNKNOWN_ADV_ID = 0x42
    """Unknown advertising identifier."""

    ERROR_CODE_LIMIT_REACHED = 0x43
    """Limit reached."""

    ERROR_CODE_OP_CANCELLED_BY_HOST = 0x44
    """Operation cancelled by host."""

    ERROR_CODE_PKT_TOO_LONG = 0x45
    """Packet too long."""

    DECODE_FAILURE = 0xFF
    """ADI vendor specific, returns when the status is not properly set."""
