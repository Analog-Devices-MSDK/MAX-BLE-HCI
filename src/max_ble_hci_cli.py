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
max_ble_hci_cli.py

Description: CLI Client to use MAX-BLE-HCI

"""
import os
import argparse
import logging

import signal

# pylint: disable=unused-import
try:
    import readline
except ImportError:
    import gnureadline as readline

# pylint: enable=unused-import
import sys
from argparse import RawTextHelpFormatter

from colorlog import ColoredFormatter

from max_ble_hci import BleHci
from max_ble_hci.constants import PhyOption, PayloadOption
from max_ble_hci.data_params import ConnParams, AdvParams, ScanParams


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
    style="%",
)

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


EXIT_FUNC_MAGIC = 999
DEFAULT_BAUD = 115200
DEFAULT_ADV_INTERVAL = 0x60
DEFAULT_SCAN_INTERVAL = 0x100
DEFAULT_CONN_INTERVAL = 0x6  # 7.5 ms
DEFAULT_SUP_TIMEOUT = 0x64  # 1 s


class ArgumentParser(argparse.ArgumentParser):
    """Argument  Parser

    Parameters
    ----------
    argparse : base parser
        Child class adding functionality to basic Argument Parser
    """

    def error(self, message):  # pylint: disable=unused-argument
        logger.error("Invalid input. Refer to 'help' for available commands.'")
        self.exit(2)


def _hex_int(hex_str: str) -> int:
    return int(hex_str, 16)


def _signal_handler(_signal, _fname):  # pylint: disable=unused-argument
    print()
    sys.exit(0)


def _run_input_cmds(commands, terminal):
    for cmd in commands:
        try:
            # pylint: disable=used-before-assignment
            _args = terminal.parse_args(cmd.split())
            _args.func(_args)
        except AttributeError:
            continue
        # Catch SystemExit, allows user to ctrl-c to quit the current command
        except SystemExit as _err:
            if _err.code != 0:
                if _err.code == EXIT_FUNC_MAGIC:
                    sys.exit(0)

                sys.exit(_err.code)
    return True


def main():
    """
    MAIN
    """
    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    command_state = ""

    # Setup the signal handler to catch the ctrl-C
    signal.signal(signal.SIGINT, _signal_handler)

    # Setup the command line description text
    cli_description = f"""
        Bluetooth Low Energy HCI tool.
        This tool is used in tandem with the BLE controller examples. 
        This tool sends HCI commands through the serial port to the target device. 
        It will receive and print the HCI events received from the target device.
        Serial port is configured as 8N1, no flow control, default baud rate of {str(DEFAULT_BAUD)}
        """

    # Parse the command line arguments
    parser = argparse.ArgumentParser(
        description=cli_description, formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    parser.add_argument("serial_port", help="Serial port path or COM#")
    parser.add_argument(
        "-b",
        "--baud",
        dest="baudRate",
        type=int,
        default=DEFAULT_BAUD,
        help="Serial port baud rate. Default: " + str(DEFAULT_BAUD),
    )
    parser.add_argument(
        "-m",
        "--monitor-trace-port",
        dest="monPort",
        default=None,
        help="Monitor Trace Msg Serial Port path or COM#. Default: None",
    )
    parser.add_argument(
        "-i",
        "--id-tag",
        dest="idtag",
        default="DUT",
        help="Board ID tag for printing trace messages. Default: None",
    )
    parser.add_argument(
        "-c",
        "--commands",
        dest="commands",
        nargs="*",
        default=None,
        help="""Commands to run on startup.
        If more than 1, separate commands with a semicolon (;).""",
    )

    parser.add_argument(
        "-t",
        "--trace_level",
        dest="trace_level",
        type=int,
        default=3,
        help="""Set the trace level
        0: Error only
        1: Warning/Error
        2: Info/Warning/Error
        3: All messages
        Default: 3""",
    )

    args = parser.parse_args()

    hci = BleHci(
        args.serial_port,
        baud=args.baudRate,
        id_tag=args.idtag,
        async_callback=print,
        evt_callback=print,
    )
    hci.logger.setLevel(args.trace_level)

    print("Bluetooth Low Energy HCI tool")
    print(f"Serial port: {args.serial_port}")
    print(f"Monitor Trace Msg Serial Port: {args.monPort}")
    print(f"8N1 {args.baudRate}")

    commands = args.commands
    if commands:
        if len(commands) > 1:
            commands = " ".join(commands)
        else:
            commands = commands[0]

        commands = commands.split(";")
        commands = [x.strip() for x in commands]

        print("Startup commands: ")
        for command in commands:
            print(f"\t{command}")

    # Start the terminal argparse
    terminal = ArgumentParser(prog="", add_help=True)
    subparsers = terminal.add_subparsers()

    clear_parser = subparsers.add_parser(
        "clear",
        aliases=["cls"],
        help="Clear the scrren",
        formatter_class=RawTextHelpFormatter,
    )

    clear_parser.set_defaults(
        func=lambda _: os.system("cls" if os.name == "nt" else "clear")
    )

    #### ADDR PARSER ####
    addr_parser = subparsers.add_parser(
        "addr", help="Set the device address.", formatter_class=RawTextHelpFormatter
    )
    addr_parser.add_argument("addr", help="Device address, ex: 00:11:22:33:44:55")
    addr_parser.set_defaults(
        func=lambda args: print(hci.set_address(int(args.addr.replace(":", ""), 16))),
        which="addr",
    )

    memstats_parser = subparsers.add_parser(
        "memstats",
        help="Get BLE stack memory usage statistics",
        formatter_class=RawTextHelpFormatter,
    )

    memstats_parser.set_defaults(func=lambda _: print(hci.get_memory_stats()))

    #### ADV PARSER ####
    adv_parser = subparsers.add_parser(
        "adv",
        help="Send the advertising commands",
        formatter_class=RawTextHelpFormatter,
    )
    adv_parser.add_argument(
        "-i",
        "--interval",
        dest="adv_interval",
        type=_hex_int,
        default=DEFAULT_ADV_INTERVAL,
        help=f"""Advertising interval in units of 0.625 ms, 16-bit hex number 0x0020 - 0x4000.
        Default: 0x{DEFAULT_ADV_INTERVAL}""",
    )
    adv_parser.add_argument(
        "--no-connect",
        dest="connect",
        action="store_false",
        help="Disable advertising as a connectable device.",
    )
    adv_parser.set_defaults(
        func=lambda args: print(
            hci.start_advertising(
                connect=args.connect,
                adv_params=AdvParams(
                    interval_min=args.adv_interval,
                    interval_max=args.adv_interval,
                ),
            ),
        ),
        which="adv",
    )

    #### SCAN PARSER ####
    scan_parser = subparsers.add_parser(
        "scan",
        help="Send scanning commands and print scan reports, ctrl-c to exit.",
        formatter_class=RawTextHelpFormatter,
    )
    scan_parser.add_argument(
        "-i",
        "--interval",
        dest="scan_interval",
        type=_hex_int,
        default=DEFAULT_SCAN_INTERVAL,
        help=f"""Scanning interval in units of 0.625 ms, 16-bit hex number 0x0020 - 0x4000.
        Default: 0x{DEFAULT_SCAN_INTERVAL}""",
    )
    scan_parser.set_defaults(
        func=lambda args: print(
            hci.set_scan_params(
                scan_params=ScanParams(scan_interval=args.scan_interval)
            )
        )
        or hci.enable_scanning(enable=True),
        which="scan",
    )

    #### INIT PARSER ####
    init_parser = subparsers.add_parser(
        "init",
        help="Send the initiating commands to open a connection",
        formatter_class=RawTextHelpFormatter,
    )
    init_parser.add_argument(
        "addr", help="Address of peer to connect with, ex: 00:11:22:33:44:55"
    )
    init_parser.add_argument(
        "-i",
        "--interval",
        dest="conn_interval",
        type=_hex_int,
        default=DEFAULT_CONN_INTERVAL,
        help=f"""Connection interval in units of 1.25ms, 16-bit hex number 0x0006 - 0x0C80."
        Default: {hex(DEFAULT_CONN_INTERVAL)}""",
    )
    init_parser.add_argument(
        "-t",
        "--timeout",
        dest="sup_timeout",
        type=_hex_int,
        default=DEFAULT_SUP_TIMEOUT,
        help=f"""Supervision timeout in units of 10ms, 16-bit hex number 0x000A - 0x0C80.
        "Default: {hex(DEFAULT_SUP_TIMEOUT)}""",
    )
    init_parser.set_defaults(
        func=lambda args: print(
            hci.init_connection(
                args.addr,
                interval=args.conn_interval,
                sup_timeout=args.sup_timeout,
                conn_params=ConnParams(peer_addr=args.addr),
            )
        )
    )

    datalen_parser = subparsers.add_parser(
        "data-len", help="Set the max data length", formatter_class=RawTextHelpFormatter
    )
    datalen_parser.set_defaults(func=lambda _: hci.set_data_len(), which="dataLen")

    send_acl_parser = subparsers.add_parser(
        "send-acl",
        help="Send ACL packets",
        formatter_class=RawTextHelpFormatter,
    )
    send_acl_parser.add_argument(
        "packet_length",
        type=int,
        help="Number of bytes per ACL packet, 16-bit decimal 1-65535, 0 to disable.",
    )
    send_acl_parser.add_argument(
        "num_packets",
        type=int,
        help="Number of packets to send, 8-bit decimal 1-255, 0 to enable auto-generate",
    )
    send_acl_parser.add_argument(
        "--handle",
        type=int,
        default=0,
        help="Number of bytes per ACL packet, 16-bit decimal 1-65535, 0 to disable.",
    )
    send_acl_parser.set_defaults(
        func=lambda args: print(
            hci.generate_acl(args.handle, args.packet_len, args.num_packets)
        ),
    )

    sinl_acl_parser = subparsers.add_parser(
        "sink-acl",
        help="Sink ACL packets, do not send events to host",
        formatter_class=RawTextHelpFormatter,
    )
    sinl_acl_parser.add_argument("-e", "--enable", default=1)
    sinl_acl_parser.set_defaults(
        func=lambda _: print(hci.enable_acl_sink(bool(args.enable))),
    )

    conn_stats_parser = subparsers.add_parser(
        "conn-stats",
        aliases=["cs"],
        help="Get the connection stats",
        formatter_class=RawTextHelpFormatter,
    )

    conn_stats_parser.set_defaults(
        func=lambda _: print(hci.get_conn_stats()), which="connstats"
    )

    test_stats_parser = subparsers.add_parser(
        "test-stats",
        aliases=["ts"],
        help="Get the test stats",
        formatter_class=RawTextHelpFormatter,
    )

    test_stats_parser.set_defaults(func=lambda _: print(hci.get_test_stats()))

    phy_enable = subparsers.add_parser(
        "bben",
        help="Enable the Baseband Radio (Required for RSSI capture)",
        formatter_class=RawTextHelpFormatter,
    )
    phy_enable.set_defaults(func=lambda args: print(hci.bb_enable()))

    phy_disable = subparsers.add_parser(
        "bbdis",
        help="Disable the Baseband Radio",
        formatter_class=RawTextHelpFormatter,
    )
    phy_disable.set_defaults(func=lambda args: print(hci.bb_disable()))

    rssi_parser = subparsers.add_parser(
        "rssi",
        help="Get an RSSI sample using CCA",
        formatter_class=RawTextHelpFormatter,
    )
    rssi_parser.add_argument("-c", "--channel", default=0)

    def _print_rssi(_args):
        rssi, status = hci.get_rssi_vs(_args.channel)
        print(f"RSSI (dBm): {rssi}")
        print(status)

    rssi_parser.set_defaults(func=_print_rssi)

    #### RESET PARSER ####
    reset_parser = subparsers.add_parser("reset", help="Sends an HCI reset command")
    reset_parser.set_defaults(func=lambda _: print(hci.reset()), which="reset")

    #### TX TEST PARSER ####
    tx_test_parser = subparsers.add_parser(
        "tx-test",
        aliases=["tx"],
        help="Execute the transmitter test.",
        formatter_class=RawTextHelpFormatter,
    )
    tx_test_parser.add_argument(
        "-c",
        "--channel",
        type=int,
        dest="channel",
        default=0,
        help="TX test channel, 0-39. Default: 0",
    )
    tx_test_parser.add_argument(
        "--phy",
        dest="phy",
        type=int,
        default=1,
        help="""Tx Test PHY
        1: 1M
        2: 2M
        3: S8
        4: S2
        Default: 1M""",
    )
    tx_test_parser.add_argument(
        "-p",
        "--payload",
        dest="payload",
        type=int,
        default=0,
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
    tx_test_parser.add_argument(
        "-pl",
        "--packet-length",
        type=int,
        default=0,
        help="Tx packet length, number of bytes per packet, 0-255. Default: 0",
    )

    tx_test_parser.set_defaults(
        func=lambda args: print(
            hci.tx_test(
                channel=args.channel,
                phy=PhyOption(args.phy),
                payload=PayloadOption(args.payload),
                packet_len=args.packet_length,
            )
        ),
    )

    tx_test_vs_parser = subparsers.add_parser(
        "txtestvs",
        aliases=["txvs"],
        help="Execute the vendor-specific transmitter test",
        formatter_class=RawTextHelpFormatter,
    )
    tx_test_vs_parser.add_argument(
        "-c",
        "--channel",
        type=int,
        dest="channel",
        default=0,
        help="Tx test channel. Default: 0",
    )
    tx_test_vs_parser.add_argument(
        "--phy",
        dest="phy",
        type=int,
        default=1,
        help="""Tx Test PHY
        1: 1M
        2: 2M
        3: S8
        4:S2
        Default: 1M""",
    )
    tx_test_vs_parser.add_argument(
        "-p",
        "--payload",
        dest="payload",
        type=int,
        default=0,
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
    tx_test_vs_parser.add_argument(
        "-pl",
        "--packet-length",
        dest="packet_length",
        type=int,
        default=0,
        help="Tx packet length, number of bytes per packet, 0-255. Default: 0",
    )
    tx_test_vs_parser.add_argument(
        "-n",
        "--num-packets",
        dest="num_packets",
        type=int,
        default=0,
        help="Number of packets to transmit, 2 bytes hex, 0 equals infinite. Default: 0",
    )
    tx_test_vs_parser.set_defaults(
        func=lambda args: print(
            hci.tx_test_vs(
                channel=args.channel,
                phy=args.phy,
                payload=args.payload,
                packet_len=args.packet_length,
                num_packets=args.num_packets,
            )
        )
    )

    #### RXTEST PARSER ####
    rx_test_parser = subparsers.add_parser(
        "rx-test",
        aliases=["rx"],
        help="Execute the receiver test",
        formatter_class=RawTextHelpFormatter,
    )
    rx_test_parser.add_argument(
        "-c",
        "--channel",
        dest="channel",
        type=int,
        default=0,
        help="Rx test channel, 0-39. Default: 0",
    )
    rx_test_parser.add_argument(
        "--phy",
        dest="phy",
        type=int,
        default=1,
        help="""Rx Test PHY
        1: 1M
        2: 2M
        3: S8
        4: S2
        Default: 1""",
    )
    rx_test_parser.set_defaults(
        func=lambda args: print(
            hci.rx_test(channel=args.channel, phy=PhyOption(args.phy))
        )
    )

    #### RXTESTVS PARSER ####
    rx_test_vs_parser = subparsers.add_parser(
        "rx-test-vs",
        aliases=["rxvs"],
        help="Execute the vendor-specific receiver test",
        formatter_class=RawTextHelpFormatter,
    )
    rx_test_vs_parser.add_argument(
        "-c",
        "--channel",
        dest="channel",
        type=int,
        default=0,
        help="Rx test channel. Default: 0",
    )
    rx_test_vs_parser.add_argument(
        "--phy",
        dest="phy",
        type=int,
        default=1,
        help="""Rx Test PHY
        1: 1M
        2: 2M
        3: S8
        4: S2
        Default: 1""",
    )
    rx_test_vs_parser.add_argument(
        "-m",
        "--mod-idx",
        dest="modulationIdx",
        type=int,
        default=0,
        help="Vendor-specific modulation index",
    )
    rx_test_vs_parser.add_argument(
        "-n",
        "--num_packets",
        dest="num_packets",
        type=int,
        default=0,
        help="Number of packets to transmit, 2 bytes hex, 0 equals infinite. Default: 0",
    )
    rx_test_vs_parser.set_defaults(
        func=lambda args: print(
            hci.rx_test_vs(
                channel=args.channel,
                phy=PhyOption(args.phy),
                modulation_idx=args.modulationIdx,
                num_packets=args.num_packets,
            )
        ),
    )

    #### ENDTEST PARSER ####
    endtest_parser = subparsers.add_parser(
        "end-test",
        aliases=["end"],
        help="End the Tx/Rx test, print the number of correctly received packets",
        formatter_class=RawTextHelpFormatter,
    )

    def _end_test(_args):
        rx_packets, status = hci.end_test()
        print(f"RX Received: {rx_packets}")
        print(status)

    endtest_parser.set_defaults(func=_end_test)

    #### RESET TEST STATS PARSER ####
    reset_test_stats_parser = subparsers.add_parser(
        "reset-ts",
        aliases=["rsts"],
        help="Reset accumulated stats from DTM",
        formatter_class=RawTextHelpFormatter,
    )
    reset_test_stats_parser.set_defaults(
        func=lambda _: print(hci.reset_test_stats()), which="reset-test-stats"
    )

    #### TXPOWER PARSER ####
    txpower_parser = subparsers.add_parser(
        "tx-power",
        aliases=["txp"],
        help="Set the Tx power",
        formatter_class=RawTextHelpFormatter,
    )
    txpower_parser.add_argument(
        "power", type=int, help="Integer power setting in units of dBm."
    )

    txpower_parser.set_defaults(
        func=lambda args: print(hci.set_adv_tx_power(args.power)),
    )

    discon_parser = subparsers.add_parser(
        "discon",
        aliases=["dc"],
        help="Send the command to disconnect",
        formatter_class=RawTextHelpFormatter,
    )

    discon_parser.set_defaults(func=lambda _: print(hci.disconnect()), which="discon")

    set_ch_map_parser = subparsers.add_parser(
        "set-chmap",
        help="Set the connection channel map to a given channel.",
        formatter_class=RawTextHelpFormatter,
    )
    set_ch_map_parser.add_argument(
        "channel",
        type=int,
        nargs="?",
        help="""Channel to use in channel map
        Will set the channel map to the given channel plus one additional channel.""",
    )
    set_ch_map_parser.add_argument(
        "-m",
        "--mask",
        dest="mask",
        type=_hex_int,
        help=""""4-byte hex number to use a channel map.
        0xFFFFFFFFFF uses all channels, 0x000000000F will use channels 0-3, etc""",
    )
    set_ch_map_parser.add_argument(
        "--handle",
        dest="handle",
        type=int,
        default=0,
        help="Connection handle, integer. Default: 0",
    )
    set_ch_map_parser.set_defaults(
        func=lambda args: hci.set_channel_map(channels=args.mask, handle=args.handle),
    )

    cmd_parser = subparsers.add_parser(
        "cmd", help="Send raw HCI command", formatter_class=RawTextHelpFormatter
    )
    cmd_parser.add_argument(
        "cmd",
        help='String of hex bytes LSB first\nex: "01030C00" to send HCI Reset command',
    )
    cmd_parser.add_argument(
        "-t",
        "--timeout",
        dest="timeout",
        type=int,
        help="Command timeout, Default: None",
    )

    cmd_parser.set_defaults(
        func=lambda args: print(hci.write_command_raw(bytes.fromhex(args.command)))
    )

    #### EXIT PARSER ####
    exit_parser = subparsers.add_parser(
        "exit",
        aliases=["quit", "q"],
        help="Exit the program",
        formatter_class=RawTextHelpFormatter,
    )
    exit_parser.set_defaults(func=lambda _: sys.exit(EXIT_FUNC_MAGIC), which="exit")

    #### HELP PARSER ####
    help_parser = subparsers.add_parser("help", aliases=["h"], help="Show help message")
    help_parser.set_defaults(func=lambda _: terminal.print_help(), which="help")

    def _completer(text, state):
        commands = subparsers.choices.keys()
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        return matches[state] if state < len(matches) else None

    readline.set_completer(_completer)
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(readline.get_completer_delims().replace("-", ""))

    command_run = False
    if commands:
        command_run = _run_input_cmds(commands, terminal)

    while True:
        if commands and not command_run:
            logger.info("Port set, running input commands.")
            command_run = _run_input_cmds(commands, terminal)

        astr = input(f"{command_state}>>> ")
        try:
            args = terminal.parse_args(astr.split())
            try:
                args.func(args)
            except AttributeError as err:
                logger.error(str(err))
                continue

        except SystemExit as err:
            if err.code == EXIT_FUNC_MAGIC:
                sys.exit(0)
            elif err.code != 0:
                logger.error(
                    "Process finished with exit code %s (%s)", err, type(err).__name__
                )

        except Exception as err:  # pylint: disable=broad-exception-caught
            logger.error("Unexpected exception %s", type(err).__name__)


################## MAIN ##################
if __name__ == "__main__":
    main()
