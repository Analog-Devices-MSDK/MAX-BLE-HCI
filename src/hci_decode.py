import argparse
from max_ble_hci.hci_packets import (
    EventPacket,
    CommandPacket,
    AsyncPacket,
    ExtendedPacket,
)
from max_ble_hci.packet_defs import PacketType, OGF, OCF
from max_ble_hci.packet_codes import StatusCode
import binascii


def main():
    parser = argparse.ArgumentParser(
        description="Evaluates connection sensitivity",
    )

    parser.add_argument("command", help="Central board")

    args = parser.parse_args()

    packet_type = int(args.command[:2], 16)
    packet_type = PacketType(packet_type)

    command = binascii.unhexlify(args.command[2:])

    if packet_type == PacketType.COMMAND:
        print(CommandPacket.from_bytes(command))
    elif packet_type == PacketType.EXTENDED:
        pass
    elif packet_type == PacketType.ASYNC:
        print(AsyncPacket.from_bytes(command))
    elif packet_type == PacketType.EVENT:
        print(EventPacket.from_bytes(command))
    else:
        ValueError(f"Unnknown packet type {packet_type}")


if __name__ == "__main__":
    main()
