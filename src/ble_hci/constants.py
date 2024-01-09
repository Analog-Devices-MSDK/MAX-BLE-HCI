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
constants.py

Description: Constants used in BLE HCI

"""

from enum import Enum


class Payload(Enum):
    """DTM Payload options"""

    PRBS9 = 0
    DF1 = 1
    DF2 = 2
    PRBS15 = 3
    ALL_1S = 4
    ALL_0S = 5
    HALF_OFF_HALF_ON = 6
    INV_DF1 = 7


# ADI_PAYLOAD_PRBS9 (0), ADI_PAYLOAD_11110000 (1),
# ADI_PAYLOAD_10101010 (2), ADI_PAYLOAD_PRBS15 (3),
# ADI_PAYLOAD_11111111 (4) ADI_PAYLOAD_00000000 (5),
# ADI_PAYLOAD_00001111 (6) and ADI_PAYLOAD_01010101 (7)


class PhyOption(Enum):
    """Available modulation rates"""

    PHY_1M = 0x1
    PHY_2M = 0x2
    PHY_CODED = 0x3
    PHY_CODED_S8 = 0x3
    PHY_CODED_S2 = 0x4
