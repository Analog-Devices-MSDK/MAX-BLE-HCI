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
integration.py

Description: Integration tests for HCI

"""
import os
import secrets
import sys
import unittest


from max_ble_hci import BleHci
from max_ble_hci import packet_codes as pc
from max_ble_hci.constants import PhyOption, PubKeyValidateMode


if len(sys.argv) > 1:
    PORT = sys.argv[1]
    # gotta get rid of it before unittest takes it
    sys.argv.pop()
elif os.environ.get("TEST_PORT"):
    PORT = os.environ.get("TEST_PORT")
else:
    PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"

hci1 = BleHci(PORT, id_tag="hci1", timeout=5)

MAX_U32 = 0xFFFFFFFF
A32 = 0xAAAAAAAA


# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
class TestHci(unittest.TestCase):
    def test_reset(self):
        # Reset puts code into nice condition, make sure it works before any tests
        self.assertEqual(hci1.reset(), pc.StatusCode.SUCCESS)

    def test_commands(self):
        hci1.reset()

        self.assertEqual(hci1.set_tx_test_err_pattern(A32), pc.StatusCode.SUCCESS)
        self.assertIsNotNone(hci1.set_connection_op_flags(1, MAX_U32, True))

        key = list(secrets.token_bytes(32))
        self.assertEqual(hci1.set_256_priv_key(key), pc.StatusCode.SUCCESS)
        self.assertEqual(
            hci1.get_channel_map_periodic_scan_adv(1, False)[1],
            pc.StatusCode.SUCCESS,
        )
        self.assertIsNotNone(hci1.get_acl_test_report())

        self.assertEqual(
            hci1.set_local_num_min_used_channels(PhyOption.PHY_1M, 0, 10),
            pc.StatusCode.SUCCESS,
        )

        self.assertEqual(
            hci1.get_peer_min_num_channels_used(1)[1],
            pc.StatusCode.ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(
            hci1.set_validate_pub_key_mode(PubKeyValidateMode.ALT1),
            pc.StatusCode.SUCCESS,
        )

        addr, status = hci1.get_rand_address()

        self.assertTrue(addr > 0 or status != pc.StatusCode.SUCCESS)

        self.assertEqual(hci1.set_local_feature(0), pc.StatusCode.SUCCESS)

        self.assertEqual(hci1.set_operational_flags(0, True), pc.StatusCode.SUCCESS)

        self.assertEqual(
            hci1.set_encryption_mode(1, True, True),
            pc.StatusCode.ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(hci1.set_diagnostic_mode(True), pc.StatusCode.SUCCESS)

    def test_stats(self):
        """Test status functions"""
        stats, status = hci1.get_pdu_filter_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_memory_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)
        stats, status = hci1.get_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_conn_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_test_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_aux_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_aux_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)
        self.assertEqual(
            hci1.set_connection_phy_tx_power(1, 0, PhyOption.PHY_1M),
            pc.StatusCode.ERROR_CODE_UNKNOWN_CONN_ID,
        )


if __name__ == "__main__":
    unittest.main()
