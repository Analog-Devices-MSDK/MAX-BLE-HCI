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

from enum import Enum
from typing import List, Optional, Union

from .packet_defs import OCF, OGF, PacketType
from .packet_codes import EventCode, StatusCode


def _byte_length(num):
    return max((num.bit_length() + 7) // 8, 1)


class Endian(Enum):
    LITTLE = "little"
    BIG = "big"


class CommandPacket:
    """
    Command Packet Class
    """

    def __init__(self, ogf, ocf, params=None) -> None:
        self.ogf = self._enum_to_int(ogf)
        self.ocf = self._enum_to_int(ocf)
        self.length = self._get_length(params)
        self.opcode = CommandPacket.make_hci_opcode(self.ogf, self.ocf)
        if params:
            self.params = params if isinstance(params, list) else [params]
        else:
            self.params = None

    def __repr__(self):
        return str(self.__dict__)

    def _enum_to_int(self, num):
        if isinstance(num, Enum):
            return num.value
        else:
            return num

    def _get_length(self, params):
        if params is None:
            return 0
        if isinstance(params, int):
            return _byte_length(params)

        return sum([_byte_length(x) for x in params])

    @staticmethod
    def make_hci_opcode(ogf: OGF, ocf: OCF):
        """Makes an HCI opcode.

        Function creates an HCI opcode from the given
        Opcode Group Field (OGF) and Opcode Command Field (OCF).

        Parameters
        ----------
        ogf : Union[OGF, int]
            Opcode group field.
        ocf : Union[Enum, int]
            Opcode command field.

        Returns
        -------
        int
            The generated HCI opcode.

        """
        if not isinstance(ogf, int):
            if isinstance(ogf, Enum):
                ogf = ogf.value
            else:
                raise TypeError(
                    "Parameter 'ogf' must be an integer or an OGF enumeration."
                )

        if not isinstance(ocf, int):
            if isinstance(ocf, Enum):
                ocf = ocf.value
            else:
                raise TypeError(
                    "Parameter 'ogf' must be an integer or an OCF enumeration."
                )

        return (ogf << 10) | ocf

    def to_bytes(self, endianness: Endian = Endian.LITTLE) -> bytearray:
        """Serializes a command packet to a byte array.

        Parameters
        ----------
        endianness : int
            `Endian.LITTLE` for little endian serialization,
            `Endian.BIG` for big endian serialization.

        Returns
        -------
        bytearray
            The serialized command.

        """
        serialized_cmd = bytearray()
        serialized_cmd.append(PacketType.COMMAND.value)
        serialized_cmd.append(self.opcode & 0xFF)
        serialized_cmd.append((self.opcode & 0xFF00) >> 8)

        serialized_cmd.append(self.length)

        if self.params:
            for param in self.params:
                num_bytes = _byte_length(param)
                serialized_cmd.extend(param.to_bytes(num_bytes, endianness.value))

        return serialized_cmd


class AsyncPacket:
    def __init__(self, data) -> None:
        self.handle = (data[0] & 0xF0) + (data[1] << 8)
        self.pb_flag = (data[0] & 0xC) >> 2
        self.bc_flag = data[0] & 0x3
        self.length = data[2] + (data[3] << 8)
        self.data = data[4:] if data[4:] else None

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def from_bytes(serialized_event):
        return AsyncPacket(serialized_event)


class EventPacket:
    def __init__(self, evt_code, length, num_cmds, opcode, status, return_vals) -> None:
        self.evt_code = EventCode(evt_code)
        self.length = length
        self.num_cmds = num_cmds
        self.opcode = opcode
        self.status = StatusCode(status)
        self.return_vals = return_vals

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def from_bytes(serialized_event, endianness=Endian.LITTLE):
        return EventPacket(
            evt_code=serialized_event[0],
            length=serialized_event[1],
            num_cmds=serialized_event[2],
            opcode=int.from_bytes(serialized_event[3:5], endianness.value),
            status=serialized_event[5],
            return_vals=serialized_event[2:],
        )

    def get_return_params(
        self,
        param_lens: Optional[List[int]] = None,
        endianness: Endian = Endian.LITTLE,
        use_raw: bool = False,
    ) -> Union[List[int], int]:
        if use_raw:
            param_bytes = self.return_vals
        else:
            param_bytes = self.return_vals[4:]

        if not param_lens:
            return int.from_bytes(param_bytes, endianness.value)

        if sum(param_lens) > len(param_bytes):
            raise ValueError(
                "Expected and actual number of return bytes do not match. "
                f"Expected={sum(param_lens)}, Actual={len(param_bytes)}"
            )

        return_params = []
        p_idx = 0
        for p_len in param_lens:
            return_params.append(
                int.from_bytes(param_bytes[p_idx : p_idx + p_len], endianness.value)
            )
            p_idx += p_len

        return return_params


class ExtendedPacket:
    def __init__(self, data):
        self.opcode = data[0] + (data[1] << 8)
        self.length = data[2] + (data[3] << 8)
        self.payload = data[4:] if data[4:] else None

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def from_bytes(serialized_event):
        return ExtendedPacket(serialized_event)
