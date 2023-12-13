from ble_hci import BleHci
PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"

if __name__ == '__main__':
    hci = BleHci(PORT_ID, log_level='INFO', retries=0)

    # print(hci.reset())

    hci.tx_test()
    