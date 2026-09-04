#! /usr/bin/env python3
###############################################################################
#
#
# Copyright (C) 2026 Maxim Integrated Products, Inc., All Rights Reserved.
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
# Copyright 2026 Analog Devices, Inc.
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
dtm_adau2100.py

Description: Simple CLI example for running BLE and BT direct test mode between
             two ADAU2100 devices (TX and RX).
"""

import argparse
import os
import signal
import sys
import threading
import time

try:
    import readline
except ImportError:
    import pyreadline3 as readline

from argparse import RawTextHelpFormatter

from max_ble_hci import BleHci
from max_ble_hci.packet_codes import StatusCode
from max_ble_hci.constants import (
    PayloadOption,
    PhyOption,
    LEPerCountMode,
    BTPerCountMode,
)

EXIT_FUNC_MAGIC = 999


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"ERROR: Invalid input. Refer to 'help' for available commands.")
        self.exit(2)


class DTMTestState:
    IDLE = "idle"
    BLE_RUNNING = "ble_running"
    BT_RUNNING = "bt_running"


class DTMTxParams:
    def __init__(self):
        self.channel = 0
        self.phy = 1
        self.payload = 0
        self.packet_length = 0
        self.packet_type = 0
        self.power = 0x7F
        self.infinite_mode = False

    def set(
        self,
        channel=None,
        phy=None,
        payload=None,
        packet_length=None,
        packet_type=None,
        power=None,
        infinite_mode=None,
    ):
        if channel is not None:
            self.channel = channel
        if phy is not None:
            self.phy = phy
        if payload is not None:
            self.payload = payload
        if packet_length is not None:
            self.packet_length = packet_length
        if packet_type is not None:
            self.packet_type = packet_type
        if power is not None:
            self.power = power
        if infinite_mode is not None:
            self.infinite_mode = infinite_mode

    def get(self):
        return {
            "channel": self.channel,
            "phy": self.phy,
            "payload": self.payload,
            "packet_length": self.packet_length,
            "packet_type": self.packet_type,
            "power": self.power,
            "infinite_mode": self.infinite_mode,
        }

    def display(self, exclude=None) -> str:
        exclude = exclude or set()
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None or key in exclude:
                continue
            print_lns.append(f"{key}:  {val}")
        return "\n".join(print_lns)

    def __repr__(self) -> str:
        return self.display()


class DTMRxParams:
    def __init__(self):
        self.channel = 0
        self.phy = 1
        self.packet_type = 0
        self.infinite_mode = False
        self.percount_mode = 0

    def set(
        self,
        channel=None,
        phy=None,
        packet_type=None,
        infinite_mode=None,
        percount_mode=None,
    ):
        if channel is not None:
            self.channel = channel
        if packet_type is not None:
            self.packet_type = packet_type
        if infinite_mode is not None:
            self.infinite_mode = infinite_mode
        if percount_mode is not None:
            self.percount_mode = percount_mode

    def get(self):
        return {
            "channel": self.channel,
            "phy": self.phy,
            "packet_type": self.packet_type,
            "infinite_mode": self.infinite_mode,
            "percount_mode": self.percount_mode,
        }

    def display(self, exclude=None) -> str:
        exclude = exclude or set()
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None or key in exclude:
                continue
            print_lns.append(f"{key}:  {val}")
        return "\n".join(print_lns)

    def __repr__(self) -> str:
        return self.display()


def calc_per(peer_tx_data: int, peer_rx_data: int) -> float:
    """Calculate PER.

    Calculates the Packet Error Rate of the current set of
    statistics.

    Parameters
    ----------
    peer_tx_data : int
        Number of packets transmitted by the tx device.
    peer_rx_data : int
        Number of packets received by the rx device.

    Returns
    -------
    float
        Calculated PER value.

    """
    try:
        return 100 - (100 * (peer_rx_data / peer_tx_data))
    except ZeroDivisionError:
        return float("NaN")


def _signal_handler(_signal, _fname):
    print()
    sys.exit(0)


def _init_cli():
    signal.signal(signal.SIGINT, _signal_handler)

    cli_description = """
        DTM ADAU2100 Test CLI.
        Runs BLE and BT Direct Test Mode between a TX and RX device.
        """

    parser = argparse.ArgumentParser(
        description=cli_description, formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("tx_port", help="Serial port path for the TX device")
    parser.add_argument("rx_port", help="Serial port path for the RX device")

    parser.add_argument(
        "-b",
        "--baud",
        type=int,
        default=921600,
        help="Serial port baud rate. Default: 921600",
    )

    parser.add_argument(
        "-efc",
        "--enable-flow-control",
        action="store_true",
        default=True,
        help="Enable flow control. Default: True",
    )

    parser.add_argument(
        "--stop-bits",
        type=int,
        default=1,
        help="Number of stop bits. Default: 1",
    )

    return parser.parse_args()


def main():
    """MAIN"""

    args = _init_cli()

    tx_hci = BleHci(
        args.tx_port,
        baud=args.baud,
        flowcontrol=args.enable_flow_control,
        stopbits=args.stop_bits,
    )
    rx_hci = BleHci(
        args.rx_port,
        baud=args.baud,
        flowcontrol=args.enable_flow_control,
        stopbits=args.stop_bits,
    )

    tx_status = tx_hci.reset()
    rx_status = rx_hci.reset()

    if tx_status is not StatusCode.SUCCESS or rx_status is not StatusCode.SUCCESS:
        print("ERROR: No connection established.")
        sys.exit(0)

    print("DTM ADAU2100 Test CLI")
    print(f"TX port: {args.tx_port}")
    print(f"RX port: {args.rx_port}")
    print(f"Baud: {args.baud}")

    test_state = DTMTestState.IDLE
    test_duration_s = 10
    test_timer = None
    enable_timer = False

    tx_ble_params = DTMTxParams()
    rx_ble_params = DTMRxParams()

    tx_bt_params = DTMTxParams()
    rx_bt_params = DTMRxParams()

    terminal = ArgumentParser(prog="", add_help=True)
    subparsers = terminal.add_subparsers()

    # Commands allowed while a test is running
    ALWAYS_ALLOWED_COMMANDS = {
        "reset",
        "exit",
        "quit",
        "q",
        "help",
        "h",
        "clear",
        "cls",
        "stop-ble-test",
        "xble",
        "stop-bt-test",
        "xbt",
        "print-config",
        "pc",
    }

    #### SET BLE TEST PARAMS PARSER ####
    set_ble_params_parser = subparsers.add_parser(
        "set-ble-test-params",
        aliases=["sblep"],
        help="Set BLE test parameters",
        formatter_class=RawTextHelpFormatter,
    )
    set_ble_params_parser.add_argument(
        "-c",
        "--channel",
        type=int,
        dest="channel",
        default=None,
        help="TX test channel, 0-39. Default: 0",
    )
    set_ble_params_parser.add_argument(
        "--phy",
        dest="phy",
        type=int,
        default=None,
        help="""Tx Test PHY
        1: 1M
        2: 2M
        3: S8
        4: S2
        Default: 1M""",
    )
    set_ble_params_parser.add_argument(
        "-p",
        "--payload",
        dest="payload",
        type=int,
        default=None,
        help="""Tx Test Payload
        0: PRBS9
        1:11110000
        2:10101010
        3: PRBS15
        4: 11111111
        5:00000000
        6:00001111
        7: 01010101
        Default: PRBS9""",
    )
    set_ble_params_parser.add_argument(
        "-pl",
        "--packet-length",
        type=int,
        default=None,
        help="Tx packet length, number of bytes per packet, 0-255. Default: 0",
    )
    set_ble_params_parser.add_argument(
        "--power",
        dest="tx_power",
        type=int,
        default=None,
        help="""Set the Tx power level, signed int
        0x7F: min
        0x7E: max
        Default: 0""",
    )
    set_ble_params_parser.add_argument(
        "-pcm",
        "--percount-mode",
        dest="percount_mode",
        type=int,
        default=None,
        help="""Percount mode.
            0: Number of correctly received packets (no error)
            1: Number of Access Address detection error only
            2: Number of CRC Error detection only
            3: Reception Error detected
            Default: 0""",
    )

    def _set_ble_test_params(args):
        tx_ble_params.set(
            channel=args.channel,
            phy=args.phy,
            payload=args.payload,
            packet_length=args.packet_length,
            power=args.tx_power,
        )
        rx_ble_params.set(
            channel=args.channel,
            phy=args.phy,
            percount_mode=args.percount_mode,
        )
        print(
            f"TX Parameters have been set to:\n{tx_ble_params.display(exclude={'packet_type', 'infinite_mode'})}\n"
        )
        print(
            f"RX Parameters have been set to:\n{rx_ble_params.display(exclude={'packet_type', 'infinite_mode'})}"
        )

    set_ble_params_parser.set_defaults(
        func=_set_ble_test_params, cmd_name="set-ble-test-params"
    )

    #### SET BT TEST PARAMS PARSER ####
    set_bt_params_parser = subparsers.add_parser(
        "set-bt-test-params",
        aliases=["sbtp"],
        help="Set BT Classic test parameters",
        formatter_class=RawTextHelpFormatter,
    )
    set_bt_params_parser.add_argument(
        "-c",
        "--channel",
        type=int,
        dest="channel",
        default=None,
        help="Tx test channel. Default: 0",
    )
    set_bt_params_parser.add_argument(
        "-pl",
        "--packet-length",
        dest="packet_length",
        type=int,
        default=None,
        help="Tx packet length, number of bytes per packet, 0-1021. Default: 0",
    )
    set_bt_params_parser.add_argument(
        "-p",
        "--payload",
        dest="payload",
        type=int,
        default=None,
        help="""Tx Test Payload
        0: PRBS9
        1: 11110000
        2: 10101010
        3: PRBS15
        4: 11111111
        5: 00000000
        6: 00001111
        7: 01010101
        Default: PRBS9
        """,
    )
    set_bt_params_parser.add_argument(
        "-pt",
        "--packet-type",
        dest="packet_type",
        type=int,
        default=None,
        help="""Tx Test packet type
        0: DM1
        1: DH1
        2: DM3
        3: DH3
        4: DM5
        5: DH5
        6: 2DH1
        7: 3DH1
        8: 2DH3
        9: 3DH3
        10: 2DH5
        11: 3DH5
        12: HV1
        13: HV2
        14: HV3
        15: EV3
        16: EV4
        17: EV5
        18: 2EV3
        19: 3EV3
        20: 2EV5
        21: 3EV5
        Default: DH1""",
    )
    set_bt_params_parser.add_argument(
        "--power",
        dest="tx_power",
        type=int,
        default=None,
        help="Transmit power -127 to 20 dBm. Default: 0",
    )
    set_bt_params_parser.add_argument(
        "-pcm",
        "--percount-mode",
        dest="percount_mode",
        type=int,
        default=None,
        help="""Percount mode.
            0: Number of correctly received packets (no error)
            1: Number of Access Address detection error only
            2: Number of HEC Error detection only
            4: Number of CRC Error detection only
            Default: 0""",
    )

    def _set_bt_test_params(args):
        tx_bt_params.set(
            channel=args.channel,
            payload=args.payload,
            packet_length=args.packet_length,
            packet_type=args.packet_type,
            power=args.tx_power,
        )
        rx_bt_params.set(
            channel=args.channel,
            percount_mode=args.percount_mode,
        )
        print(
            f"TX Parameters have been set to:\n{tx_bt_params.display(exclude={'phy', 'infinite_mode'})}\n"
        )
        print(
            f"RX Parameters have been set to:\n{rx_bt_params.display(exclude={'phy', 'infinite_mode'})}"
        )

    set_bt_params_parser.set_defaults(
        func=_set_bt_test_params, cmd_name="set-bt-test-params"
    )

    #### SET TIME DURATION PARSER ####
    set_time_parser = subparsers.add_parser(
        "set-time-duration",
        aliases=["st"],
        help="Set the test time duration (in seconds)",
        formatter_class=RawTextHelpFormatter,
    )
    set_time_parser.add_argument(
        "time",
        type=float,
        default=1,
        help="The time duration (in seconds) of a test",
    )

    def _set_time_duration(args):
        nonlocal test_duration_s
        test_duration_s = args.time
        print(f"Test duration set to {test_duration_s}s")

    set_time_parser.set_defaults(func=_set_time_duration, cmd_name="set-time-duration")

    #### ENABLE TIMER PARSER ####
    enable_timer_parser = subparsers.add_parser(
        "enable-timer",
        aliases=["et"],
        help="Enable/disable the auto-stop timer for tests",
        formatter_class=RawTextHelpFormatter,
    )
    enable_timer_parser.add_argument(
        "enable",
        type=int,
        choices=[0, 1],
        help="0: Disable, 1: Enable",
    )

    def _enable_timer(args):
        nonlocal enable_timer
        enable_timer = bool(args.enable)
        state_str = "Enabled" if enable_timer else "Disabled"
        print(f"Auto-stop timer {state_str}")

    enable_timer_parser.set_defaults(func=_enable_timer, cmd_name="enable-timer")

    #### CW MODE PARSER ####
    cw_mode_parser = subparsers.add_parser(
        "cw-mode",
        aliases=["cw"],
        help="Enable/disable CW (infinite) mode for BLE and BT",
        formatter_class=RawTextHelpFormatter,
    )
    cw_mode_parser.add_argument(
        "enable",
        type=int,
        choices=[0, 1],
        help="0: Disable, 1: Enable",
    )

    def _cw_mode(args):
        enable = bool(args.enable)
        tx_ble_params.set(infinite_mode=enable, packet_length=1, payload=4)
        rx_ble_params.set(infinite_mode=enable)
        tx_bt_params.set(infinite_mode=enable, packet_length=1, payload=4)
        rx_bt_params.set(infinite_mode=enable)
        state_str = "Enabled" if enable else "Disabled"
        print(f"CW mode {state_str}")

    cw_mode_parser.set_defaults(func=_cw_mode, cmd_name="cw-mode")

    #### PRINT CONFIG PARSER ####
    print_config_parser = subparsers.add_parser(
        "print-config",
        aliases=["pc"],
        help="Print current BLE and BT DTM configurations",
        formatter_class=RawTextHelpFormatter,
    )

    def _print_config(args):
        ble_exclude = {"packet_type", "infinite_mode"}
        bt_exclude = {"phy", "infinite_mode"}
        print("=== BLE Configuration ===")
        print("  TX Parameters:")
        print(
            f"    {tx_ble_params.display(exclude=ble_exclude)}".replace("\n", "\n    ")
        )
        print("  RX Parameters:")
        print(
            f"    {rx_ble_params.display(exclude=ble_exclude)}".replace("\n", "\n    ")
        )
        print()
        print("=== BT Configuration ===")
        print("  TX Parameters:")
        print(f"    {tx_bt_params.display(exclude=bt_exclude)}".replace("\n", "\n    "))
        print("  RX Parameters:")
        print(f"    {rx_bt_params.display(exclude=bt_exclude)}".replace("\n", "\n    "))
        print()
        cw_str = "Enabled" if tx_ble_params.infinite_mode else "Disabled"
        timer_str = "Enabled" if enable_timer else "Disabled"
        print(f"CW Mode: {cw_str}")
        print(f"Auto-Stop Timer: {timer_str}")
        print(f"Test Duration: {test_duration_s}s")

    print_config_parser.set_defaults(func=_print_config, cmd_name="print-config")

    #### RESET PARSER ####
    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset both TX and RX devices",
        formatter_class=RawTextHelpFormatter,
    )

    def _reset(args):
        nonlocal test_state, test_timer
        if test_timer is not None:
            test_timer.cancel()
            test_timer = None
        print(f"TX Status Code: {tx_hci.reset()}")
        print(f"RX Status Code: {rx_hci.reset()}")
        test_state = DTMTestState.IDLE

    reset_parser.set_defaults(func=_reset, cmd_name="reset")

    #### START BLE TEST PARSER ####
    start_ble_parser = subparsers.add_parser(
        "start-ble-test",
        aliases=["sble"],
        help="Start a BLE DTM test",
        formatter_class=RawTextHelpFormatter,
    )

    def _start_ble_test(args):
        nonlocal test_state, test_timer
        test_state = DTMTestState.BLE_RUNNING

        print(tx_hci.infinite_txrx_vs(tx_ble_params.infinite_mode))
        print(rx_hci.infinite_txrx_vs(rx_ble_params.infinite_mode))
        print(rx_hci.percount_mode_vs(rx_ble_params.percount_mode))

        time.sleep(0.1)

        print(
            rx_hci.rx_test(
                channel=rx_ble_params.channel, phy=PhyOption(rx_ble_params.phy)
            )
        )

        time.sleep(0.1)
        print(
            tx_hci.tx_test(
                mode=4,
                channel=tx_ble_params.channel,
                phy=PhyOption(tx_ble_params.phy),
                payload=PayloadOption(tx_ble_params.payload),
                packet_len=tx_ble_params.packet_length,
                cte_len=0,
                cte_type=255,
                power=tx_ble_params.power,
            )
        )

        if enable_timer and not tx_ble_params.infinite_mode:
            print(f"BLE test started. Will auto-stop in {test_duration_s}s.")
            test_timer = threading.Timer(test_duration_s, _stop_ble_test, args=[None])
            test_timer.daemon = True
            test_timer.start()
        else:
            print("BLE test started. Use 'stop-ble-test' to end.")

    start_ble_parser.set_defaults(func=_start_ble_test, cmd_name="start-ble-test")

    #### START BT TEST PARSER ####
    start_bt_parser = subparsers.add_parser(
        "start-bt-test",
        aliases=["sbt"],
        help="Start a BT Classic DTM test",
        formatter_class=RawTextHelpFormatter,
    )

    def _start_bt_test(args):
        nonlocal test_state, test_timer
        test_state = DTMTestState.BT_RUNNING
        print(
            rx_hci.rx_test_bt_vs(
                channel=rx_bt_params.channel,
                packet_type=rx_bt_params.packet_type,
                inf_test=bool(rx_bt_params.infinite_mode),
                percount_mode=rx_bt_params.percount_mode,
            )
        )
        time.sleep(0.1)
        print(
            tx_hci.tx_test_bt_vs(
                channel=tx_bt_params.channel,
                packet_len=tx_bt_params.packet_length,
                payload=tx_bt_params.payload,
                packet_type=tx_bt_params.packet_type,
                tx_power=tx_bt_params.power,
                inf_test=bool(tx_bt_params.infinite_mode),
            )
        )

        if enable_timer and not tx_bt_params.infinite_mode:
            print(f"BT test started. Will auto-stop in {test_duration_s}s.")
            test_timer = threading.Timer(test_duration_s, _stop_bt_test, args=[None])
            test_timer.daemon = True
            test_timer.start()
        else:
            print("BT test started. Use 'stop-bt-test' to end.")

    start_bt_parser.set_defaults(func=_start_bt_test, cmd_name="start-bt-test")

    #### STOP BLE TEST PARSER ####
    stop_ble_parser = subparsers.add_parser(
        "stop-ble-test",
        aliases=["xble"],
        help="Stop the running BLE DTM test",
        formatter_class=RawTextHelpFormatter,
    )

    def _stop_ble_test(args):
        nonlocal test_state, test_timer
        if test_state != DTMTestState.BLE_RUNNING:
            print("No BLE test is currently running.")
            return
        if test_timer is not None:
            test_timer.cancel()
            test_timer = None

        nb_packets_transmitted, tx_status = tx_hci.end_test()
        time.sleep(0.1)
        metrics, rx_status = rx_hci.end_ex_test()
        tx_hci.reset()
        rx_hci.reset()
        print(f"\nTX Packets Transmitted: {nb_packets_transmitted}")
        print(f"TX Status: {tx_status}\n")

        print(f"RX Packets Received: {metrics.nb_packets}")
        print(f"RX RSSI Minimum: {metrics.rssi_min} dBm")
        print(f"RX RSSI Maximum: {metrics.rssi_max} dBm")
        print(f"RX RSSI Average: {metrics.rssi_avg} dBm")
        print(f"RX Status: {rx_status}")

        if LEPerCountMode(rx_ble_params.percount_mode) == LEPerCountMode.CORRECT:
            print(
                f"PER calculated: {calc_per(nb_packets_transmitted, metrics.nb_packets)}"
            )
        test_state = DTMTestState.IDLE

    stop_ble_parser.set_defaults(func=_stop_ble_test, cmd_name="stop-ble-test")

    #### STOP BT TEST PARSER ####
    stop_bt_parser = subparsers.add_parser(
        "stop-bt-test",
        aliases=["xbt"],
        help="Stop the running BT Classic DTM test",
        formatter_class=RawTextHelpFormatter,
    )

    def _stop_bt_test(args):
        nonlocal test_state, test_timer
        if test_state != DTMTestState.BT_RUNNING:
            print("No BT test is currently running.")
            return
        if test_timer is not None:
            test_timer.cancel()
            test_timer = None

        tx_nb_packets, tx_status = tx_hci.test_end_bt_vs()
        time.sleep(0.1)
        rx_nb_packets, rx_status = rx_hci.test_end_bt_vs()
        tx_hci.reset()
        rx_hci.reset()
        print(f"\nTX Packets Transmitted: {tx_nb_packets}")
        print(f"TX Status: {tx_status}\n")

        print(f"RX Packets Received: {rx_nb_packets}")
        print(f"RX Status: {rx_status}")

        if BTPerCountMode(rx_bt_params.percount_mode) == BTPerCountMode.CORRECT:
            print(f"PER calculated: {calc_per(tx_nb_packets, rx_nb_packets)}")
        test_state = DTMTestState.IDLE

    stop_bt_parser.set_defaults(func=_stop_bt_test, cmd_name="stop-bt-test")

    #### CLEAR PARSER ####
    clear_parser = subparsers.add_parser(
        "clear",
        aliases=["cls"],
        help="Clear the screen",
        formatter_class=RawTextHelpFormatter,
    )
    clear_parser.set_defaults(
        func=lambda _: os.system("cls" if os.name == "nt" else "clear"),
        cmd_name="clear",
    )

    #### EXIT PARSER ####
    exit_parser = subparsers.add_parser(
        "exit",
        aliases=["quit", "q"],
        help="Exit the program",
        formatter_class=RawTextHelpFormatter,
    )
    exit_parser.set_defaults(func=lambda _: sys.exit(EXIT_FUNC_MAGIC), cmd_name="exit")

    #### HELP PARSER ####
    help_parser = subparsers.add_parser("help", aliases=["h"], help="Show help message")
    help_parser.set_defaults(func=lambda _: terminal.print_help(), cmd_name="help")

    def _completer(text, state):
        commands = subparsers.choices.keys()
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        return matches[state] if state < len(matches) else None

    readline.set_completer(_completer)
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(readline.get_completer_delims().replace("-", ""))

    while True:
        command_str = input(">>> ")

        if command_str in ("", "\n"):
            continue

        cmd_name = command_str.split()[0]

        if test_state != DTMTestState.IDLE:
            if cmd_name not in ALWAYS_ALLOWED_COMMANDS:
                print(
                    f"Test in progress ({test_state}). "
                    "Only 'reset', 'exit', 'stop-ble-test', or 'stop-bt-test' allowed."
                )
                continue

        if test_state == DTMTestState.IDLE:
            if cmd_name in ("stop-ble-test", "xble"):
                print("No BLE test is currently running.")
                continue
            if cmd_name in ("stop-bt-test", "xbt"):
                print("No BT test is currently running.")
                continue

        try:
            parsed_args = terminal.parse_args(command_str.split())
            try:
                parsed_args.func(parsed_args)
            except AttributeError as err:
                print(f"ERROR: {err}")
                continue

        except SystemExit as err:
            if err.code == EXIT_FUNC_MAGIC:
                sys.exit(0)
            elif err.code != 0:
                print(f"Process finished with exit code {err.code}")

        except Exception as err:
            print(f"Unexpected exception: {type(err).__name__}: {err}")


if __name__ == "__main__":
    main()
