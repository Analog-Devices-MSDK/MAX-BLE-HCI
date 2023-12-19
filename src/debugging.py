import dataclasses
import sys
import time

from ble_hci import BleHci
from ble_hci.ble_hci import PortConfig

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6TZ-if00-port0"
PORT_ID2 = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30GQ5JP-if00-port0"


def reset(id_num):
    hci = BleHci(
        PORT_ID, log_level="INFO", retries=1, timeout=1, id_tag=f"LOCAL{id_num}"
    )

    hci.reset()


if __name__ == "__main__":
    # pcfg = PortConfig(PORT_ID)

    hci = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1, id_tag="GLOBAL")
    hci2 = BleHci(PORT_ID2, log_level="INFO", retries=1, timeout=1, id_tag="SOLO")

    for _ in range(2):
        print(hci.reset())
    hci2.reset()
    try:
        reset(1)
        time.sleep(1)
        reset(2)
        hci2.reset()
    except Exception as err:
        print(err)
        sys.exit(0)
