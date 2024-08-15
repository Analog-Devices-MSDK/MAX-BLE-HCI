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
enc_test.py

Description: Small encryption HCI test

"""
import argparse
import sys
from datetime import datetime
import os

# pylint: disable=import-error,redefined-builtin
from cryptography.hazmat.primitives.asymmetric import ec

from rich import print


# pylint: enable=import-error,redefined-builtin
from max_ble_hci import BleHci
from max_ble_hci.hci_packets import EventPacket
from max_ble_hci.packet_codes import EventSubcode, StatusCode


class Tester:
    """Test Harness"""

    # pylint: disable=too-few-public-methods
    P256_P = (
        115792089210356248762697446949407573530086143415290314195533631308867097853951
    )
    P256_A = -3
    P256_B = (
        41058363725152142129326129780047268409114441015993725554835256314039467401291
    )

    def __init__(self, serial_port) -> None:
        self.serial_port = serial_port
        self.hci = BleHci(
            serial_port, id_tag="hci1", timeout=5, evt_callback=self._common_callback
        )

        self.event_done = False
        self.results = {}

    def _is_point_on_curve(self, xcoord, ycoord) -> bool:
        left = ycoord * ycoord
        right = (xcoord * xcoord * xcoord) + (self.P256_A * xcoord) + self.P256_B
        return (left - right) % self.P256_P == 0

    def _check_point(self, xcoord, ycoord):
        xcoord = xcoord % self.P256_P
        ycoord = ycoord % self.P256_P

        if not self._is_point_on_curve(xcoord, ycoord):
            return False

        return True

    def _pub_key_read_event(self, packet: EventPacket):
        packet.get_return_params()

        status, xcoord, ycoord = packet.get_return_params([1, 32, 32])
        status = StatusCode(status)

        if status != StatusCode.SUCCESS:
            print(f"Read pub key failed. Status: {status}")

        self.results["pub-key-read"] = self._check_point(xcoord, ycoord)

    def _dhk_event(self, packet: EventPacket):
        if (
            StatusCode(packet.evt_params[0])
            == StatusCode.ERROR_CODE_INVALID_HCI_CMD_PARAMS
        ):
            self.results["dhk"] = True
        else:
            self.results["dhk"] = False

    def _common_callback(self, packet: EventPacket):
        if packet.evt_subcode == EventSubcode.READ_LOCAL_P256_PUB_KEY_CMPLT:
            self._pub_key_read_event(packet)
        elif packet.evt_subcode == EventSubcode.GENERATE_DHKEY_CMPLT:
            self._dhk_event(packet)

        self.event_done = True

    def _run_pub_key_read(self):
        self.event_done = False
        status = self.hci.read_local_p256_pub_key()

        if status != StatusCode.SUCCESS:
            self.results["pub-key-read"] = False
            return

        while not self.event_done:
            pass

    def _run_bad_dhk(self):
        """
        TEST HCI/AEN/BI-01-C
        Generate DH Key Error With Invalid Point
        """
        # Generate a private key for use with the P-256 curve

        private_key = ec.generate_private_key(ec.SECP256R1())

        # Generate the corresponding public key
        public_key = private_key.public_key()

        # Get the x and y coordinates from the public key
        public_numbers = public_key.public_numbers()
        invalid_x_coordinate = public_numbers.x + 1_000_000
        y_coordinate = public_numbers.y

        self.event_done = False
        start = datetime.now()
        status = self.hci.generate_dhk(xcoord=invalid_x_coordinate, ycoord=y_coordinate)

        alt1_maybe_fail = False
        if status == StatusCode.SUCCESS:
            alt1_maybe_fail = True
        elif status == StatusCode.ERROR_CODE_INVALID_HCI_CMD_PARAMS:
            self.results["dhk"] = True
            self.event_done = True
            return

        while not self.event_done and (datetime.now() - start).total_seconds() < 10:
            continue

        if not self.event_done and alt1_maybe_fail:
            self.results["dhk"] = False

    def _run_simple_aes(self):
        expected_ct = "66C6C2278E3B8E053E7EA326521BAD99"
        expected_ct = list(bytes.fromhex(expected_ct))

        evt = self.hci.write_command_raw(
            "01172020bf01fb9d4ef3bc36d874f5394138684c1302f1e0dfcebdac7968574635241302"
        )

        if evt.status != StatusCode.SUCCESS:
            self.results["encryption"] = False
        else:
            cyphertext = list(evt.evt_params[4:])

            if cyphertext != expected_ct:
                self.results["encryption"] = False
            else:
                self.results["encryption"] = True

        if not self.results["encryption"]:
            print("Failed basic AES test")
            print("Resp", cyphertext)
            print("Expected", expected_ct)

    def run(self) -> bool:
        """RUN Encryption test

        Returns
        -------
        bool
            True if all pass. False if any failure
        """
        status = self.hci.reset()
        if status != StatusCode.SUCCESS:
            return False

        status = self.hci.enable_all_events()
        if status != StatusCode.SUCCESS:
            print("Failed to enable events")
            return False

        self._run_pub_key_read()
        self._run_bad_dhk()
        self.hci.disable_all_events()
        self._run_simple_aes()

        total_result = True
        for test, result in self.results.items():
            print(f"{test}:", "[green]Pass[/green]" if result else "[red]Fail[/red]")
            if not result:
                total_result = False

        return total_result


def main():
    """MAIN"""
    port = ""

    parser = argparse.ArgumentParser(description="Basic HCI Encryption tests")
    parser.add_argument("serial_port", nargs="?", help="Serial port used for HCI")
    args = parser.parse_args()

    if args.serial_port and args.serial_port != "":
        print(args.serial_port)
        port = args.serial_port
    elif os.environ.get("TEST_PORT"):
        port = os.environ.get("TEST_PORT")

    if port == "":
        raise ValueError(
            "Serial port must be specified through command line or in script"
        )

    tester = Tester(port)
    result = tester.run()

    if not result:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
