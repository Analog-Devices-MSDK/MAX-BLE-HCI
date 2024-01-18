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
The package `ble_hci` contains the `BleHci` object, which is used as a method
of communication between the test host (PC) and the test controller(s) (PCB).
The HCI is primarily used by the test controllers during board-to-board testing,
but is provided publically due to the wide range of HCI applications and use
cases.

Implementation details
----------------------
The HCI object contained in this package has many of the base HCI functions
already implemented. These include:

    - reset
    - maximize data length
    - send/sink ACL data
    - TX test (basic and vendor-specific)
    - RX test (basic and vendor-specific)
    - end test
    - PHY selection
    - TX power selection
    - BD address selection
    - channel map selection
    - start advertising
    - start scanning
    - initialize connection
    - disconnect
    - register read/write

Should an HCI command that is not currently implemented be needed, the `BleHci`
object also provides a function for sending a raw HCI command.

Classes
-------
- BleHci

Usage
-----
The `BleHci` object contains several initialization parameters which can be
used to define the board UART COM/serial port, define a string identifier
for the HCI, and specificy the HCI logging level. For the purpose of these
examples, it is assumed the COM/serial port string has already been assigned
to the variable `port`.

Create an HCI, basic:

.. code-block:: python

    hci = BleHci(port)

Create an HCI, set ID string to `'DUT'`:

.. code-block:: python

    hci = BleHci(port, id_tag='DUT')

Create an HCI, set log level to `'ERROR'`:

.. code-block:: python

    hci = BleHci(port, log_level='ERROR')

"""
from .ble_hci import BleHci
from . import constants
from . import data_params
from . import hci_packets
from . import packet_codes
from . import packet_defs
