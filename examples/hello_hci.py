from ble_hci import BleHci

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NMWQ-if00-port0"

controller = BleHci(PORT)
event = controller.reset()

print(event)
