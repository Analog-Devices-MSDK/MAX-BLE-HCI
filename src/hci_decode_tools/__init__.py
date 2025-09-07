# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
HCI Decode Tools
================

The HCI Decode Tools library provices an API for decoding HCI commands.

Modules
-------
packet_codes
    Contains HCI packet identification code definitions.
packets
    Contains HCI packet deserializers.
utils
    Contains HCI packet decoding utilities.

Classes
-------
`HciSerialSniffer`: Sniff and decode HCI packets from a serial port.
`HciSerialSnifferPortCfg`: Sniffer serial port configuration container.
`packets.AclPacket`: HCI ACL packet deserializer.
`packets.CommandPacket`: HCI command packet deserializer.
`packets.EventPacket`: HCI event packet deserializer.

Functions
---------
`decode_packet`: Decode a single HCI packet.
`decode_bytes_file`: Decode multiple HCI packets from a binary file.
`decode_text_file`: Decode multiple HCI packets from a text file.

CLI
---
`hcitools`: CLI interface for HCI packet decoding.

"""
from .decode import decode_bytes_file, decode_packet, decode_text_file
