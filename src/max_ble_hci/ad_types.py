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
ad_types

Description: Advertising data types

"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List
from .utils import unsigned_to_signed


class AdvEventType(Enum):
    """Advertising Event Type"""

    ADV_IND = 0
    ADV_DIRECT_IND = 1
    ADV_SCAN_IND = 2
    ADV_NONCONN_IND = 3
    SCAN_RSP = 4


class AddressType(Enum):
    """Adress Type"""

    PUB_DEV_ADDRESS = 0
    RAND_DEV_ADDR = 1
    PUBLIC_ID_ADDR = 2
    RAND_ID_ADDR = 3


class ADType(Enum):
    """Advertising data types"""

    FLAGS = 0x1
    INCOMPLETE_16B_SC_UUID = 0x2
    COMPLETE_16B_SC_UUID = 0x3
    INCOMPLETE_32B_SC_UUID = 0x4
    COMPLETE_32B_SC_UUID = 0x5
    INCOMPLETE_128B_SC_UUID = 0x6
    COMPLETE_128B_SC_UUID = 0x7
    LOCAL_NAME_SHORT = 0x8
    LOCAL_NAME_COMPLETE = 0x9
    TX_POWER_LEVEL = 0x0A
    DEV_CLASS = 0x0D
    SIMPLE_PAIR_HASH_C192 = 0x0E
    SIMPLE_PAIR_RAND_R192 = 0x0F
    DEV_ID = 0x10
    SEC_MAN_TK_VALUE = 0x10
    SEC_MAN_OOB_FLAGS = 0x11
    PERIPH_CONN_INTERVAL_RANGE = 0x12
    SERV_SOLICITATION_16B = 0x14
    SERV_SOLICITATION_128B = 0x15
    SERV_DATA_16B = 0x16
    PUB_TARGET_ADDR = 0x17
    RAND_TARGET_ADDR = 0x18
    APPEARANCE = 0x19
    ADV_INTERVAL = 0x1A
    LE_BT_DEV_ADDR = 0x1B
    LE_ROLE = 0x1C
    SIMPLE_PAIR_HASH_C256 = 0x1D
    SIMPLE_PAIR_RAND_R256 = 0x1E
    SERV_SOLICITATION_32B = 0x1F
    SERV_DATA = 0x20
    LE_SEC_CONN_CONF_VALUE = 0x22
    LE_SEC_CONN_RAND_VALUE = 0x23
    URI = 0x24
    INDOOR_POSITIONING = 0x25
    TRANSPORT_DISC_DATA = 0x26
    LE_SUPP_FEAT = 0x27
    CHAN_MAP_UPDATE_IND = 0x28
    PB_ADV = 0x29
    MESH_MESSAGE = 0x2A
    MESH_BEACON = 0x2B
    BIG_INFO = 0x2C
    BROADCAST_CODE = 0x2D
    RESOLV_SET_ID = 0x2E
    ADV_INTERVAL_LONG = 0x2F
    BROADCAST_NAME = 0x30
    ENC_ADV_DATA = 0x31
    PER_ADC_RESP_TIME_INFO = 0x32
    ELECTRONIC_SHELF_LABEL = 0x34
    INFO_DATA_3D = 0x3D
    MANUFACTURER_SPEC_DATA = 0xFF


@dataclass
class AdvReport:
    """Advertising Report"""

    event_type: AdvEventType = None
    address_type: AddressType = None
    address: str = None
    data_len: int = None
    data: list = None
    rssi: int = None

    @staticmethod
    def from_bytes(data: bytes) -> List[AdvReport]:
        """Raw advertising report data to list of advertising reports

        Parameters
        ----------
        data : bytes
            Raw advertising report

        Returns
        -------
        List[AdvReport]
            List of deserialized advertising reports
        """
        data_bytes = data
        data = list(data)  # Convert to ints

        # Constants for sizes
        sizes = {"evt_type": 1, "addr_type": 1, "addr": 6, "len": 1, "rssi": 1}

        num_reports = data[0]
        reports = [AdvReport() for _ in range(num_reports)]

        offset = 1

        # Im sorry
        for i in range(num_reports):
            reports[i].event_type = AdvEventType(data[offset])
            offset += sizes["evt_type"]

            reports[i].address_type = AddressType(data[offset])
            offset += sizes["addr_type"]

            address = data[offset : offset + sizes["addr"]][::-1]
            reports[i].address = ":".join(f"{byte:02x}" for byte in address)
            offset += sizes["addr"]

            data_len = data[offset]
            reports[i].data_len = data_len
            offset += sizes["len"]

            data_slice = data[offset : offset + data_len][::-1]
            reports[i].data = data_slice
            offset += data_len

            reports[i].rssi = unsigned_to_signed(data_bytes[offset], 8)
            offset += sizes["rssi"]

        return reports


@dataclass
class AdvData:
    """Advertising Data"""

    length: int = None
    type: ADType = None
    data: object = None

    @staticmethod
    def from_raw_data(data: List[int]) -> List[AdvData]:
        """Convert advertising report data to N advertising data packets

        Parameters
        ----------
        data : List[int]
            Raw data from advertising report

        Returns
        -------
        List[AdvData]
            List of adverstising data packets
        """
        ad_data = []

        idx = 0
        while idx < len(data):
            data_len = data[idx + 0]
            ad_type = ADType(data[idx + 1])

            base = idx + 2
            decoded_data = data[base : base + data_len]

            if ad_type in (ADType.LOCAL_NAME_SHORT, ADType.LOCAL_NAME_COMPLETE):
                decoded_data = str(decoded_data)
            ad_data.append(AdvData(length=data_len, type=ad_type, data=decoded_data))

            idx += data_len + 2

        return ad_data
