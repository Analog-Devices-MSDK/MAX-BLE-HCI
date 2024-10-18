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
import argparse
import logging
import os
import signal
import secrets

# pylint: disable=unused-import,too-many-lines
try:
    import readline
except ImportError:
    import gnureadline as readline

# pylint: enable=unused-import
import sys
from argparse import RawTextHelpFormatter

# pylint: disable=import-error
from colorlog import ColoredFormatter

from max_ble_hci import BleHci
from max_ble_hci.constants import PayloadOption, PhyOption, AddrType
from max_ble_hci.data_params import (
    AdvParams,
    EstablishConnParams,
    ScanParams,
    ConnParams,
)
from max_ble_hci.utils import address_str2int
from max_ble_hci.packet_codes import EventMaskLE, StatusCode, EventCode, EventSubcode
from max_ble_hci.hci_packets import EventPacket
from max_ble_hci.ad_types import AdvReport
from max_ble_hci import utils


# pylint: enable=import-error


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
DEFAULT_SCAN_INTERVAL = 0x10
DEFAULT_CONN_INTERVAL = 0x6  # 7.5 ms
DEFAULT_SUP_TIMEOUT = 0x64  # 1 s
DEFAULT_CE_LEN = 0x0F10
DEFAULT_CONN_LATENCY = 0


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
            print(cmd)
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


def _init_cli():
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

    parser.add_argument("--version", action="version", version="%(prog)s 1.4.0")

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
        "-efc",
        "--enable-flow-control",
        action="store_true",
        default=False,
        help="Enable flow control Default: False",
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
        "--startup-script",
        help="""Filepath to to run startup commands.
        Commands should be newline seperated""",
    )

    parser.add_argument(
        "-t",
        "--trace_level",
        dest="trace_level",
        type=int,
        default=2,
        choices=(0, 1, 2, 3),
        help="""Set the trace level
        0: Error only
        1: Warning/Error
        2: Info/Warning/Error
        3: All messages
        Default: 2""",
    )

    return parser.parse_args()


def main():
    # pylint: disable=too-many-statements, too-many-branches, too-many-locals
    """
    MAIN
    """

    args = _init_cli()

    hci = BleHci(
        args.serial_port,
        baud=args.baudRate,
        id_tag=args.idtag,
        async_callback=print,
        evt_callback=print,
        flowcontrol=args.enable_flow_control,
        recover_on_power_loss=True,
    )

    trace_lut = {
        0: "ERROR",
        1: "WARNING",
        2: "INFO",
        3: "DEBUG",
    }
    trace_level = trace_lut[args.trace_level]
    hci.logger.setLevel(trace_level)

    print("Bluetooth Low Energy HCI tool")
    print(f"Serial port: {args.serial_port}")
    print(f"8N1 {args.baudRate}")

    commands = args.commands
    if args.startup_script:
        if commands:
            raise NotImplementedError(
                "Cannot decide on which order to run startup and commands"
            )

        with open(args.startup_script, "r", encoding="utf-8") as startup:
            commands = startup.readlines()
            commands = [command.strip() for command in commands]

        print(commands)

    elif commands:
        if len(commands) > 1:
            commands = " ".join(commands)
        else:
            commands = commands[0]

        commands = commands.split(";")
        commands = [x.strip() for x in commands]
        print(commands)
        print("Startup commands: ")
        for command in commands:
            print(f"\t{command}")

    # Start the terminal argparse
    terminal = ArgumentParser(prog="", add_help=True)
    subparsers = terminal.add_subparsers()

    log_level_parser = subparsers.add_parser(
        "loglevel",
        aliases=["ll"],
    )

    log_level_parser.add_argument(
        "loglevel",
        type=int,
        nargs="?",
        choices=(0, 1, 2, 3),
        help="""Set the log level
        0: Error only
        1: Warning/Error
        2: Info/Warning/Error
        3: All messages
        Default: 2""",
    )

    def _set_log_level(level):
        if level is None:
            print(f"Current Log level {hci.get_log_level()}")
            return

        trace_level = level
        hci.set_log_level(trace_lut[trace_level])

    log_level_parser.set_defaults(func=lambda args: _set_log_level(args.loglevel))

    clear_parser = subparsers.add_parser(
        "clear",
        aliases=["cls"],
        help="Clear the screen",
        formatter_class=RawTextHelpFormatter,
    )

    clear_parser.set_defaults(
        func=lambda _: os.system("cls" if os.name == "nt" else "clear")
    )
    #### UPDATE PARSER ####
    update_parser = subparsers.add_parser(
        "update", help="update the firmware", formatter_class=RawTextHelpFormatter
    )
    update_parser.add_argument("addr", help="start address of memory bank to upload")
    update_parser.add_argument("update", help="name of application file")
    update_parser.set_defaults(
        func=lambda args: print(hci.firmware_update(args.addr, args.update)),
        which="update",
    )

    #### RESET PARSER ####
    reset_parser = subparsers.add_parser(
        "sysreset", help="reset the device", formatter_class=RawTextHelpFormatter
    )

    reset_parser.set_defaults(
        func=lambda args: print(hci.reset_device()),
        which="sysreset",
    )

    #### ERASE PARSER ####
    erase_parser = subparsers.add_parser(
        "erase",
        help="erase one page of the flash",
        formatter_class=RawTextHelpFormatter,
    )

    erase_parser.add_argument("addr", help="start address of memory bank to be erased")

    erase_parser.set_defaults(
        func=lambda args: print(hci.erase_page(args.addr)),
        which="erase",
    )

    #### ADDR PARSER ####
    addr_parser = subparsers.add_parser(
        "addr", help="Set the device address.", formatter_class=RawTextHelpFormatter
    )
    addr_parser.add_argument("addr", help="Device address, ex: 00:11:22:33:44:55")
    addr_parser.set_defaults(
        func=lambda args: print(hci.set_address(args.addr)),
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
        help="Start advertising",
        formatter_class=RawTextHelpFormatter,
    )
    adv_parser.add_argument(
        "enable",
        nargs="?",
        choices=("1", "0", "enable", "start", "en", "disable", "dis", "stop"),
        help="""Enable or disable advertising
        Default: enable""",
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
        "-n", "--name", type=str, default="", help="Advertising name"
    )
    adv_parser.add_argument(
        "-a",
        "--addr-type",
        type=int,
        choices=[0, 1, 2, 3],
        default=0,
        help="""Set address type.
        0: Public
        1: Random
        2: Public Identity
        3: Random Identitiy
        Default: Public""",
    )
    adv_parser.add_argument(
        "--no-connect",
        dest="connect",
        action="store_false",
        help="Disable advertising as a connectable device.",
    )
    adv_parser.add_argument(
        "--filter",
        action="store_const",
        const=3,
        default=0,
        help="Filter devices using the whitelist.",
    )

    def _adv_func(args):
        enable: str = args.enable
        addr_type: AddrType = AddrType(args.addr_type)
        if not enable:
            enable = "1"

        if enable in ("1", "en", "enable", "start"):
            if addr_type == AddrType.RANDOM:
                rand_addr = secrets.randbits(48)
                logger.info(
                    "Advertising with random adrress %s",
                    utils.address_int2str(rand_addr),
                )
                hci.set_random_address(rand_addr)

            logger.info("Enabling advertising")
            adv_params = AdvParams(
                adv_type=0 if args.connect else 0x3,
                interval_min=args.adv_interval,
                interval_max=args.adv_interval,
                filter_policy=args.filter,
            )
            hci.start_advertising(
                connect=args.connect, adv_params=adv_params, adv_name=args.name
            )
        elif enable in ("0", "dis", "disable", "stop"):
            logger.info("Disabling advertising")
            print(hci.enable_adv(False))

        else:
            assert False, "All options should be covered"

    adv_parser.set_defaults(func=_adv_func)

    #### SCAN PARSER ####
    scan_parser = subparsers.add_parser(
        "scan",
        help="Start scanning.",
        formatter_class=RawTextHelpFormatter,
    )
    scan_parser.add_argument(
        "enable",
        nargs="?",
        choices=("1", "0", "enable", "en", "start", "disable", "dis", "stop"),
        help="""Enable or disable scanning
        Default: enable""",
    )

    scan_parser.add_argument(
        "-i",
        "--interval",
        dest="scan_interval",
        type=_hex_int,
        default=DEFAULT_SCAN_INTERVAL,
        help=f"""Scanning interval in units of 0.625 ms, 16-bit hex number 0x0004 - 0x4000.
        Default: 0x{DEFAULT_SCAN_INTERVAL}""",
    )

    scan_parser.add_argument(
        "--no-log",
        action="store_true",
        help="Disable logging outut of events from advertising reports",
    )

    scan_parser.add_argument(
        "--show-only",
        action="append",
        nargs="?",
        default=[],
        help="Disable logging outut of events from advertising reports",
    )

    def _scan_func(args):
        def _scan_event_callback(packet: EventPacket):
            if (
                packet.evt_code != EventCode.LE_META
                and packet.evt_subcode != EventSubcode.ADVERTISING_REPORT
            ):
                return

            reports = AdvReport.from_bytes(packet.evt_params)

            for report in reports:
                if report.address in args.show_only or args.show_only == []:
                    print(report.address, report.rssi)

        enable = args.enable
        if not enable:
            enable = "1"

        if enable in ("1", "en", "enable", "start"):
            logger.info("Enabling scanning")

            status = hci.set_scan_params(
                scan_params=ScanParams(scan_interval=args.scan_interval)
            )
            if status != StatusCode.SUCCESS:
                logger.error("Failed to set scan params!")
                return

            if args.no_log:
                hci.set_event_callback(None)
            else:
                hci.set_event_callback(_scan_event_callback)
                hci.set_event_mask_le(
                    EventMaskLE.ADV_REPORT
                    | EventMaskLE.PERIODIC_ADV_REPORT
                    | EventMaskLE.EXTENDED_ADV_REPORT
                )

            print(hci.enable_scanning(True))
            hci.set_log_level(logging.ERROR)

        elif enable in ("0", "dis", "disable", "stop"):
            hci.set_log_level("INFO")
            logger.info("Disabling scanning")
            print(hci.enable_scanning(False))
            hci.disable_all_events()
        else:
            logger.error("Could not match command to enable or disable")
            return

    scan_parser.set_defaults(func=_scan_func)

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
                addr=address_str2int(args.addr[::-1]),
                sup_timeout=args.sup_timeout,
                conn_params=EstablishConnParams(
                    peer_addr=address_str2int(args.addr),
                    conn_interval_min=args.conn_interval,
                    conn_interval_max=args.conn_interval,
                ),
            )
        )
    )
    conn_update = subparsers.add_parser(
        "conn-update",
        help="Start advertising",
        formatter_class=RawTextHelpFormatter,
    )
    conn_update.add_argument(
        "handle",
        nargs="?",
        default=0,
        type=int,
        help="""Connection handle""",
    )
    conn_update.add_argument(
        "-i",
        "--interval",
        type=_hex_int,
        default=DEFAULT_CONN_INTERVAL,
        help=f"""Connection interval in units of 1.25ms, 16-bit hex number 0x0006 - 0x0C80."
Default: {hex(DEFAULT_CONN_INTERVAL)}""",
    )
    conn_update.add_argument(
        "-l",
        "--latency",
        type=_hex_int,
        default=DEFAULT_CONN_LATENCY,
        help=f"""The Conn_Latency parameter shall define the maximum allowed connection latency
Default: {hex(DEFAULT_CONN_LATENCY)}""",
    )
    conn_update.add_argument(
        "-t",
        "--timeout",
        dest="sup_timeout",
        type=_hex_int,
        default=DEFAULT_SUP_TIMEOUT,
        help=f"""Supervision timeout in units of 10ms, 16-bit hex number 0x000A - 0x0C80.
Default: {hex(DEFAULT_SUP_TIMEOUT)}""",
    )

    conn_update.add_argument(
        "-c",
        "--ce_len",
        default=DEFAULT_CE_LEN,
        type=_hex_int,
        help=f"""The Minimum_CE_Length and Maximum_CE_Length are information
parameters providing the Controller with a hint about the expected minimum
and maximum length of the connection events. The Minimum_CE_Length shall
be less than or equal to the Maximum_CE_Length.
Default: {hex(DEFAULT_CE_LEN)}""",
    )

    def _conn_update_callback(packet: EventPacket):
        if packet.evt_subcode == EventSubcode.CONNECTION_UPDATE:
            logger.info("Connection update complete!")

        hci.set_event_callback(print)
        print(">>>>")

    conn_update.set_defaults(
        func=lambda args: print(
            hci.update_connection_params(
                args.handle,
                ConnParams(
                    conn_interval_max=args.interval,
                    conn_interval_min=args.interval,
                    max_latency=args.latency,
                    sup_timeout=args.supervision_timeout,
                    min_ce_length=args.ce_len,
                    max_ce_length=args.ce_len,
                ),
                callback=_conn_update_callback,
            ),
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
        "packet_len",
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

    def auto_acl(args):
        if args.num_packets == 0:
            print(hci.enable_autogenerate_acl(args.packet_len))
        print(hci.generate_acl(args.handle, args.packet_len, args.num_packets))

    send_acl_parser.set_defaults(func=auto_acl)

    sinl_acl_parser = subparsers.add_parser(
        "sink-acl",
        help="Sink ACL packets, do not send events to host",
        formatter_class=RawTextHelpFormatter,
    )
    sinl_acl_parser.add_argument("-e", "--enable", default=1)
    sinl_acl_parser.set_defaults(
        func=lambda _: print(hci.enable_acl_sink(bool(args.enable))),
    )
    adv_stats_parser = subparsers.add_parser(
        "adv-stats",
        aliases=["as"],
        help="Get the advertising stats",
        formatter_class=RawTextHelpFormatter,
    )

    adv_stats_parser.set_defaults(func=lambda _: print(hci.get_adv_stats()))

    scan_stats_parser = subparsers.add_parser(
        "scan-stats",
        aliases=["ss"],
        help="Get the scan stats",
        formatter_class=RawTextHelpFormatter,
    )

    scan_stats_parser.set_defaults(func=lambda _: print(hci.get_scan_stats()))

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

    #### RESET CONNECTION STATS PARSER ####
    reset_connection_stats_parser = subparsers.add_parser(
        "reset-cs",
        aliases=["rscs"],
        help="Reset accumulated stats from connection mode",
        formatter_class=RawTextHelpFormatter,
    )
    reset_connection_stats_parser.set_defaults(
        func=lambda _: print(hci.reset_connection_stats()),
        which="reset-connection-stats",
    )
    #### RESET Adv STATS PARSER ####
    reset_adv_stats_parser = subparsers.add_parser(
        "reset-adv-stats",
        aliases=["rsas"],
        help="Reset accumulated stats from connection mode",
        formatter_class=RawTextHelpFormatter,
    )
    reset_adv_stats_parser.set_defaults(
        func=lambda _: print(hci.reset_adv_stats()),
    )

    reset_scan_stats_parser = subparsers.add_parser(
        "reset-scan-stats",
        aliases=["rsss"],
        help="Reset accumulated stats from connection mode",
        formatter_class=RawTextHelpFormatter,
    )
    reset_scan_stats_parser.set_defaults(
        func=lambda _: print(hci.reset_scan_stats()),
    )

    #### SET PHY PARSER ####
    set_phy_parser = subparsers.add_parser(
        "set-phy",
        aliases=["sp"],
        help="Set the PHY.",
        formatter_class=RawTextHelpFormatter,
    )
    set_phy_parser.add_argument(
        "-c",
        "--conn-handle",
        type=int,
        dest="handle",
        default=0,
        help="Connection handle. Default: 0",
    )
    set_phy_parser.add_argument(
        "-p",
        "--phy",
        dest="phy",
        type=int,
        default=1,
        help="""Desired PHY
        1: 1M
        2: 2M
        3: S2
        4: S8
        Default: 1M""",
    )
    phy_lut = {
        1: PhyOption.PHY_1M,
        2: PhyOption.PHY_2M,
        3: PhyOption.PHY_CODED_S2,
        4: PhyOption.PHY_CODED_S8,
    }
    set_phy_parser.set_defaults(
        func=lambda _: print(
            hci.set_phy(
                handle=args.handle, tx_phys=phy_lut[args.phy], rx_phys=phy_lut[args.phy]
            )
        ),
        which="set-phy",
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

    def _whitelist_func(args):
        method = args.method
        if method == "size":
            wl_size = hci.read_whitelist_size()
            print(f"Whitelist size: {wl_size}")
            return

        if method == "clear":
            print(hci.clear_whitelist())
            return

        if len(args.args) != 2:
            raise ValueError(
                f"Incorrect number of arguments. Expected 2 got {len(args.args)}"
            )

        addr_type = int(args.args[0])
        address = args.args[1]

        if method == "add":
            print(hci.add_device_to_whitelist(addr_type=addr_type, address=address))
        else:
            print(
                hci.remove_device_from_whitelist(addr_type=addr_type, address=address)
            )

    whitelist_parser = subparsers.add_parser(
        "filter",
        aliases=["filt", "wl", "whitelist"],
        help="Add, remove devices from whitelist as well as clear",
    )
    whitelist_parser.add_argument(
        "method",
        nargs="?",
        default="size",
        type=str,
        choices=("add", "remove", "clear", "size"),
    )
    wl_args_help = """Additional whitelist parameters depending on method.
    add and remove require positional arguments <Address Type> <address>
    adress: 6 bytes device address (Ex: xx:xx:xx:xx:xx:xx)
    AddressType:
    \tPublic Device Address 0
    \tRandom Device Address 1
    \tPublic ID Address 2 
    \tRandom ID Address 3
    """
    whitelist_parser.add_argument("args", nargs="*", type=str, help=wl_args_help)
    whitelist_parser.set_defaults(func=_whitelist_func)

    #### ENABLE ENCRYPTION PARSER ####
    enable_enc_parser = subparsers.add_parser(
        "ena-enc",
        help="LE Enable Encryption Command",
    )
    enable_enc_parser.add_argument(
        "handle",
        type=int,
        help="Connection handle.",
    )
    enable_enc_parser.add_argument(
        "random",
        type=_hex_int,
        help="Random Number.",
    )
    enable_enc_parser.add_argument(
        "ediv",
        type=_hex_int,
        help="Encrypted Diversifier.",
    )
    enable_enc_parser.add_argument(
        "ltk",
        type=_hex_int,
        help="Long Term Key.",
    )
    enable_enc_parser.set_defaults(
        func=lambda args: hci.enable_encryption(
            handle=args.handle, random=args.random, ediv=args.ediv, ltk=args.ltk
        ),
    )

    #### LTK REPLY PARSER ####
    ltk_reply_parser = subparsers.add_parser(
        "ltk-reply",
        help="LE LTK Reply Command",
    )
    ltk_reply_parser.add_argument(
        "handle",
        type=int,
        help="Connection handle.",
    )
    ltk_reply_parser.add_argument(
        "ltk",
        type=_hex_int,
        help="Long Term Key.",
    )
    ltk_reply_parser.set_defaults(
        func=lambda args: hci.ltk_reply(handle=args.handle, ltk=args.ltk),
    )

    #### ENABLE EVENT PARSER ####
    ena_evt_mask_parser = subparsers.add_parser(
        "ena-evt",
        aliases=["evt"],
        help="Enable all event masks.",
        formatter_class=RawTextHelpFormatter,
    )
    ena_evt_mask_parser.set_defaults(
        func=lambda args: hci.enable_all_events(),
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

    ls_parser = subparsers.add_parser(
        "ls",
        help="List directory",
        formatter_class=RawTextHelpFormatter,
    )

    ls_parser.add_argument("ls_dir", nargs="?", default=".")
    ls_parser.set_defaults(
        func=lambda args: [print(x) for x in os.listdir(args.ls_dir)]
    )
    cd_parser = subparsers.add_parser(
        "cd",
        help="change working directory",
        formatter_class=RawTextHelpFormatter,
    )
    cd_parser.add_argument("dir")
    cd_parser.set_defaults(func=lambda args: os.chdir(args.dir))

    pwd_parser = subparsers.add_parser(
        "pwd",
        help="print working directory",
        formatter_class=RawTextHelpFormatter,
    )
    pwd_parser.set_defaults(func=lambda args: print(os.getcwd()))

    # Create the 'make' subparser
    make_parser = subparsers.add_parser(
        "make",
        help="Run make",
        formatter_class=RawTextHelpFormatter,
    )

    make_parser.add_argument(
        "-j",
        "--jobs",
        default="",
    )
    make_parser.add_argument("-C", "--directory", default=".")

    make_parser.set_defaults(
        func=lambda args: os.system(f"make -j {args.jobs} -C {args.directory}")
    )

    def _script_runner(script_path):
        print(script_path)
        with open(script_path, "r", encoding="utf-8") as script:
            commands = script.readlines()

        if commands:
            commands = [command.strip() for command in commands if command != ""]
            _run_input_cmds(commands, terminal)

    run_parser = subparsers.add_parser(
        "shell",
        help="run command via os shell",
        formatter_class=RawTextHelpFormatter,
    )
    run_parser.add_argument("shellargs", nargs="+")
    run_parser.set_defaults(func=lambda args: os.system(" ".join(args.shellargs)))

    flush_parser = subparsers.add_parser("flush", help="Flush serial port")
    flush_parser.set_defaults(func=lambda _: hci.port.flush())

    def _script_runner(script_path):
        print(script_path)
        with open(script_path, "r", encoding="utf-8") as script:
            commands = script.readlines()

        if commands:
            _run_input_cmds(commands, terminal)

    run_parser = subparsers.add_parser(
        "run",
        help="run command via os",
        formatter_class=RawTextHelpFormatter,
    )
    run_parser.add_argument("run")
    run_parser.set_defaults(func=lambda args: _script_runner(args.run))

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

        command_str = input(">>> ")

        # just an empty command
        if command_str in ("", os.linesep):
            continue

        try:
            args = terminal.parse_args(command_str.split())
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
