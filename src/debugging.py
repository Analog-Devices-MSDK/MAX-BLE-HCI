from ble_hci import BleHci
import time
PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"

if __name__ == '__main__':
    hci = BleHci(PORT_ID, log_level='INFO', retries=0)

    for i in range(100):
        hci.reset()
        hci.tx_test()
        hci.end_test()
        print(hci.get_test_stats())
        hci.reset_test_stats()