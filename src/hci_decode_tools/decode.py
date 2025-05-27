# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module contains utilities for decoding HCI packets.

This module defines utility functions which can be used
to decode either singular HCI packets or multiple HCI
packets from a test or binary file.

Usage
-----
Example: Decoding a single HCI packet

.. code-block:: python

    import hci_decode_tools
    # example packet: controller.reset
    hci_packet = int.to_bytes(0x01030C00, length=4, byteorder="big")
    print(hci_decode_tools.decode_packet(hci_packet))

Example: Decoding multiple HCI packets from a binary file

.. code-block:: python

    import hci_decode_tools
    # example file: packets.bin
    fname = "packets.bin"
    print(hci_decode_tools.decode_bytes_file(fname))

Example: Decoding multiple HCI packets from a text file

.. code-block:: python

    import hci_decode_tools
    # example file: packets.txt
    fname = "packets.txt"
    # example host->controller tag: TX: (include whitespace)
    # example controller->host tag: RX: (include whitespace)
    h2c_tag = "TX: "
    c2h_tag = "RX: "
    print(hci_decode_tools.decode_text_file(fname, h2c_tag=h2c_tag, c2h_tag=c2h_tag))

"""
import binascii
import os
from typing import List, Optional
from .packets.acl_packet import AclPacket
from .packets.command_packet import CommandPacket
from .packets.event_packet import EventPacket

def decode_packet(packet: bytes) -> str:
    """Decode an HCI packet.

    Parameters
    ----------
    packet : bytes
        Packet to decode.

    Returns
    -------
    str
        Decoded and formatted packet.

    """
    packet_code = packet[0]
    packet = packet[1:]
    if packet_code == AclPacket.PACKET_ID:
        return AclPacket.from_bytes(packet).parse_packet()
    if packet_code == CommandPacket.PACKET_ID:
        return CommandPacket.from_bytes(packet).parse_packet()
    if packet_code == EventPacket.PACKET_ID:
        return EventPacket.from_bytes(packet).parse_packet()
    return "--Invalid packet ID--"

def decode_bytes_file(fname: str) -> str:
    """Decode HCI packets from a binary file.

    Parameters
    ----------
    fname : str
        Path of the binary file to decode.

    Returns
    -------
    str
        All packets in the file decoded and formatted.

    """
    rstr = ""
    with open(fname, "rb") as hci_stream:
        hci_stream.seek(0, os.SEEK_END)
        eof = hci_stream.tell()
        hci_stream.seek(0, os.SEEK_SET)
        while True:
            pkt = hci_stream.read(1)
            pkt_code = int.from_bytes(pkt[0:], byteorder="little")
            pkt_len = 0
            if pkt_code == AclPacket.PACKET_ID:
                pkt += hci_stream.read(4)
                pkt_len = int.from_bytes(pkt[3:], byteorder="little")
            elif pkt_code == CommandPacket.PACKET_ID:
                pkt += hci_stream.read(3)
                pkt_len = int.from_bytes(pkt[3:], byteorder="little")
            elif pkt_code == EventPacket.PACKET_ID:
                pkt += hci_stream.read(2)
                pkt_len = int.from_bytes(pkt[2:], byteorder="little")
            else:
                pkt = int.from_bytes(pkt, byteorder="big")
                print(f"--Invalid packet ID: {pkt:X}--")
                continue
            pkt += hci_stream.read(pkt_len)
            rstr += f"{decode_packet(pkt)}\n"

            if hci_stream.tell() == eof:
                break
    return rstr

def decode_text_file(
    fname: str,
    leading: Optional[List[str]] = None,
    c2h_tag: Optional[str] = None,
    h2c_tag: Optional[str] = None
) -> str:
    """Decode HCI packets from a text-based file.

    Parameters
    ----------
    fname : str
        Path of the file to decode.

    Returns
    -------
    str
        All packets in the file decoded and formatted.

    """
    rstr = ""
    with open(fname, "r", encoding="utf-8") as hci_stream:
        for line in hci_stream.readlines():
            line = line.strip()
            if not line:
                continue
            if c2h_tag is not None and line.startswith(c2h_tag):
                rstr += "[Controller-->Host]\n"
                line = line.replace(c2h_tag, "")
            elif h2c_tag is not None and line.startswith(h2c_tag):
                    rstr += "[Host-->Controller]\n"
                    line = line.replace(h2c_tag, "")
            elif leading is not None:
                is_pkt = False
                for leader in leading:
                    if line.startswith(leader):
                        line = line.replace(leader, "")
                        is_pkt = True
                        break
                if not is_pkt:
                    continue
            rstr += f"{decode_packet(binascii.unhexlify(line))}\n"
    return rstr
