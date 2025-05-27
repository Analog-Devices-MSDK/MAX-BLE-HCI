# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module defines an HCI command packet deserializer.

This module contains the definition of the `CommandPacket` class,
which can be used to deserialize, decode. and format HCI command
packets.

Usage
-----
Example: Decoding an HCI command packet

.. code-block:: python

    from hci_decode_tools.packets import CommandPacket
    # example packet: controller.reset (ignore packet id)
    pkt_bytes = int.to_bytes(0x030C00, length=3, byteorder="big")
    pkt = CommandPacket.from_bytes(pkt_bytes)
    print(pkt.parse_packet())

"""
from __future__ import annotations
from typing import List, Tuple, Union
from ..packet_codes.command import parse_opcode
from ..utils._packet_structs.command_struct import get_params
from ..utils.params import HciParam, HciParamIdxRef

class CommandPacket:
    """Command packet deserializer.

    HCI command packet format:

    - Opcode     -> bytes[0:2]
    - Length     -> bytes[2:3]
    - Parameters -> bytes[3: ]

    Parameters
    ----------
    opcode : int
        Packet-defined opcode.
    length : int
        Packet length.
    params : bytes
        Packet-defined parameters.

    Attributes
    ----------
    PACKET_ID : int
        Command packet ID, first byte of an HCI
        command packet transmission. Value is `0x01`.
    ogf : OGF
        Command Operation Group Field.
    ocf : Union[OCF, int]
        Command Operation Control Field.
    length : int
        Packet length.
    params : bytes
        Command parameters.

    """
    PACKET_ID = 0x01
    def __init__(self, opcode: int, length: int, params: bytes) -> None:
        self.ogf, self.ocf = parse_opcode(opcode)
        self.length = length
        self.params = params
        self._p_idx = None
        self._p_vals = None

    @staticmethod
    def from_bytes(packet: bytes) -> CommandPacket:
        """Create a `CommandPacket` object from bytes.

        Deserializes an HCI command packet from a bytes object.

        Parameters
        ----------
        packet : bytes
            Packet to deserialize.

        Returns
        -------
        CommandPacket
            Deserialized packet.

        """
        opcode = int.from_bytes(packet[0:2], byteorder="little")
        length = int.from_bytes(packet[2:3], byteorder="little")
        params = packet[3:]
        return CommandPacket(opcode, length, params)

    def parse_packet(self) -> str:
        """Parse and format a deserialized command packet.

        Returns
        -------
        str
            The formatted command packet.

        """
        rstr = "PacketType=Command\n"
        if isinstance(self.ocf, int):
            rstr += f"Command={self.ogf.name}.[OCF={self.ocf:02X}]\n"
        else:
            rstr += f"Command={self.ogf.name}.{self.ocf.name}\n"
        rstr += f"Length={self.length}\n"
        self._p_idx = 0
        params = get_params(self.ogf, self.ocf)
        if params is None:
            rstr += f"Params: None\n"
            return rstr
        rstr += f"Params:\n"
        self._p_vals = []
        idx = 0
        for param in params:
            p_str, idx = self._parse_param(param, idx)
            rstr += p_str
        return rstr

    def _parse_param(self, param: Union[HciParam, List[HciParam]], idx: int) -> Tuple[str, int]:
        """
        Parse a single command parameter.
        """
        rstr = ""
        if isinstance(param, list):
            for subidx in range(self._p_vals[idx + param.pop(0).ref].value):
                for subparam in param:
                    p_str, idx = self._parse_param(subparam, idx)
                    rstr += p_str.format(subidx)
            return rstr, idx

        p_len = param.length
        if isinstance(p_len, HciParamIdxRef):
            p_len = self._p_vals[idx + p_len.ref].value
        p_val = param.dtype.from_bytes(self.params[self._p_idx:self._p_idx + p_len])
        self._p_idx += p_len
        idx += 1
        rstr += f"    {param.label}={p_val}\n"
        self._p_vals.append(p_val)
        return rstr, idx
