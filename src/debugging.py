from ble_hci import BleHci
import time

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6TZ-if00-port0"

if __name__ == "__main__":
    hci = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1)

    

