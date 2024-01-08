    
from ble_hci import BleHci
import ble_hci.packet_codes as pc 
import time

#Serial ports used for HCI
master_hci_port = '' 
slave_hci_port = '' 


def main():
    master = BleHci(master_hci_port)
    slave = BleHci(slave_hci_port)

    master.reset()
    slave.reset()

    master_addr = 0x001234887733
    slave_addr = 0x111234887733

    master.set_adv_tx_power(-10)
    slave.set_adv_tx_power(-10)

    slave.set_address(slave_addr)
    master.set_address(master_addr)

    slave.start_advertising(connect=True)
    master.init_connection(addr=slave_addr)
   

    while True:
        slave_stats, _ = slave.get_conn_stats()
        master_stats, _ = master.get_conn_stats()

        if slave_stats.rx_data and master_stats.rx_data:
            print(f'Slave PER {slave_stats.per()}')
            print(f'Master PER {master_stats.per()}')
            break
        
        time.sleep(0.5)


    master.disconnect()
    slave.disconnect()

    master.reset()
    slave.reset()