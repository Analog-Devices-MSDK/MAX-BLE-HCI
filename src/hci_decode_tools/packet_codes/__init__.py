# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
The package `packet_codes` contains objects which define HCI
packet-specific identification codes.

Implementation Details
----------------------
The objects in the `packet_codes` package are defined as follows:

    - `acl.L2CAPSignalingCodes`: HCI ACL packet ID codes
    - `command.OCF`: HCI command packet Operation Control Field codes
    - `command.OGF`: HCI command packet Operation Group Field codes
    - `event.EventCode`: HCI event packet ID codes
    - `event.SubEventCode`: HCI LEMeta event packet ID codes

All objects made available by this package inherit from the
`Enum` class. As such, both the value and the name of these
packet codes can be accessed using the `value` and the `name`
attributes, respectively.

"""
