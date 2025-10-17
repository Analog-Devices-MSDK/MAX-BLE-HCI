# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
The package `packets` contains objects which define HCI
packet deserializers.

Implmentation Details
---------------------
The objects in the `packets` package are defined as follows:

    - `AclPacket`: Deserializer for HCI ACL packets
    - `CommandPacket`: Deserializer for HCI command packets
    - `EventPacket`: Deserializer for HCI event packets

Each of the objects made available by this package contain the
static method `from_bytes` and the class method `parse_packet`.
The `from_bytes` static method allows for the creation of the
object from a byte stream, and is the intended way to initialize
and instance of thse classes. The `parse_packet` method decodes
and formats the HCI packet stored by the class instance.

"""
from .acl_packet import AclPacket
from .command_packet import CommandPacket
from .event_packet import EventPacket
