import time
import sys

from ble_hci import BleHci

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6TZ-if00-port0"

def reset():
    hci = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1)
    print(sys.getrefcount(hci))
    hci.reset()

if __name__ == "__main__":
    # hci = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1)

    # for _ in range(1000):
    #     print(hci.reset())
    try:
        reset()
        time.sleep(1)
        reset()
    except Exception as err:
        print(err)
        sys.exit(0)
