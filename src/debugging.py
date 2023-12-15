import dataclasses
import sys
import time

from ble_hci import BleHci
from ble_hci.ble_hci import PortConfig

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30GPTRC-if00-port0"
PORT_ID2 = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30GQ5JP-if00-port0"


def reset():
    hci = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1)

    hci.reset()


if __name__ == "__main__":

    pcfg = PortConfig(PORT_ID)


    # hci = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1)
    hci2 = BleHci(PORT_ID2, log_level="INFO", retries=1, timeout=1)

    # for _ in range(2):
    # print(hci.reset())
    hci2.reset()
    # try:
    #     reset()
    #     time.sleep(1)
    #     reset()
    # except Exception as err:
    #     print(err)
    #     sys.exit(0)
