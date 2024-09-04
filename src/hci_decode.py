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
hci_decode.py

Description: Basic decoding of raw HCI command packets

"""

import argparse
import binascii

# pylint: disable=redefined-builtin,import-error
from rich import print

from max_ble_hci.hci_packets import (
    OGF,
    AsyncPacket,
    CommandPacket,
    ControllerOCF,
    EventPacket,
    LEControllerOCF,
)
from max_ble_hci.packet_codes import EventMask, EventMaskLE
from max_ble_hci.packet_defs import PacketType

# pylint: enable=redefined-builtin,import-error


def _make_event_mask(params):
    event_mask = 0
    param_len = params[0]

    for i, value in enumerate(params[1:]):
        event_mask |= value << (param_len - (i + 1)) * 8
    return event_mask


def _parse_event_mask(command: CommandPacket):
    event_mask = _make_event_mask(command.params)

    # clear all rfu bits
    mask = EventMask.from_int(event_mask)
    mask_list = mask.as_str_list()

    print("[cyan]Event Mask\n-----------[/cyan]")
    for mask_str in mask_list:
        print(mask_str)


def _parse_event_mask_le(command: CommandPacket):
    event_mask = _make_event_mask(command.params)
    event_mask &= (1 << 34) | ((1 << 34) - 1)

    mask = EventMaskLE(event_mask)
    mask_list = mask.as_str_list()

    print("[cyan]Event Mask\n-----------[/cyan]")
    for mask_str in mask_list:
        print(mask_str)


def _parse_packet(command):
    packet_type = int(command[:2], 16)
    packet_type = PacketType(packet_type)

    command = binascii.unhexlify(command[2:])

    print(packet_type)
    if packet_type == PacketType.COMMAND:
        command = CommandPacket.from_bytes(command)
        print(command)
        ogf = OGF(command.ogf)
        if (
            ogf == OGF.LE_CONTROLLER
            and command.ocf == LEControllerOCF.SET_EVENT_MASK.value
        ):
            _parse_event_mask_le(command)

        elif (
            ogf == OGF.CONTROLLER and command.ocf == ControllerOCF.SET_EVENT_MASK.value
        ):
            _parse_event_mask(command)

    elif packet_type == PacketType.EXTENDED:
        pass
    elif packet_type == PacketType.ASYNC:
        print(AsyncPacket.from_bytes(command))
    elif packet_type == PacketType.EVENT:
        print(EventPacket.from_bytes(command))
    else:
        raise ValueError(f"Unnknown packet type {packet_type}")


def main():
    """MAIN"""
    parser = argparse.ArgumentParser(
        description="Evaluates connection sensitivity",
    )

    parser.add_argument("command", help="Central board")
    parser.add_argument("-e", "--event-mask", help="Command is event mask")

    args = parser.parse_args()

    command: str = args.command

    _parse_packet(command)


if __name__ == "__main__":
    main()
