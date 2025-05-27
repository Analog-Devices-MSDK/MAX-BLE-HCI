# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""HCI decoding tool command-line interface."""
import argparse
import binascii
import hci_decode_tools
from hci_decode_tools.sniffer import HciSerialSniffer, HciSerialSnifferPortCfg

_DESC = """hcitools: HCI decoding tools"""

def _run_decode_cli(args: argparse.Namespace) -> None:
    """
    Run the decode command.
    """
    pkt_bytes = binascii.unhexlify(args.hci_packet)
    print(hci_decode_tools.decode_packet(pkt_bytes))

def _run_file_cli(args: argparse.Namespace) -> None:
    """
    Run the file command.
    """
    decoded = ""
    if args.is_bytes:
        decoded = hci_decode_tools.decode_bytes_file(args.filepath)
    else:
        decoded = hci_decode_tools.decode_text_file(
            args.filepath,
            leading=args.pkt_tag,
            c2h_tag=args.c2h_tag,
            h2c_tag=args.h2c_tag
        )

    if args.output_path is not None:
        with open(args.output_path, "w", encoding="utf-8") as hci_out:
            hci_out.write(decoded)
    else:
        print(decoded)

def _run_sniff_cli(args:argparse.Namespace) -> None:
    """
    Run the sniff command.
    """
    cfg = HciSerialSnifferPortCfg(
        baudrate = args.baud,
        bytesize = args.bytesize,
        parity = args.parity,
        stopbits=args.stopbits,
        timeout=args.timeout,
        xonxoff=args.xonxoff,
        rtscts=args.rtscts,
        dsrdtr=args.dsrdtr,
        write_timeout=args.write_timeout,
        inter_byte_timeout=args.inter_byte_timeout,
        exclusive=args.exclusive
    )
    sniff_mode = HciSerialSniffer.SniffMode.BIDIRECTIONAL
    if args.sniff_mode in ["ctrl2host", "c2h"]:
        sniff_mode = HciSerialSniffer.SniffMode.CTRL2HOST_ONLY
    elif args.sniff_mode in ["host2ctrl", "h2c"]:
        sniff_mode = HciSerialSniffer.SniffMode.HOST2CTRL_ONLY
    sniffer = HciSerialSniffer(
        args.serial_port,
        sniff_mode=sniff_mode,
        port_config=cfg,
        output_file=args.output_file
    )

    print("=============================================")
    print(f"Sniffer Proxy Port: {sniffer.get_proxy()}")
    print("=============================================\n")

    try:
        sniffer.start()
        sniffer.join()
    except KeyboardInterrupt:
        sniffer.close()

def _init_decode_cli(parser: argparse.ArgumentParser) -> None:
    """
    Initialize the decode command.
    """
    parser.add_argument("hci_packet", help="Hci packet to decode")
    parser.set_defaults(func=_run_decode_cli)

def _init_file_cli(parser: argparse.ArgumentParser) -> None:
    """
    Initialize the file command.
    """
    parser.add_argument("filepath", help="Path to the file to decode")
    parser.add_argument(
        "-t", "--tag",
        dest="pkt_tag",
        default=None,
        action="append",
        help="Leading characters on HCI packet lines, can be used more than once"
    )
    parser.add_argument(
        "-c2h", "--c2h-tag",
        dest="c2h_tag",
        default = None,
        help="Leading characters on ctrl2host HCI packet lines, can replace tags"
    )
    parser.add_argument(
        "-h2c", "--h2c-tag",
        dest="h2c_tag",
        default = None,
        help="Leading characters on host2ctrl HCI packet lines, can replace tags"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_path",
        default=None,
        help="Specify a file in which to write output (default prints to console)"
    )
    parser.add_argument(
        "--is-bytes",
        dest="is_bytes",
        action="store_true",
        help="Indicate file to decode is a binary file, tags are ignored"
    )
    parser.set_defaults(func=_run_file_cli)

def _init_sniff_cli(parser: argparse.ArgumentParser) -> None:
    """
    Initialize the sniff command.
    """
    parser.add_argument("serial_port", help="Serial port to sniff")
    parser.add_argument(
        "-m", "--mode",
        dest="sniff_mode",
        type=str.lower,
        default="bidirectional",
        choices=["ctrl2host", "c2h", "host2ctrl", "h2c", "bidirectional", "both"],
        help="IO path to sniff"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        default=None,
        help="Specify a file in which to write output (default prints to console)"
    )
    parser.add_argument(
        "-b", "--baudrate",
        dest="baud",
        type=int,
        default=115200,
        help="Serial port baud rate"
    )
    parser.add_argument(
        "-bs", "--bytesize",
        dest="bytesize",
        type=int,
        default=8,
        choices=[5, 6, 7, 8],
        help="Serial port byte size"
    )
    parser.add_argument(
        "-p", "--parity",
        dest="parity",
        type=str.upper,
        default="N",
        choices=["E", "M", "N", "O", "S"],
        help="Serial port parity (Even, Mark, None, Odd, or Space)"
    )
    parser.add_argument(
        "-s", "--stopbits",
        dest="stopbits",
        type=float,
        default=1,
        choices=[1, 1.5, 2],
        help="Serial port stop bits"
    )
    parser.add_argument(
        "-t", "--timeout",
        dest="timeout",
        type=float,
        default=None,
        help="Read timeout in seconds, may interfere with flow control"
    )
    parser.add_argument(
        "-w", "--write-timeout",
        dest="write_timeout",
        type=float,
        default=None,
        help="Write timeout in seconds, may interfere with flow control"
    )
    parser.add_argument(
        "-i", "--inter-byte-timeout",
        dest="inter_byte_timeout",
        type=float,
        default=None,
        help="Inter character timeout in seconds, may interfere with flow control"
    )
    parser.add_argument(
        "--xonxoff",
        dest="xonxoff",
        action="store_true",
        help="Enable software flow control"
    )
    parser.add_argument(
        "--rtscts",
        dest="rtscts",
        action="store_true",
        help="Enable rts/cts hardware flow control"
    )
    parser.add_argument(
        "--dsrdtr",
        dest="dsrdtr",
        action="store_true",
        help="Enable dsr/dtr hardware flow control"
    )
    parser.add_argument(
        "--exclusive",
        dest="exclusive",
        action="store_true",
        help="Set exclusive access mode"
    )
    parser.set_defaults(func=_run_sniff_cli)

def init_cli() -> argparse.Namespace:
    """Initialize the hcitools command line interface.

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments.

    """
    parser = argparse.ArgumentParser(
        description=_DESC,
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers()
    decode_parser = subparsers.add_parser(
        "decode",
        help="Decode an HCI packet",
        formatter_class=argparse.RawTextHelpFormatter
    )
    file_parser = subparsers.add_parser(
        "file",
        help="Decode HCI packets from a file",
        formatter_class=argparse.RawTextHelpFormatter
    )
    sniff_parser = subparsers.add_parser(
        "sniff",
        help="Sniff/Decode HCI packets on a serial port (CTRL-C to exit)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    _init_decode_cli(decode_parser)
    _init_file_cli(file_parser)
    _init_sniff_cli(sniff_parser)
    return parser.parse_args()

def main() -> None:
    """
    Main function for the hcitools command line interface.
    """
    args = init_cli()
    args.func(args)

if __name__ == "__main__":
    main()
