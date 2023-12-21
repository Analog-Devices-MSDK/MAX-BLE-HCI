import dataclasses
import sys
import time

from ble_hci import BleHci
from ble_hci.ble_hci import PortConfig
from ble_hci.packet_codes import StatusCode
from ble_hci.data_params import ConnParams

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6TZ-if00-port0"
PORT_ID2 = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30GQ5JP-if00-port0"


if __name__ == "__main__":
    slave = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1, id_tag="slave")
    master = BleHci(PORT_ID2, log_level="INFO", retries=1, timeout=1, id_tag="master")

    master.reset()
    #slave.reset()

    master_addr = 0x001234887733
    slave_addr = 0x111234887733

    master.set_adv_tx_power(-10)
    slave.set_adv_tx_power(-10)

    slave.set_address(slave_addr)
    master.set_address(master_addr)

    status = slave.start_advertising(connect=True)
    assert status == StatusCode.LL_SUCCESS, f"Failed to start advertising {status}"
    status = master.init_connection(addr=slave_addr)
    assert status == StatusCode.LL_SUCCESS, f"Failed to init {status}"
    print("****************************************************")
    while True:
        time.sleep(10)
        slave_stats, pstatus = slave.get_conn_stats()
        master_stats, mstatus = master.get_conn_stats()

        print(slave_stats, pstatus)
        print(master_stats, mstatus)
