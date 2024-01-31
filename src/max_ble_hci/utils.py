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
utils.py

Description: Basic utilities to help withe BLE-HCI

"""

import sys
from typing import List
import glob
import os
import serial


DEFAULT_BAUDRATE = 115200


def get_serial_ports() -> List[str]:
    """Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    if sys.platform.startswith("win"):
        ports = [f"COM{(i + 1)}" for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            possible_port = serial.Serial(port)
            possible_port.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    serial_list_linux = "/dev/serial/by-id"

    if os.path.exists(serial_list_linux):
        dir_list = os.listdir(serial_list_linux)

        for i, file in enumerate(dir_list):
            dir_list[i] = os.path.join(serial_list_linux, file)
        if dir_list:
            result.extend(dir_list)

    return result


def to_le_nbyte_list(value: int, n_bytes: int) -> List[int]:
    """Create a list of little-endian bytes.

    Converts a multi-byte number into a list of single-byte
    values. The list is little endian.

    Parameters
    ----------
    value : int
        The multi-byte value that should be converted.
    n_bytes : int
        The expected byte length of the given value

    Returns
    -------
    List[int]
        The given value represented as a little endian
        list of single-byte values. The length is
        equivalent to the `n_bytes` parameter.

    """
    little_endian = []
    for i in range(n_bytes):
        num_masked = (value & (0xFF << 8 * i)) >> (8 * i)
        little_endian.append(num_masked)
    return little_endian


def le_list_to_int(nums: List[int]) -> int:
    """Create an integer from a little-endian list.

    Converts a little-endian list of single byte values
    to a single multi-byte integer.

    Parameters
    ----------
    nums : List[int]
        List containing single-byte values in little endian
        byte order.

    Returns
    -------
    int
        The multi-byte value created from the given list.

    """
    full_num = 0
    for i, num in enumerate(nums):
        full_num |= num << 8 * i
    return full_num
