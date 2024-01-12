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
import signal

# pylint: disable=unused-import
import readline

# pylint: enable=unused-import
import sys
from argparse import RawTextHelpFormatter

from colorlog import ColoredFormatter

from ble_hci import BleHci
from ble_hci.constants import PhyOption, PayloadOption
from ble_hci import packet_codes as pc

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.DEBUG)

# Create a console handler and set the level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a colored formatter
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

# Add the formatter to the console handler
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)


EXIT_FUNC_MAGIC = 999
DEFAULT_BAUD = 115200
DEFAULT_ADV_INTERVAL = 0x60
DEFAULT_SCAN_INTERVAL = 0x100
DEFAULT_CONN_INTERVAL = 0x6  # 7.5 ms
DEFAULT_SUP_TIMEOUT = 0x64  # 1 s

hci = None


class ListenAction(argparse.Action):
    """Listen Action"""

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            setattr(namespace, self.dest, int(values))
        else:
            setattr(namespace, self.dest, True)


class ArgumentParser(argparse.ArgumentParser):
    """Argument  Parser

    Parameters
    ----------
    argparse : base parser
        Child class adding functionality to basic Argument Parser
    """

    def error(self, message):
        logger.error("Invalid input. Refer to 'help' for available commands.'")
        self.exit(2)


def hex_int(hex_str: str) -> int:
    """Convert hex as string to int

    Parameters
    ----------
    hex_str : str
        hex value as string

    Returns
    -------
    int
        hex string converted to int
    """
    return int(hex_str, 16)


def signal_handler(signal, fname):
    # pylint: disable=unused-variable
    print()
    sys.exit(0)


def run_input_cmds(commands):
    for cmd in commands:
        try:
            args = terminal.parse_args(cmd.split())
            args.func(args)
        except AttributeError:
            continue

        # Catch SystemExit, allows user to ctrl-c to quit the current command
        except SystemExit as err:
            if "{0}".format(err) != "0":
                # Catch the magic exit value, return 0
                if "{0}".format(err) == str(EXIT_FUNC_MAGIC):
                    sys.exit(0)

                # Return error
                sys.exit(int("{0}".format(err)))

            # Continue if we get a different code

    return True


def addr_func(args):
    """Set BD Address

    Parameters
    ----------
    args : _type_
        _description_
    """
    addr = int(args.addr.replace(":", ""), 16)
    hci.set_address(addr)


def adv_func(args):
    hci.start_advertising(
        interval=args.adv_interval,
        connect=args.connect,
        listen=args.listen,
        stats=args.stats,
        maintain=args.maintain,
    )


def scan_func(args):
    # TODO: Figure out to replicate this
    hci.start(interval=args.scan_interval)


def init_func(args):
    hci.init_connection(
        args.addr,
        interval=args.conn_interval,
        timeout=args.sup_timeout,
        listen=args.listen,
        stats=args.stats,
        maintain=args.maintain,
    )


def data_len_func(args):
    hci.set_data_len()


def send_acl_func(args):
    hci.sendAcl(args.packet_length, args.num_packets)


def sink_acl_func(args):
    hci.sinkAcl()


def conn_stats_func(args):
    
    print(hci.get_conn_stats())


def phy_func(args):
    hci.set_phy(args.phy)


def reset_func(args):
    hci.reset()


def memstats_func(args):
    # TODO: NO CLUE
    print(hci.get_memory_stats())
    # hci.listen(stats=args.stats, time=args.time)


def tx_test_func(args):
    code = hci.tx_test(
        channel=args.channel,
        phy=PhyOption(args.phy),
        payload=PayloadOption(args.payload),
        packet_len=args.packet_length,
    )


def tx_test_vs_func(args):
    hci.tx_test_vs_(
        channel=args.channel,
        phy=args.phy,
        payload=args.payload,
        packet_length=args.packet_length,
        num_packets=args.num_packets,
    )


def rx_test_func(args):
    hci.rx_test(channel=args.channel, phy=PhyOption(args.phy))


def rx_test_vs_func(args):
    hci.rx_test_vs(
        channel=args.channel,
        phy=PhyOption(args.phy),
        modulation_idx=args.modulationIdx,
        num_packets=args.num_packets,
    )


def end_test_func(args):
    hci.end_test()


def reset_test_stats_func(args):
    hci.reset_test_stats()


def tx_power_func(args):
    hci.set_adv_tx_power(args.power, handle=args.handle)


def discon_func(args):
    hci.disconnect()


def set_ch_map_func(args):
    hci.set_channel_map(channel=args.channel, mask=args.mask, handle=args.handle)


def cmd_func(args):
    # TODO: NO CLUE 2
    hci.command(args.cmd, listen=args.listen)


def read_reg_func(args):
    print(args.addr)
    hci.read_register(args.addr, args.length)


def write_reg_func(args):
    hci.write_register(args.addr, args.value)


def help_func(args):
    terminal.print_help()


def exit_func(args):
    if hci is not None:
        hci.exit()
    sys.exit(EXIT_FUNC_MAGIC)


def set_trace_func(args):
    hci.logger.setLevel(args.trace_level)


def serial_port_func(args):
    global hci
    global PORT_INITIALIZED
    if hci is not None:
        hci.exit()
        hci = BleHci(args.serialPort, baud=args.baudRate, monPort_id=args.monPort)
    else:
        hci = BleHci(args.serialPort, baud=args.baudRate, monPort_id=args.monPort)

    PORT_INITIALIZED = True


def set_id_func(args):
    global hci
    hci.id = args.idtag


################## MAIN ##################
if __name__ == "__main__":
    # Setup the signal handler to catch the ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    # Setup the command line description text
    DESC_TEXT = f"""
        Bluetooth Low Energy HCI tool.
        This tool is used in tandem with the BLE controller examples. 
        This tool sends HCI commands through the serial port to the target device. 
        It will receive and print the HCI events received from the target device.
        Serial port is configured as 8N1, no flow control, default baud rate of {str(DEFAULT_BAUD)}
        """

    # Parse the command line arguments
    parser = argparse.ArgumentParser(
        description=DESC_TEXT, formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "serialPort",
        nargs="?",
        default=None,
        help="Serial port path or COM#. Default: None"
        + '\nIf not set, set using the "port" command.',
    )
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
        help="Commands to run on startup."
        + "\nIf more than 1, separate commands with a comma.",
    )

    args = parser.parse_args()

    if args.serialPort is None:
        logger.warning(
            "Serial port not initialized. Set port using the 'port' command."
        )
        PORT_INITIALIZED = False
    else:
        PORT_INITIALIZED = True
        hci = BleHci(args.serialPort, baud=args.baudRate, id_tag=args.idtag)

    print("Bluetooth Low Energy HCI tool")
    print(f"Serial port: {args.serialPort}")
    print(f"Monitor Trace Msg Serial Port: {args.monPort}")
    print(f"8N1 {args.baudRate}")

    COMMANDS = args.commands
    if COMMANDS:
        if len(COMMANDS) > 1:
            COMMANDS = " ".join(COMMANDS)
        else:
            COMMANDS = COMMANDS[0]

        COMMANDS = COMMANDS.split(",")
        COMMANDS = [x.strip() for x in COMMANDS]

        print("Startup commands: ")
        for x in COMMANDS:
            print(f"\t{x}")

    # Start the terminal argparse
    terminal = ArgumentParser(prog="", add_help=True)
    subparsers = terminal.add_subparsers()

    #### ADDR PARSER ####
    addr_parser = subparsers.add_parser(
        "addr", help="Set the device address.", formatter_class=RawTextHelpFormatter
    )
    addr_parser.add_argument("addr", help="Device address, ex: 00:11:22:33:44:55")
    addr_parser.set_defaults(func=addr_func, which="addr")

    memstats_parser = subparsers.add_parser(
        "memstats",
        help="Get BLE stack memory usage statistics",
        formatter_class=RawTextHelpFormatter,
    )

    memstats_parser.set_defaults(func=memstats_func)

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
        type=hex_int,
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

    adv_parser.add_argument(
        "--stats",
        dest="stats",
        action="store_true",
        help="Periodically print the connection stats if listening.",
    )
    adv_parser.add_argument(
        "--maintain",
        dest="maintain",
        action="store_true",
        help="Setup an event listener to restart advertising if we disconnect.",
    )
    adv_parser.set_defaults(func=adv_func, which="adv")

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
        type=hex_int,
        default=DEFAULT_SCAN_INTERVAL,
        help=f"""Scanning interval in units of 0.625 ms, 16-bit hex number 0x0020 - 0x4000.
        Default: 0x{DEFAULT_SCAN_INTERVAL}""",
    )
    scan_parser.set_defaults(func=scan_func, which="scan")

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
        type=hex_int,
        default=DEFAULT_CONN_INTERVAL,
        help=f"""Connection interval in units of 1.25ms, 16-bit hex number 0x0006 - 0x0C80."
        Default: {hex(DEFAULT_CONN_INTERVAL)}""",
    )
    init_parser.add_argument(
        "-t",
        "--timeout",
        dest="sup_timeout",
        type=hex_int,
        default=DEFAULT_SUP_TIMEOUT,
        help=f"""Supervision timeout in units of 10ms, 16-bit hex number 0x000A - 0x0C80.
        "Default: {hex(DEFAULT_SUP_TIMEOUT)}""",
    )
    init_parser.add_argument(
        "-l",
        "--listen",
        dest="listen",
        default=False,
        nargs="?",
        action=ListenAction,
        help="Enable listening for events.\nUses: "
        + "\n-l           --> listens indefinitely, ctrl-c to exit"
        + "\n-l N_SECONDS --> listens for N_SECONDS, then returns",
    )
    init_parser.add_argument(
        "--stats",
        dest="stats",
        action="store_true",
        help="Periodically print the connection stats if listening.",
    )
    init_parser.add_argument(
        "--maintain",
        dest="maintain",
        action="store_true",
        help="Setup an event listener to restart advertising if we disconnect.",
    )
    init_parser.set_defaults(func=init_func, which="init")

    datalen_parser = subparsers.add_parser(
        "data-len", help="Set the max data length", formatter_class=RawTextHelpFormatter
    )
    datalen_parser.set_defaults(func=data_len_func, which="dataLen")

    sendacl_parser = subparsers.add_parser(
        "send-acl", help="Send ACL packets", formatter_class=RawTextHelpFormatter
    )
    sendacl_parser.add_argument(
        "packet_length",
        type=int,
        help="Number of bytes per ACL packet, 16-bit decimal 1-65535, 0 to disable.",
    )
    sendacl_parser.add_argument(
        "num_packets",
        type=int,
        help="Number of packets to send, 8-bit decimal 1-255, 0 to enable auto-generate",
    )
    sendacl_parser.set_defaults(func=send_acl_func, which="sendAcl")

    sinkAcl_parser = subparsers.add_parser(
        "sink-acl",
        help="Sink ACL packets, do not send events to host",
        formatter_class=RawTextHelpFormatter,
    )
    sinkAcl_parser.set_defaults(func=sink_acl_func, which="sinkAcl")

    connStats_parser = subparsers.add_parser(
        "connstats",
        help="Get the connection stats",
        formatter_class=RawTextHelpFormatter,
    )
    connStats_parser.set_defaults(func=conn_stats_func, which="connstats")

    #### PHY PARSER ####
    phy_parser = subparsers.add_parser(
        "phy",
        help="Update the PHY in the active connection",
        formatter_class=RawTextHelpFormatter,
    )
    phy_parser.add_argument(
        "--phy",
        type=int,
        default=1,
        help="Desired PHY\n1: 1M\n2: 2M\n3: S8\n4: S2\nDefault: 1M",
    )
    ## TODO: fix this its weird
    phy_parser.add_argument(
        "-t",
        "--timeout",
        dest="timeout",
        type=int,
        help="Number of seconds to listen for after setting PHY.",
    )
    phy_parser.set_defaults(func=phy_func, which="phy")

    #### RESET PARSER ####
    reset_parser = subparsers.add_parser("reset", help="Sends an HCI reset command")
    reset_parser.set_defaults(func=reset_func, which="reset")

    #### LISTEN PARSER ####
    listen_parser = subparsers.add_parser(
        "listen", help="Listen for HCI events, print to screen"
    )
    listen_parser.add_argument(
        "-t",
        "--time",
        dest="time",
        type=int,
        default=0,
        help="Time to listen in seconds. Default: 0 (indefinitely)",
    )
    listen_parser.add_argument(
        "--stats",
        dest="stats",
        action="store_true",
        help="Periodically print the connection stats if listening.",
    )
    listen_parser.set_defaults(func=memstats_func, which="listen")

    txTest_parser = subparsers.add_parser(
        "tx-test",
        aliases=["tx"],
        help="Execute the transmitter test.",
        formatter_class=RawTextHelpFormatter,
    )
    txTest_parser.add_argument(
        "-c",
        "--channel",
        type=int,
        dest="channel",
        default=0,
        help="TX test channel, 0-39. Default: 0",
    )
    txTest_parser.add_argument(
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
    txTest_parser.add_argument(
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
    txTest_parser.add_argument(
        "-pl",
        "--packet-length",
        type=int,
        default=0,
        help="Tx packet length, number of bytes per packet, 0-255. Default: 0",
    )
    txTest_parser.set_defaults(func=tx_test_func, which="txTest")

    tx_test_vs_parser = subparsers.add_parser(
        "tx-test-vs",
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
    tx_test_vs_parser.set_defaults(func=tx_test_vs_func, which="txTestVS")

    #### RXTEST PARSER ####
    rxTest_parser = subparsers.add_parser(
        "rx-test",
        aliases=["rx"],
        help="Execute the receiver test",
        formatter_class=RawTextHelpFormatter,
    )
    rxTest_parser.add_argument(
        "-c",
        "--channel",
        dest="channel",
        type=int,
        default=0,
        help="Rx test channel, 0-39. Default: 0",
    )
    rxTest_parser.add_argument(
        "--phy",
        dest="phy",
        type=int,
        default=1,
        help="Rx Test PHY\n1: 1M\n2: 2M\n3: S8\n4: S2\nDefault: 1",
    )
    rxTest_parser.set_defaults(func=rx_test_func, which="rxTest")

    #### RXTESTVS PARSER ####
    rxTestVS_parser = subparsers.add_parser(
        "rx-test-vs",
        aliases=["rxvs"],
        help="Execute the vendor-specific receiver test",
        formatter_class=RawTextHelpFormatter,
    )
    rxTestVS_parser.add_argument(
        "-c",
        "--channel",
        dest="channel",
        type=int,
        default=0,
        help="Rx test channel. Default: 0",
    )
    rxTestVS_parser.add_argument(
        "--phy",
        dest="phy",
        type=int,
        default=1,
        help="Rx Test PHY\n1: 1M\n2: 2M\n3: S8\n4: S2\nDefault: 1",
    )
    rxTestVS_parser.add_argument(
        "-m",
        "--mod-idx",
        dest="modulationIdx",
        type=int,
        default=0,
        help="Vendor-specific modulation index",
    )
    rxTestVS_parser.add_argument(
        "-n",
        "--num_packets",
        dest="num_packets",
        type=int,
        default=0,
        help="Number of packets to transmit, 2 bytes hex, 0 equals infinite. Default: 0",
    )
    rxTestVS_parser.set_defaults(func=rx_test_vs_func, which="rxTestVS")

    #### ENDTEST PARSER ####
    endTest_parser = subparsers.add_parser(
        "end-test",
        aliases=["end"],
        help="End the Tx/Rx test, print the number of correctly received packets",
        formatter_class=RawTextHelpFormatter,
    )
    endTest_parser.set_defaults(func=end_test_func, which="endTest")

    #### ENDTESTVS PARSER ####
    reset_test_stats_parser = subparsers.add_parser(
        "reset-test-stats",
        aliases=["rst-ts"],
        help="Reseta accumulated stats from DTM",
        formatter_class=RawTextHelpFormatter,
    )
    reset_test_stats_parser.set_defaults(
        func=reset_test_stats_func, which="reset-test-stats"
    )
    
    #### TXPOWER PARSER ####
    txPower_parser = subparsers.add_parser(
        "tx-power",
        aliases=["txp"],
        help="Set the Tx power",
        formatter_class=RawTextHelpFormatter,
    )
    txPower_parser.add_argument(
        "power", type=int, help="Integer power setting in units of dBm."
    )
    txPower_parser.add_argument(
        "--handle", dest="handle", type=int, help="Connection handle, integer."
    )  ## TODO: CHECK THIS
    txPower_parser.set_defaults(func=tx_power_func, which="txPower")

    discon_parser = subparsers.add_parser(
        "discon",
        aliases=["dc"],
        help="Send the command to disconnect",
        formatter_class=RawTextHelpFormatter,
    )
    discon_parser.set_defaults(func=discon_func, which="discon")

    setChMap_parser = subparsers.add_parser(
        "set-ch-map",
        help="Set the connection channel map to a given channel.",
        formatter_class=RawTextHelpFormatter,
    )
    setChMap_parser.add_argument(
        "channel",
        type=int,
        nargs="?",
        help="""Channel to use in channel map
        Will set the channel map to the given channel plus one additional channel.""",
    )
    setChMap_parser.add_argument(
        "-m",
        "--mask",
        dest="mask",
        type=hex_int,
        help=""""4-byte hex number to use a channel map.
        0xFFFFFFFFFF uses all channels, 0x000000000F will use channels 0-3, etc""",
    )
    setChMap_parser.add_argument(
        "--handle",
        dest="handle",
        type=int,
        default=0,
        help="Connection handle, integer. Default: 0",
    )
    setChMap_parser.set_defaults(func=set_ch_map_func, which="setChMap")

    cmd_parser = subparsers.add_parser(
        "cmd", help="Send raw HCI command", formatter_class=RawTextHelpFormatter
    )
    cmd_parser.add_argument(
        "cmd",
        help='String of hex bytes LSB first\nex: "01030C00" to send HCI Reset command',
    )
    cmd_parser.add_argument(
        "-l",
        "--listen",
        dest="listen",
        action=ListenAction,
        default=False,
        help="Enable listening for events.\nUses: "
        + "\n-l           --> listens indefinitely, ctrl-c to exit"
        + "\n-l N_SECONDS --> listens for N_SECONDS, then returns",
    )
    cmd_parser.add_argument(
        "-t",
        "--timeout",
        dest="timeout",
        type=int,
        help="Command timeout, Default: None",
    )
    cmd_parser.set_defaults(func=cmd_func, which="cmd")

    readReg_parser = subparsers.add_parser(
        "read-reg",
        aliases=["read"],
        help="Read register, device performs a memcpy from address and returns the value",
        formatter_class=RawTextHelpFormatter,
    )
    readReg_parser.add_argument(
        "addr", help='Address to read, 32-bit hex value\nex: "0x20000000"'
    )
    readReg_parser.add_argument(
        "length",
        type=hex_int,
        help='Number of bytes to read, 4- or 8-bit hex value\nex: "0x2"',
    )
    readReg_parser.set_defaults(func=read_reg_func, which="readReg")

    writeReg_parser = subparsers.add_parser(
        "write-reg",
        aliases=["write"],
        help="Write register, device performs a memcpy to the memory address",
        formatter_class=RawTextHelpFormatter,
    )
    writeReg_parser.add_argument(
        "addr", help='Address to write, 32-bit hex value\nex:"0x20000000"'
    )
    writeReg_parser.add_argument(
        "value",
        type=hex_int,
        help='Data to write, 8-, 16-, or 32-bit hex value\nex:"0x12"',
    )
    writeReg_parser.set_defaults(func=write_reg_func, which="writeReg")

    #### EXIT PARSER ####
    exit_parser = subparsers.add_parser(
        "exit",
        aliases=["quit", "q"],
        help="Exit the program",
        formatter_class=RawTextHelpFormatter,
    )
    exit_parser.set_defaults(func=exit_func, which="exit")

    #### HELP PARSER ####
    help_parser = subparsers.add_parser("help", aliases=["h"], help="Show help message")
    help_parser.set_defaults(func=help_func, which="help")

    #### PORT PARSER ####
    port_parser = subparsers.add_parser(
        "port", help="Set the serialPort", formatter_class=RawTextHelpFormatter
    )
    port_parser.add_argument("serialPort", help="Serial port path or COM#")
    port_parser.add_argument(
        "-b",
        "--baud",
        dest="baudRate",
        type=int,
        default=DEFAULT_BAUD,
        help="Serial port baud rate. Default: " + str(DEFAULT_BAUD),
    )
    port_parser.add_argument(
        "-m",
        "--monitor-trace-port",
        dest="monPort",
        default=None,
        help="Monitor Trace Msg Serial Port path or COM#. Default: None",
    )
    port_parser.set_defaults(func=serial_port_func, which="port")

    #### ID PARSER ####
    id_parser = subparsers.add_parser(
        "id",
        aliases=["tag"],
        help="Set or change board ID for printing trace messages.",
        formatter_class=RawTextHelpFormatter,
    )
    id_parser.add_argument("idtag", help="Board ID tag for printing trace messages.")
    id_parser.set_defaults(func=set_id_func)

    #### TRACE PARSER ####
    trace_parser = subparsers.add_parser(
        "trace_level",
        aliases=["trace"],
        help="Set test trace messaging level",
        formatter_class=RawTextHelpFormatter,
    )
    trace_parser.add_argument(
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
    trace_parser.set_defaults(func=set_trace_func, which="trace")


    



    def completer(text, state):
        commands = list(subparsers.choices.keys())
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        return matches[state] if state < len(matches) else None

    
    readline.set_completer(completer)
    readline.parse_and_bind('tab: complete')

    COMMANDS_RUN = False
    if PORT_INITIALIZED and COMMANDS:
        logger.info("Port set, running input commands.")
        COMMANDS_RUN = run_input_cmds(COMMANDS)
    elif COMMANDS:
        logger.warning(
            "Warning: Serial port not initialized. Commands will be run after initialization."
        )

    while True:
        if COMMANDS and not COMMANDS_RUN and PORT_INITIALIZED:
            logger.info("Port set, running input commands.")
            COMMANDS_RUN = run_input_cmds(COMMANDS)

        astr = input(">>> ")
        try:
            args = terminal.parse_args(astr.split())

            if (
                not PORT_INITIALIZED
                and not args.which == "port"
                and not args.which == "help"
                and not args.which == "exit"
            ):
                logger.error(
                    "Serial port is not set. Set serial port using the 'port' command."
                )
            else:
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
        except Exception as err:
            logger.error('Unexpected exception %s', type(err).__name__)
