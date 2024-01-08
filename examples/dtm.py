from ble_hci import BleHci
import time

rx_hci_port = ''
tx_hci_port = ''

def main():
    TX_POWER = -10
    NUM_PACKETS = 100

    rx_hci = BleHci(rx_hci_port)
    tx_hci = BleHci(rx_hci_port)



    tx_hci.set_adv_tx_power(TX_POWER)
    tx_hci.reset_test_stats()
    rx_hci.reset_test_stats()

    rx_hci.rx_test()
    
    tx_hci.tx_test_vs(num_packets=NUM_PACKETS)

    time.sleep(0.1)

    tx_hci.end_test()
    rx_hci.end_test()

    tx_stats, _ = tx_hci.get_test_stats()
    rx_stats, _ = rx_hci.get_test_stats()

    per = rx_stats.per(tx_stats)

    print(per)
    
    
if __name__ == '__main__':
    main()
    