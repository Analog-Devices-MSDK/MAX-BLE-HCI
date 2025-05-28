# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module defines an HCI event packet deserializer.

This module contains the definition of the `EventPacket` class,
which can be used to deserialize, decode, and format HCI event
packets.

Usage
-----
Example: Decoding an HCI event packet

.. code-block:: python

    from hci_decode_tools.packets import EventPacket
    # example packet: host number of completed packets (ignore packet id)
    pkt_bytes = int.to_bytes(0x13050110000100, length=7, byteorder="big)
    pkt = EventPacket.from_bytes(pkt_bytes)
    print(pkt.parse_packet())

"""
from __future__ import annotations
from typing import List, Tuple, Union
from ..packet_codes.command import parse_opcode
from ..packet_codes.event import EventCode, SubEventCode
from ..utils._packet_structs.event_stuct import get_params
from ..utils.params import HciParam, HciParamIdxRef


class EventPacket:
    """Event packet deserialized.

    HCI event packet format:

    - Event Code -> bytes[0:1]
    - Length     -> bytes[1:2]
    - Parameters -> bytes[2: ]

    Paramters
    ---------
    code : EventCode
        Packet-defined event code.
    length : int
        Packet length.
    params : bytes
        Packet-defined parameters.

    Attributes
    ----------
    PACKET_ID : int
        Event packet ID, first byte of an HCI
        event packet transmission. Value is `0x04`.
    code : EventCode
        Event code.
    length : int
        Packet length.
    params : bytes
        Event parameters.

    """

    PACKET_ID = 0x04

    def __init__(self, code: EventCode, length: int, params: bytes) -> None:
        self.code = code
        self.length = length
        self.params = params
        self._p_idx = None
        self._p_vals = None

    @staticmethod
    def from_bytes(packet: bytes) -> EventPacket:
        """Create an `EventPacket` object from bytes.

        Deserializes an HCI even packet from a bytes object.

        Parameters
        ----------
        packet : bytes
            Packet to deserialize.

        Returns
        -------
        EventPacket
            Deserialized packet.

        """
        code = EventCode(int.from_bytes(packet[0:1], byteorder="little"))
        length = int.from_bytes(packet[1:2], byteorder="little")
        params = packet[2:]
        return EventPacket(code, length, params)

    def parse_packet(self) -> str:
        """Parse and format a deserialized event packet.

        Returns
        -------
        str
            The formatted event packet.

        """
        rstr = "PacketType=Event\n"
        rstr += f"EventCode={self.code.name}\n"
        rstr += f"Length={self.length}\n"

        param_code = self.code
        self._p_idx = 0
        if self.code == EventCode.COMMAND_COMPLETE:
            rstr += f"NumHciCommand={int.from_bytes(self.params[0:1], byteorder='little')}\n"
            ogf, ocf = parse_opcode(
                int.from_bytes(self.params[1:3], byteorder="little")
            )
            rstr += f"Command={ogf.name}.{ocf.name}\n"
            param_code = (ogf, ocf)
            self._p_idx += 3
        elif self.code == EventCode.LE_META:
            sub_code = SubEventCode(int.from_bytes(self.params[0], byteorder="little"))
            rstr += f"SubEventCode={sub_code.name}"
            param_code = sub_code
            self._p_idx += 1

        params = get_params(param_code)
        if params is None:
            rstr += "Params: None\n"
            return rstr
        rstr += "Params:\n"
        self._p_vals = []
        idx = 0
        for param in params:
            p_str, idx = self._parse_param(param, idx)
            rstr += p_str
        return rstr

    def _parse_param(
        self, param: Union[HciParam, List[HciParam]], idx: int
    ) -> Tuple[str, int]:
        """
        Parse a single event parameter.
        """
        rstr = ""
        if isinstance(param, list):
            idxref = param.pop(0)
            maxidx = 0
            if idxref is None:
                maxidx = int(
                    (len(self.params) - self._p_idx) / sum(p.length for p in param)
                )
            else:
                maxidx = self._p_vals[idx + idxref].value
            for subidx in range(maxidx):
                for subparam in param:
                    p_str, idx = self._parse_param(subparam, idx)
                    rstr += p_str.format(subidx)
            return rstr, idx

        p_len = len(self.params) - self._p_idx if param.length is None else param.length
        if isinstance(p_len, HciParamIdxRef):
            if p_len.ref is None:
                p_len = len(self.params) - self._p_idx
            else:
                p_len = self._p_vals[idx + p_len.ref].value
        p_val = param.dtype.from_bytes(self.params[self._p_idx : self._p_idx + p_len])
        self._p_idx += p_len
        idx += 1
        rstr += f"    {param.label}={p_val}\n"
        self._p_vals.append(p_val)
        return rstr, idx
