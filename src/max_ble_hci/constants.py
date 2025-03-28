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
"""Contains HCI constants definitions."""
from __future__ import annotations

from enum import Enum
from typing import Tuple

ADI_PORT_BAUD_RATE = 115200

MAX_U16 = 2**16 - 1
"""Maximum value for a 16-bit unsigned integer."""
MAX_U32 = 2**32 - 1
"""Maximum value for a 32-bit unsigned integer."""
MAX_U64 = 2**64 - 1
"""Maximum value for a 64-bit unsigned integer."""


class Endian(Enum):
    """Endian byte-order definitions."""

    LITTLE = "little"
    """Little endian byte order."""

    BIG = "big"
    """Big endian byte order."""


class PhyOption(Enum):
    """BLE-defined PHY options."""

    PHY_1M = 0x1
    """1M PHY option."""

    PHY_2M = 0x2
    """2M PHY option."""

    PHY_CODED = 0x3
    """Generic coded PHY option."""

    PHY_CODED_S8 = 0x3
    """Coded S8 PHY option."""

    PHY_CODED_S2 = 0x4
    """Coded S2 PHY option."""

    def __str__(self) -> str:
        if self == PhyOption.PHY_1M:
            return "1M"

        if self == PhyOption.PHY_2M:
            return "2M"

        if self == PhyOption.PHY_CODED_S2:
            return "S2"

        if self == PhyOption.PHY_CODED_S8:
            return "S8"

        if self == PhyOption.PHY_CODED:
            return "Coded"

        return ""

    @staticmethod
    def to_mask(phy: PhyOption) -> Tuple[int, int]:
        """Convert list of phy options to PHY preference mask and PHY option mask

        Parameters
        ----------
        phy : PhyOption
            PhyOption Enum

        Returns
        -------
        Tuple[int, int]
            PHY preference mask as defined by BLE spec
            PHY option mask as defined by BLE spec
        """

        if phy == PhyOption.PHY_1M:
            return (1 << 0, 0)

        if phy == PhyOption.PHY_2M:
            return (1 << 1, 0)

        if phy in (PhyOption.PHY_CODED, PhyOption.PHY_CODED_S8):
            return (1 << 2, 2)

        return (1 << 2, 1)

    @staticmethod
    def str_to_enum(phy: str) -> PhyOption:
        """Convert phy as string to enum

        Parameters
        ----------
        phy : str
            PHY (1M, 2M, S8, S2)

        Returns
        -------
        PhyOption
            PHY option as enum

        Raises
        ------
        ValueError
            If PHY option does not exist
        """
        if phy.upper() not in ("1M", "2M", "S8", "S2"):
            raise ValueError("PHY string must be in (1M, 2M, S8, S2)")

        if phy == "1M":
            return PhyOption.PHY_1M
        if phy == "2M":
            return PhyOption.PHY_2M
        if phy == "S2":
            return PhyOption.PHY_CODED_S2
        if phy == "S8":
            return PhyOption.PHY_CODED_S8

        return PhyOption.PHY_1M


class PayloadOption(Enum):
    """BLE-definded payload options."""

    PLD_PRBS9 = 0
    """PRBS9 payload option."""

    PLD_11110000 = 1
    """11110000 payload option."""

    PLD_10101010 = 2
    """10101010 payload option."""

    PLD_PRBS15 = 3
    """PRBS15 payload option."""

    PLD_11111111 = 4
    """11111111 payload option."""

    PLD_00000000 = 5
    """00000000 payload option."""

    PLD_00001111 = 6
    """00001111 payload option."""

    PLD_01010101 = 7
    """01010101 payload option."""


class AddrType(Enum):
    """BLE-defined peer address types."""

    PUBLIC = 0
    """Public device address."""

    RANDOM = 1
    """Random device address."""

    PUBLIC_IDENTITY = 2
    """
    Resolvable Private address based on local IRK from
    resolving list, or public address if no match is found.
    
    .. note::
        For advertising, this value is valid for own device
        address type only. For connection, this value is valid
        for both own device address type and connectable peer
        device address type.

    """

    RANDOM_IDENTITY = 3
    """
    Resolvable Private address based on local IRK from
    resolving list, or random address is no match is found.

    .. note::
        For advertising, this value is valid for own device
        address type only. For connection, this value is valid
        for both own device address type and connectable peer
        device address type.

    """


class PubKeyValidateMode(Enum):
    """Public key validation modes."""

    ALT1 = 0x0
    """ALT1 validation mode."""

    ALT2 = 0x1
    """ALT2 validation mode."""


class TxTestMode(Enum):
    """Transmitter Test Modes"""

    ENHANCED = 1
    """Transmitter Test Enhanced"""

    V3 = 3
    """Transmitter Test V4"""

    V4 = 4
    """Transmitter Test V4"""


class CteType(Enum):
    """Requested CTE Types"""

    AOA = 0
    """AoA Constant Tone Extension"""
    AOD_1_US = 1
    """AoD Constant Tone Extension with 1 us slots"""
    AOD_2_US = 2
    """AoD Constant Tone Extension with 2 us slots"""


class TxPower(Enum):
    """Transmitter Power Levels"""

    MAX = 0x7F
    """Maximum power level"""

    MIN = 0x7E
    """Minimum power level"""

    @staticmethod
    def str_to_mask(option: str) -> int:
        """Select a power level.

        Parameters
        ----------
        option: str
            The desired power level.

        Returns
        -------
        int
            The power level's corresponding power symbol.
        """
        option = option.lower()

        if option == "max":
            return TxPower.MAX.value

        if option == "min":
            return TxPower.MIN.value

        return TxPower.MAX.value
