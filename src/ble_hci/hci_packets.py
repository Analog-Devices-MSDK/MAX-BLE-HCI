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
"""Contains objects used for the creation of HCI packets."""
# pylint: disable=too-many-arguments
from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union

from .packet_codes import EventCode, EventSubcode, StatusCode
from .packet_defs import OCF, OGF, PacketType
from .constants import Endian


def byte_length(num: int):
    """Calculate the length of an integer in bytes.

    PRIVATE

    """
    return max((num.bit_length() + 7) // 8, 1)


class CommandPacket:
    """Serializer for HCI command packets.

    Object defines a container/serializer for HCI command
    packets. Initializing an instance of the object creates
    a container which stores the desired command opcode and
    parameters. A serialized command can then be generated
    through the use of the `to_bytes` function. In the event
    that an opcode is needed but a full packet is not, the
    static method `make_hci_opcode` can be called without
    initializing an instance of the object.

    Parameters
    ----------
    ogf : Union[OGF, int]
        Opcode group field.
    ocf : Union[OCF, int]
        Opcode command field.
    params : Union[List[int], int], optional
        Command parameters, if any.

    Attributes
    ----------
    ogf : OGF
        Opcode group field.
    ocf : OCF
        Opcode command field.
    length : int
        Total length of command parameters.
    opcode : int
        Command opcode.
    params : Union[List[int], int], optional
        Command parameters, if any.

    """

    def __init__(
        self,
        ogf: Union[OGF, int],
        ocf: Union[OCF, int],
        params: Optional[Union[List[int], int]] = None,
    ):
        self.ogf = self._enum_to_int(ogf)
        self.ocf = self._enum_to_int(ocf)
        self.length = self._get_length(params)
        self.opcode = CommandPacket.make_hci_opcode(self.ogf, self.ocf)
        if params is not None:
            self.params = params if isinstance(params, list) else [params]
        else:
            self.params = None

    def __repr__(self) -> str:
        return str(self.__dict__)

    def _enum_to_int(self, num):
        """Convert an enumeration value to an integer.

        PRIVATE

        """
        if isinstance(num, Enum):
            return num.value
        return num

    def _get_length(self, params):
        """Get parameters length.

        PRIVATE

        """
        if params is None:
            return 0
        if isinstance(params, int):
            return byte_length(params)

        return sum(byte_length(x) for x in params)

    @staticmethod
    def make_hci_opcode(ogf: Union[OGF, int], ocf: Union[OCF, int]) -> int:
        """Make an HCI opcode.

        Creates an HCI opcode from the given Opcode Group Field (OGF)
        and Opcode Command Field (OCF) values.

        Parameters
        ----------
        ogf : Union[OGF, int]
            Opcode group field.
        ocf : Union[OCF, int]
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
        """Serialize a command packet.

        Serializes a command packets from the stored attribute
        values into a command data byte array.

        Parameters
        ----------
        endianness : Endian
            Endian byte order to apply during serialization.

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

        if self.params is not None:
            for param in self.params:
                num_bytes = byte_length(param)
                try:
                    serialized_cmd.extend(param.to_bytes(num_bytes, endianness.value))
                except OverflowError:
                    serialized_cmd.extend(
                        param.to_bytes(num_bytes, endianness.value, signed=True)
                    )

        return serialized_cmd


class ExtendedPacket:
    """Serializer for HCI extended command packets.

    Object defines a container/serializer for HCI extended command
    packets. Initializing an instance of the object creates a container
    which stores the desired extended command opcode and payload. A
    serialized command can then be generated through the use of the
    `to_bytes` function. In the event that an opcode is needed but a
    full packet is not, the static method `make_hci_opcode` can be used
    without initializing an instance of the object.

    Parameters
    ----------
    ogf : Union[OGF, int]
        Opcode group field.
    ocf : Union[OCF, int]
        Opcode command field.
    payload : Union[List[int], int], optional
        Command parameters, if any.

    Attributes
    ----------
    ogf : OGF
        Opcode group field.
    ocf : OCF
        Opcode command field.
    length : int
        Total length of command parameters.
    opcode : int
        Command opcode.
    payload : Union[List[int], int], optional
        Command parameters, if any.

    """

    def __init__(
        self,
        ogf: Union[OGF, int],
        ocf: Union[OCF, int],
        payload: Optional[Union[List[int], int]] = None,
    ):
        self.ogf = self._enum_to_int(ogf)
        self.ocf = self._enum_to_int(ocf)
        self.length = self._get_length(payload)
        self.opcode = ExtendedPacket.make_hci_opcode(self.ogf, self.ocf)
        if payload is not None:
            self.payload = payload if isinstance(payload, list) else [payload]
        else:
            self.payload = None

    def __repr__(self):
        return str(self.__dict__)

    def _enum_to_int(self, num):
        """Convert an enumeration value to an integer.

        PRIVATE

        """
        if isinstance(num, Enum):
            return num.value
        return num

    def _get_length(self, pld):
        """Get payload length.

        PRIVATE

        """
        if pld is None:
            return 0
        if isinstance(pld, int):
            return byte_length(pld)

        return sum(byte_length(x) for x in pld)

    @staticmethod
    def make_hci_opcode(ogf: Union[OGF, int], ocf: Union[OCF, int]) -> int:
        """Make an HCI opcode.

        Creates an HCI opcode from the given Opcode Group Field (OGF)
        and Opcode Command Field (OCF) values.

        Parameters
        ----------
        ogf : Union[OGF, int]
            Opcode group field.
        ocf : Union[OCF, int]
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
        """Serialize a command packet.

        Serializes a command packets from the stored attribute
        values into a command data byte array.

        Parameters
        ----------
        endianness : Endian
            Endian byte order to apply during serialization.

        Returns
        -------
        bytearray
            The serialized command.

        """
        serialized_cmd = bytearray()
        serialized_cmd.append(PacketType.EXTENDED.value)
        serialized_cmd.append(self.opcode & 0xFF)
        serialized_cmd.append((self.opcode & 0xFF00) >> 8)

        serialized_cmd.append(self.length & 0xFF)
        serialized_cmd.append((self.length & 0xFF00) >> 8)

        if self.payload is not None:
            for param in self.payload:
                num_bytes = byte_length(param)
                try:
                    serialized_cmd.extend(param.to_bytes(num_bytes, endianness.value))
                except OverflowError:
                    serialized_cmd.extend(
                        param.to_bytes(num_bytes, endianness.value, signed=True)
                    )

        return serialized_cmd


class AsyncPacket:
    """Deserializer for HCI ACL packets.

    Object defines a deserializer/data container for HCI
    Asynchronous Connection-Less packets. To create an
    instance directly from bytes, use the static function
    `from_bytes`.

    Parameters
    ----------
    handle : int
        Packet handle value.
    pb_flag : int
        Packet PB flag.
    bc_flag : int
        Packet BC flag.
    length : int
        Packet data length.
    data : bytes
        Packet data.

    Attributes
    ----------
    handle : int
        Packet handle value.
    pb_flag : int
        Packet PB flag.
    bc_flag : int
        Packet BC flag.
    length : int
        Packet data length.
    data : bytes
        Packet data.

    """

    def __init__(
        self, handle: int, pb_flag: int, bc_flag: int, length: int, data: bytes
    ):
        self.handle = handle
        self.pb_flag = pb_flag
        self.bc_flag = bc_flag
        self.length = length
        self.data = data

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_bytes(pkt: bytes) -> AsyncPacket:
        """Deserialize an HCI ACL packet.

        Deserializes an HCI Asynchronous Connection-Less packet
        from a bytes object.

        Parameters
        ----------
        pkt : bytes
            Serialized async packet.

        Returns
        -------
        AsyncPacket
            The deserialized packet.

        """
        return AsyncPacket(
            handle=(pkt[0] & 0xF0) + (pkt[1] << 8),
            pb_flag=(pkt[0] & 0xC) >> 2,
            bc_flag=pkt[0] & 0x3,
            length=pkt[2] + (pkt[3] << 8),
            data=pkt[4:] if pkt[4:] else None,
        )


class EventPacket:
    """Deserializer for HCI event packets.

    Object defines a deserializer/data container for HCI
    event packets. To create an instance directly from
    bytes, use the static function `from_bytes`. Event
    packet return parameters can be retrieved by calling
    the `get_return_params` function once an instance of
    the object has been created.

    Parameters
    ----------
    evt_code : int
        Packet event code.
    length : int
        Packet data length.
    status : int
        Packet status code.
    evt_params : bytes
        Packet return parameters.
    evt_subcode : int, optional
        Packet event subcode.

    Attributes
    ----------
    evt_code : EventCode
        Packet event code.
    length : int
        Packet data length.
    status : StatusCode
        Packet status code.
    evt_subcode : EventSubcode, optional
        Packet event subcode
    evt_params : bytes
        Packet return parameters.

    """

    def __init__(
        self,
        evt_code: int,
        length: int,
        status: int,
        evt_params: bytes,
        evt_subcode: Optional[int] = None,
    ):
        self.evt_code = EventCode(evt_code)
        self.length = length
        self.status = StatusCode(status) if status else None
        self.evt_subcode = EventSubcode(evt_subcode) if evt_subcode else None
        self.evt_params = evt_params

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def from_bytes(serialized_event: bytes) -> EventPacket:
        """Deserialize an HCI event packet.

        Deserializes an HCI event packet from a bytes object.

        Parameters
        ----------
        serialized_event : bytes
            Serialized event packet.

        Returns
        -------
        EventPacket
            The deserialized packet.


        """
        if serialized_event[0] == EventCode.COMMAND_COMPLETE.value:
            pkt = EventPacket(
                evt_code=serialized_event[0],
                length=serialized_event[1],
                status=StatusCode(serialized_event[5]),
                evt_params=serialized_event[2:],
            )

        elif serialized_event[0] == EventCode.HARDWARE_ERROR.value:
            pkt = EventPacket(
                evt_code=serialized_event[0],
                length=serialized_event[1],
                status=StatusCode.ERROR_CODE_HW_FAILURE.value,
                evt_params=serialized_event[2:],
            )
        elif serialized_event[0] == EventCode.NUM_COMPLETED_PACKETS.value:
            pkt = EventPacket(
                evt_code=serialized_event[0],
                length=serialized_event[1],
                status=StatusCode.SUCCESS.value,
                evt_params=serialized_event[2:],
            )
        elif serialized_event[0] == EventCode.DATA_BUFF_OVERFLOW.value:
            pkt = EventPacket(
                evt_code=serialized_event[0],
                length=serialized_event[1],
                status=None,
                evt_params=serialized_event[2:],
            )
        elif serialized_event[0] == EventCode.LE_META.value:
            pkt = EventPacket(
                evt_code=serialized_event[0],
                length=serialized_event[1],
                status=None,
                evt_params=serialized_event[3:],
                evt_subcode=serialized_event[2],
            )
        elif serialized_event[0] == EventCode.AUTH_PAYLOAD_TIMEOUT_EXPIRED.value:
            pkt = EventPacket(
                evt_code=serialized_event[0],
                length=serialized_event[1],
                status=None,
                evt_params=serialized_event[2:],
            )
        elif serialized_event[0] == EventCode.VENDOR_SPEC:
            pkt = EventPacket(
                evt_code=serialized_event[0],
                length=serialized_event[1],
                status=serialized_event[2],
                evt_params=serialized_event[3:],
            )
        else:
            raise ValueError(f"Invalid event code ({serialized_event[0]}) received.")

        return pkt

    def get_return_params(
        self,
        param_lens: Optional[List[int]] = None,
        endianness: Endian = Endian.LITTLE,
        signed: bool = False,
    ) -> Union[List[int], int]:
        """Retrieve packet return parameters.

        Parses the packet return parameters from the bytes stored
        in the `evt_params` attribute in accordance with the given
        lengths and deserialization parameters.

        Parameters
        ----------
        param_lens : List[int], optional
            The length values of each expected return parameter. If
            only 1 return is expected, this value does not need to
            be provided.
        endianness : Endian
            Endian byte order to apply during deserialization.
        signed : bool
            Are the return values signed integers?

        Returns
        -------
        Union[List[int], int]
            The parsed return parameter(s).

        """
        if self.evt_code == EventCode.COMMAND_COMPLETE:
            param_bytes = self.evt_params[4:]

        if not param_lens:
            return int.from_bytes(param_bytes, endianness.value, signed=signed)

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
