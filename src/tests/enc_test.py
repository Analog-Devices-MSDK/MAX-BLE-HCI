import argparse
import sys
from datetime import datetime
from max_ble_hci import BleHci
from max_ble_hci.utils import le_list_to_int
from max_ble_hci.packet_codes import StatusCode, EventSubcode
from max_ble_hci.hci_packets import EventPacket

from rich import print
from cryptography.hazmat.primitives.asymmetric import ec


from fastecdsa.curve import P256
from fastecdsa.point import Point


class Tester:
    def __init__(self, serial_port) -> None:
        self.serial_port = serial_port
        self.hci = BleHci(
            serial_port, id_tag="hci1", timeout=5, evt_callback=self.common_callback
        )

        self.event_done = False
        self.results = {}

    def _pub_key_read_event(self, packet: EventPacket):
        packet.get_return_params()

        status, xcoord, ycoord = packet.get_return_params([1, 32, 32])
        status = StatusCode(status)

        if status != StatusCode.SUCCESS:
            print(f"Read pub key failed. Status: {status}")

        try:
            _ = Point(xcoord, ycoord, curve=P256)
            self.results["pub-key-read"] = True
        except ValueError:
            self.results["pub-key-read"] = False
            print("Point not on curve. Encryption fail")

    def _dhk_event(self, packet: EventPacket):
        if (
            StatusCode(packet.evt_params[0])
            == StatusCode.ERROR_CODE_INVALID_HCI_CMD_PARAMS
        ):
            self.results["dhk"] = True
        else:
            self.results["dhk"] = False

    def common_callback(self, packet: EventPacket):
        if packet.evt_subcode == EventSubcode.READ_LOCAL_P256_PUB_KEY_CMPLT:
            self._pub_key_read_event(packet)
        elif packet.evt_subcode == EventSubcode.GENERATE_DHKEY_CMPLT:
            self._dhk_event(packet)

        self.event_done = True

    def _run_pub_key_read(self):
        self.event_done = False
        status = self.hci.read_local_p256_pub_key()

        if status != StatusCode.SUCCESS:
            return False

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

    def run(self):
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
    port = ""

    parser = argparse.ArgumentParser(description="Basic HCI Encryption tests")
    parser.add_argument("serial_port", nargs="?", help="Serial port used for HCI")
    args = parser.parse_args()

    if args.serial_port and args.serial_port != "":
        print(args.serial_port)
        port = args.serial_port

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
