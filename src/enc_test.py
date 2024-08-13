import sys
from max_ble_hci import BleHci
from max_ble_hci.utils import le_list_to_int
from max_ble_hci.packet_codes import StatusCode
from max_ble_hci.hci_packets import EventPacket, LEControllerOCF
from max_ble_hci.constants import PhyOption, PubKeyValidateMode

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
            print("Pub key valid!")
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

    def _run_bad_dhk(self):
    
        event: EventPacket = self.hci.write_command_raw(
            "012620401ea1f0f01faf1d9609592284f19e4c0047b58afd8615a69f559077b22faaa1904c55f33e429dad377356703a9ab85160472d1130e28e36765f89aff915b1214b"
        )
        print(event.status)

        # self.hci.write_command_raw()
        # bad_params = [
        #     65,
        #     64,
        #     30,
        #     161,
        #     240,
        #     240,
        #     31,
        #     175,
        #     29,
        #     150,
        #     9,
        #     89,
        #     34,
        #     132,
        #     241,
        #     158,
        #     76,
        #     0,
        #     71,
        #     181,
        #     138,
        #     253,
        #     134,
        #     21,
        #     166,
        #     159,
        #     85,
        #     144,
        #     119,
        #     178,
        #     47,
        #     170,
        #     161,
        #     144,
        #     76,
        #     85,
        #     243,
        #     62,
        #     66,
        #     157,
        #     173,
        #     55,
        #     115,
        #     86,
        #     112,
        #     58,
        #     154,
        #     184,
        #     81,
        #     96,
        #     71,
        #     45,
        #     17,
        #     48,
        #     226,
        #     142,
        #     54,
        #     118,
        #     95,
        #     137,
        #     175,
        #     249,
        #     21,
        #     177,
        #     33,
        #     75,
        # ]
        # status = self.hci.send_le_controller_command(
        #     LEControllerOCF.GENERATE_DHKEY, params=bad_params
        # )

        

    def _run_simple_aes(self):
        pass

    def run(self):
        status = self.hci.reset()
        if status != StatusCode.SUCCESS:
            return False
        
        self._run_pub_key_read()
        self._run_bad_dhk()
        self._run_simple_aes()
      


if __name__ == "__main__":
    # PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"
    PORT = "/dev/serial/by-id/usb-ARM_DAPLink_CMSIS-DAP_04091702a987036900000000000000000000000097969906-if01"

    tester = Tester(PORT)
    tester.run()
