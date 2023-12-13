import time

from ble_hci import BleHci

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6TZ-if00-port0"

if __name__ == "__main__":
    hci = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1)

    for _ in range(100):
        print(hci.reset())
        print(hci.tx_test())
        # print(hci.end_test_vs())
        print(hci.end_test())
        print(hci.get_test_stats())
        print(hci.reset_test_stats())
