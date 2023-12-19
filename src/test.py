import secrets
import unittest
import time
from ble_hci import BleHci, ble_hci
from ble_hci import packet_codes as pc
from ble_hci import packet_defs as pd

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"
PORT2 = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30GQ5JP-if00-port0"
hci1 = BleHci(PORT, id_tag="hci1")
hci2 = BleHci(PORT2, id_tag="hci2")
MAX_U32 = 0xFFFFFFFF
A32 = 0xAAAAAAAA


class TestHci(unittest.TestCase):
    def test_reset(self):
        # Reset puts code into nice condition, make sure it works before any tests
        self.assertEqual(hci1.reset(), pc.StatusCode.LL_SUCCESS)
        self.assertEqual(hci2.reset(), pc.StatusCode.LL_SUCCESS)



    def test_commands(self):
        hci1.reset()

        self.assertEqual(hci1.set_tx_test_err_pattern(A32), pc.StatusCode.LL_SUCCESS)
        self.assertIsNotNone(hci1.set_connection_op_flags(1, MAX_U32, True))

        key = list(secrets.token_bytes(32))
        self.assertEqual(hci1.set_256_priv_key(key), pc.StatusCode.LL_SUCCESS)
        self.assertEqual(
            hci1.get_channel_map_periodic_scan_adv(1, False)[1],
            pc.StatusCode.LL_SUCCESS,
        )
        self.assertIsNotNone(hci1.get_acl_test_report())

        self.assertEqual(
            hci1.set_local_num_min_used_channels(ble_hci.PhyOption.P1M, 0, 10),
            pc.StatusCode.LL_SUCCESS,
        )

        self.assertEqual(
            hci1.get_peer_min_num_channels_used(1)[1],
            pc.StatusCode.LL_ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(
            hci1.set_validate_pub_key_mode(pd.PubKeyValidateMode.ALT1),
            pc.StatusCode.LL_SUCCESS,
        )

        addr, status = hci1.get_rand_address()
        self.assertTrue(len(addr) == 6 or status != pc.StatusCode.LL_SUCCESS)

        self.assertEqual(hci1.set_local_feature(0), pc.StatusCode.LL_SUCCESS)

        self.assertEqual(hci1.set_operational_flags(0, True), pc.StatusCode.LL_SUCCESS)

        self.assertEqual(
            hci1.set_encryption_mode(1, True, True),
            pc.StatusCode.LL_ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(hci1.set_diagnostic_mode(True), pc.StatusCode.LL_SUCCESS)

    def test_stats(self):
        stats, status = hci1.get_pdu_filter_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci1.get_memory_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci1.get_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)
        stats, status = hci1.get_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci1.get_conn_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci1.get_test_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci1.get_aux_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci1.get_aux_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)
        self.assertEqual(
            hci1.set_connection_phy_tx_power(1, 0, ble_hci.PhyOption.P1M),
            pc.StatusCode.LL_ERROR_CODE_UNKNOWN_CONN_ID,
        )

        # stats, status = hci1.get_periodic_scanning_stats()
        # self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)
    def test_dtm(self):
        TX_POWER = -10
        NUM_PACKETS = 100

        self.assertEqual(hci1.set_adv_tx_power(TX_POWER), pc.StatusCode.LL_SUCCESS)
        self.assertEqual(hci1.reset_test_stats(), pc.StatusCode.LL_SUCCESS)
        self.assertEqual(hci2.reset_test_stats(), pc.StatusCode.LL_SUCCESS)

        self.assertEqual(hci2.rx_test(), pc.StatusCode.LL_SUCCESS)
        self.assertEqual(
            hci1.tx_test_vs(num_packets=NUM_PACKETS), pc.StatusCode.LL_SUCCESS
        )

        time.sleep(0.1)

        hci1.end_test()
        rx_ok = hci2.end_test()

        stats_central, status_central = hci1.get_test_stats()
        stats_periph, status_peripheral = hci2.get_test_stats()

        self.assertEqual(status_central, pc.StatusCode.LL_SUCCESS)
        self.assertEqual(status_peripheral, pc.StatusCode.LL_SUCCESS)

        self.assertEqual(rx_ok, stats_periph.rx_data)
        self.assertEqual(NUM_PACKETS, stats_central.tx_data)

        hci1.reset_test_stats()
        hci2.reset_test_stats()

        stats_central, _ = hci1.get_test_stats()
        stats_periph, _ = hci2.get_test_stats()

        for key in stats_central.__dict__:
            self.assertTrue(stats_central.__dict__[key], pc.StatusCode.LL_SUCCESS)
            self.assertTrue(stats_periph.__dict__[key], pc.StatusCode.LL_SUCCESS)

    def test_connection(self):
        master = hci1
        slave = hci2

        master.reset()
        slave.reset()

        master_addr = 0x001234887733
        slave_addr = 0x111234887733

        master.set_adv_tx_power(-10)
        slave.set_adv_tx_power(-10)

        slave.set_address(slave_addr)
        master.set_address(master_addr)

        status = slave.start_advertising(connect=True)
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)
        status = master.init_connection(addr=slave_addr)
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)
        
        
        while True:
            slave_stats, _ = slave.get_conn_stats()
            master_stats, _ = master.get_conn_stats()

            if slave_stats.rx_data and master_stats.rx_data:
                break
            time.sleep(0.5)


        self.assertEqual(master.disconnect(), pc.StatusCode.LL_SUCCESS)
        self.assertEqual(slave.disconnect(), pc.StatusCode.LL_ERROR_CODE_CONN_TERM_BY_LOCAL_HOST)
        
        master.reset()
        slave.reset()

    def test_iso(self):
        _, status = hci1.get_iso_test_report()
        if status == pc.StatusCode.LL_DECODE_FAILURE:
            # ISO not enabled
            return

        status = hci1.enable_iso_packet_sink(True)
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)

        status = hci1.enable_autogen_iso_packets(100)
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)

        _, status = hci1.get_iso_connection_stats()
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)

        pass

    def test_sniffer(self):
        # If the sniffer is disabled inside Cordio this will not return a LL_SUCCESS (lhci_cmd_vs.c)
        status = hci1.enable_sniffer_packet_forwarding(True)
        self.assertTrue(
            status == pc.StatusCode.LL_SUCCESS
            or status == pc.StatusCode.LL_ERROR_CODE_UNKNOWN_HCI_CMD
        )


if __name__ == "__main__":
    unittest.main()
