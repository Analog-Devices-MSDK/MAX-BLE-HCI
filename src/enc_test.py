import os
import sys
from max_ble_hci import BleHci
from max_ble_hci.utils import le_list_to_int
from max_ble_hci.packet_codes import StatusCode
from max_ble_hci.hci_packets import EventPacket, LEControllerOCF
from max_ble_hci.constants import PhyOption, PubKeyValidateMode
import pyaes
from rich import print

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"


from fastecdsa.curve import P256
from fastecdsa.point import Point


class Tester:
    def __init__(self, serial_port) -> None:
        self.serial_port = serial_port
        self.hci = BleHci(PORT, id_tag="hci1", timeout=5)
        self.event_done = False
        self.results = {}

    def pub_key_read_callback(self, packet: EventPacket):
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

        self.hci.port.evt_callback = print
        self.event_done = True

    def _run_pub_key_read(self):
        status = self.hci.enable_all_events()
        if status != StatusCode.SUCCESS:
            print("Failed to enable events")
            return False

        self.event_done = False
        status = self.hci.read_local_p256_pub_key(callback=self.pub_key_read_callback)

        if status != StatusCode.SUCCESS:
            return False

        while not self.event_done:
            pass

        self.hci.disable_all_events()

    def _run_bad_dhk(self):
        event: EventPacket = self.hci.write_command_raw(
            "012620401ea1f0f01faf1d9609592284f19e4c0047b58afd8616a69f559077b22faaa1904c55f33e429dad377356703a9ab85160472d1130e28e36765f89aff915b1214b"
        )

        if event.status == StatusCode.SUCCESS:
            print("[red]DHK gen returned succes. Not expected[/red]")
            self.results["dhk"] = False
        else:
            self.results["dhk"] = True

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

        self._run_pub_key_read()
        self._run_bad_dhk()
        self._run_simple_aes()

        total_result = True
        for test, result in self.results.items():
            print(f"{test}:", "[green]Pass[/green]" if result else "[red]Fail[/red]")
            if not result:
                total_result = False

        return total_result


if __name__ == "__main__":
    PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"
    PORT = "/dev/serial/by-id/usb-ARM_DAPLink_CMSIS-DAP_04091702a987036900000000000000000000000097969906-if01"

    tester = Tester(PORT)
    result = tester.run()

    if not result:
        sys.exit(-1)
    else:
        sys.exit(0)
