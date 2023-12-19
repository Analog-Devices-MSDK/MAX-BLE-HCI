import dataclasses
import sys
import time

from ble_hci import BleHci
from ble_hci.ble_hci import PortConfig
from ble_hci.packet_codes import StatusCode

PORT_ID = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"
PORT_ID2 = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30GQ5JP-if00-port0"


def reset(id_num):
    hci = BleHci(
        PORT_ID, log_level="INFO", retries=1, timeout=1, id_tag=f"LOCAL{id_num}"
    )

    hci.reset()
def test_dtm(central:BleHci, peripheral:BleHci, test_time:float = 3):
    
    assert central.set_adv_tx_power(-10) == StatusCode.LL_SUCCESS
    assert central.reset_test_stats() == StatusCode.LL_SUCCESS
    assert central.tx_test_vs(num_packets=1000)  == StatusCode.LL_SUCCESS
    peripheral.rx_test()
    time.sleep(test_time)

    central.end_test()
    rx_packets = peripheral.end_test()
    stats_periph = peripheral.get_test_stats()
    print(rx_packets,stats_periph)

    stats_central = central.get_test_stats()
    print(stats_central)


    # tx_packets = central.get_test_stats()[0]['tx-data']
    # print(100 - (rx_packets/ tx_packets) * 100)





    


if __name__ == "__main__":
  
    hci1 = BleHci(PORT_ID, log_level="INFO", retries=1, timeout=1, id_tag="CEN")
    hci2 = BleHci(PORT_ID2, log_level="INFO", retries=1, timeout=1, id_tag="PERIPH")

    # hci1.reset()
    # hci2.reset()


    test_dtm(hci1, hci2)