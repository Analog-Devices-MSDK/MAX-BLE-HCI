# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module defines an HCI ACL packet deserializer.

This module contains the definition of the `AclPacket` class,
which can be used to deserialize, decode, and format HCI ACL
packets.

Usage
-----
Example: Decoding an HCI ACL packet

.. code-block:: python

    from hci_decode_tools.packets import AclPacket
    # example packet: l2cap information request (ignore packet id)
    pkt_bytes = int.to_bytes(0x10000A00060001000A0102000200, length=20, byteorder="big")
    pkt = AclPacket.from_bytes(pkt_bytes)
    print(pkt.parse_packet())

"""
from __future__ import annotations
from typing import List, Tuple, Union
from ..packet_codes.acl import L2CAPSignalingCodes
from ..utils._packet_structs.acl_struct import get_params
from ..utils.params import HciParam, HciParamIdxRef


class AclPacket:
    # pylint: disable=too-many-instance-attributes
    """ACL packet deserializer.

    HCI ACL packet format:

    - Connection Handle -> bytes=[0:2], bits=[ 0:11]
    - BC Flag           -> bytes=[0:2], bits=[12:14]
    - PB Flag           -> bytes=[0:2], bits=[14:  ]
    - Packet Length     -> bytes=[2:4]
    - Payload Length    -> bytes=[4:6]
    - Channel ID        -> bytes=[6:8]
    - Payload           -> bytes=[8: ]

    Parameters
    ----------
    connection_handle : int
        Packet-defined connection handle.
    bc_flag : int
        Packet-defined BC flag.
    pb_flag : int
        Packet-defined PB flag.
    lengths : Tuple[int, int]
        Data lengths in the format `(packet_length, payload_length)`.
    channel_id : int
        Packet-defined channel ID.
    packet_data : bytes
        Packet-defined payload data.

    Attributes
    ----------
    PACKET_ID : int
        ACL packet ID, first byte of an HCI ACL packet
        transmission. Value is `0x02`.
    connection_handle : int
        Connection handle.
    bc_flag : int
        BC flag.
    pb_flag : int
        PB flag.
    packet_length : int
        Total packet length.
    payload_length : int
        Packet payload length.
    channel_id : int
        Channel ID.
    packet_data : bytes
        Packet payload data.

    """
    PACKET_ID = 0x02

    def __init__(
        self,
        connection_handle: int,
        bc_flag: int,
        pb_flag: int,
        lengths: Tuple[int, int],
        channel_id: int,
        packet_data: bytes,
    ) -> None:
        self.connection_handle = connection_handle
        self.bc_flag = bc_flag
        self.pb_flag = pb_flag
        self.packet_length, self.payload_length = lengths
        self.channel_id = channel_id
        self.packet_data = packet_data
        self._p_idx = None
        self._p_vals = None

    @staticmethod
    def from_bytes(packet: bytes) -> AclPacket:
        """Create an `AclPacket` object from bytes.

        Deserializes an HCI ACL packet from a bytes object.

        Parameters
        ----------
        packet : bytes
            Packet to deserialize.

        Returns
        -------
        AclPacket
            Deserialized packet.

        """
        hdl = int.from_bytes(packet[:2], byteorder="little")
        connection_handle = hdl & 0x0FFF
        bc_flag = (hdl >> 12) & 0x0003
        pb_flag = (hdl >> 14) & 0x0003
        lengths = (
            int.from_bytes(packet[2:4], byteorder="little"),
            int.from_bytes(packet[4:6], byteorder="little"),
        )
        channel_id = int.from_bytes(packet[6:8], byteorder="little")
        packet_data = packet[8:]
        return AclPacket(
            connection_handle, bc_flag, pb_flag, lengths, channel_id, packet_data
        )

    def parse_packet(self) -> str:
        """Parse and format a deserialized ACL packet.

        Returns
        -------
        str
            The formatted ACL packet.

        """
        rstr = "PacketType=ACL\n"
        rstr += f"ConnectionHandle={self.connection_handle}\n"
        rstr += f"PacketLength={self.packet_length}\n"
        if self.packet_length == 0:
            return rstr
        rstr += f"PayloadLength={self.payload_length}\n"
        rstr += f"ChannelId={self.channel_id}\n"

        if not self.channel_id in [0x01, 0x05]:
            rstr += (
                f"PacketData: {int.from_bytes(self.packet_data, byteorder='little')}\n"
            )
            return rstr
        code = L2CAPSignalingCodes(
            int.from_bytes(self.packet_data[0:1], byteorder="little")
        )
        rstr += f"SignalingCode={code.name}\n"
        rstr += (
            f"PacketId={int.from_bytes(self.packet_data[1:2], byteorder='little')}\n"
        )
        rstr += (
            f"DataLength={int.from_bytes(self.packet_data[2:4], byteorder='little')}\n"
        )
        self._p_idx = 4
        params = get_params(code)
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
        Parse a single command parameter.
        """
        rstr = ""
        if isinstance(param, list):
            idxref = param.pop(0).ref
            maxidx = 0
            if idxref is None:
                maxidx = int(
                    (len(self.packet_data) - self._p_idx) / sum(p.length for p in param)
                )
            else:
                maxidx = self._p_vals[idx + idxref].value
            for subidx in range(maxidx):
                for subparam in param:
                    p_str, idx = self._parse_param(subparam, idx)
                    rstr += p_str.format(subidx)
            return rstr, idx

        p_len = (
            len(self.packet_data) - self._p_idx
            if param.length is None
            else param.length
        )
        if isinstance(p_len, HciParamIdxRef):
            if p_len.ref is None:
                p_len = len(self.packet_data) - self._p_idx
            else:
                p_len = self._p_vals[idx + p_len.ref].value
        if p_len < 0:
            print(f"HERE: {p_len}")
            p_len = len(self.packet_data) - self._p_idx - abs(p_len)
        p_val = param.dtype.from_bytes(
            self.packet_data[self._p_idx : self._p_idx + p_len]
        )
        self._p_idx += p_len
        idx += 1
        rstr += f"    {param.label}={p_val}\n"
        self._p_vals.append(p_val)
        return rstr, idx
