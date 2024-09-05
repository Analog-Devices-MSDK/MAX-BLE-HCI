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
firmware_update.py

Description: This is an example to show how to update the firmware through HCI script.

"""
from max_ble_hci import BleHci
from max_ble_hci.packet_codes import StatusCode

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6J1-if00-port0"


def main():
    """MAIN"""
    conn = BleHci(PORT)

    # make sure you have to erase the flash memory before you flash to it

    # Page size of flash memory
    PAGE_SIZE = 0x2000  # this is the page size of MAX32655
    address_to_erase = 0x10040000
    erased_size = 0x38000

    result = None

    while erased_size > 0:
        result = conn.erase_page(address_to_erase)
        if result != StatusCode.SUCCESS:
            print(result)
            return
        erased_size -= PAGE_SIZE
        address_to_erase += PAGE_SIZE

    result = conn.firmware_update(0x10040000, "hello_world.bin")
    if result != StatusCode.SUCCESS:
        print(result)
        return

    # reset the device to reload the uploaded firmware
    result = conn.reset_device()
    if result != StatusCode.SUCCESS:
        print(result)
        return


if __name__ == "__main__":
    main()
