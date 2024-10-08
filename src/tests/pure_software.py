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
pure_software.py

Description: Unittest for software not requiring hardware. 
Serial port required to open an HCI instance.

"""
import os
import unittest

from max_ble_hci import BleHci, utils
from max_ble_hci.hci_packets import EventCode, EventPacket, StatusCode


class Software(unittest.TestCase):
    """Softare Unit Test"""

    # pylint: disable=missing-function-docstring
    def hci_required(self):
        if os.environ.get("TEST_PORT"):
            port = os.environ.get("TEST_PORT")
        else:
            ports = utils.get_serial_ports()
            if not ports:
                return
            port = ports[0]

        hci = BleHci(port)

        expected_fips1 = [170, 187, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_fips2 = [104, 101, 108, 108, 111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        fips1 = hci.convert_fips197(0xAABB)
        fips2 = hci.convert_fips197("hello")
        self.assertEqual(fips1, expected_fips1)
        self.assertEqual(fips2, expected_fips2)

    def test_utils(self):
        ans = utils.to_le_nbyte_list(0xAABB, 4)
        self.assertEqual(ans, [0xBB, 0xAA, 0x00, 0x00])

        ans = utils.le_list_to_int(ans)
        self.assertEqual(ans, 0xAABB)

        good_data = [1, 2, 3, 4]
        ans = utils.can_represent_as_bytes(good_data)
        self.assertTrue(ans)

        bad_data = [1, 2009, 3, 4]
        ans = utils.can_represent_as_bytes(bad_data)
        self.assertFalse(ans)

        address = utils.address_str2int("00:11:22:33:44:55")
        self.assertEqual(address, 0x001122334455)

        self.assertEqual(utils.byte_length(0), 1)
        self.assertEqual(utils.byte_length(1), 1)
        self.assertEqual(utils.byte_length(254), 1)
        self.assertEqual(utils.byte_length(30_000), 2)
        self.assertEqual(utils.byte_length(-1), 1)

        reset_command = "0e0401030c00"
        evt = EventPacket.from_bytes(bytes.fromhex(reset_command))
        self.assertEqual(evt.evt_code, EventCode.COMMAND_COMPLETE)
        self.assertEqual(evt.get_return_params(), StatusCode.SUCCESS.value)

        test_addr = 0x112233445566
        expected_str_addr = "11:22:33:44:55:66"

        result = utils.address_int2str(test_addr)

        self.assertEqual(expected_str_addr, result)


if __name__ == "__main__":
    unittest.main()
