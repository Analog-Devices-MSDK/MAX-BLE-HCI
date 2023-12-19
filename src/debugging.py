import dataclasses
import sys
import time

from ble_hci import BleHci
from ble_hci.ble_hci import PortConfig
from ble_hci.packet_codes import StatusCode

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"
PORT_ID2 = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30GQ5JP-if00-port0"


    






    


if __name__ == "__main__":
  
    master = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1, id_tag="CEN")
    slave = BleHci(PORT_ID2, log_level="INFO", retries=1, timeout=1, id_tag="PERIPH")

    master.reset()
    slave.reset()

    master_addr = [0x00,0x12,0x34,0x88,0x77,0x33]
    slave_addr = [0x11,0x12,0x34,0x88,0x77,0x33]

    master.set_address(master_addr)
    slave.set_address(slave_addr)






    