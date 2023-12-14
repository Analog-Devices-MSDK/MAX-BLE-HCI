import unittest
import secrets
from ble_hci import BleHci
from ble_hci import ble_hci
from ble_hci import packet_codes as pc
from ble_hci import packet_defs as pd

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"
hci = BleHci(PORT)

MAX_U32 = 0xFFFFFFFF
A32 = 0xAAAAAAAA


class TestHci(unittest.TestCase):
    def test_reset(self):
        # Reset puts code into nice condition, make sure it works before any tests
        self.assertEqual(hci.reset(), pc.StatusCode.LL_SUCCESS)

    def test_commands(self):
        hci.reset()

        self.assertEqual(hci.set_tx_test_err_pattern(A32), pc.StatusCode.LL_SUCCESS)
        self.assertIsNotNone(hci.set_connection_op_flags(1, MAX_U32, True))

        key = list(secrets.token_bytes(32))
        self.assertEqual(hci.set_256_priv_key(key), pc.StatusCode.LL_SUCCESS)
        self.assertEqual(
            hci.get_channel_map_periodic_scan_adv(1, False)[1], pc.StatusCode.LL_SUCCESS
        )
        self.assertIsNotNone(hci.get_acl_test_report())

        self.assertEqual(
            hci.set_local_num_min_used_channels(ble_hci.PhyOption.P1M, 0, 10),
            pc.StatusCode.LL_SUCCESS,
        )

        self.assertEqual(
            hci.get_peer_min_num_channels_used(1)[1],
            pc.StatusCode.LL_ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(
            hci.set_validate_pub_key_mode(pd.PubKeyValidateMode.ALT1),
            pc.StatusCode.LL_SUCCESS,
        )

        addr, status = hci.get_rand_address()
        self.assertTrue(len(addr) == 6 or status != pc.StatusCode.LL_SUCCESS)

        self.assertEqual(hci.set_local_feature(0), pc.StatusCode.LL_SUCCESS)

        self.assertEqual(hci.set_operational_flags(0, True), pc.StatusCode.LL_SUCCESS)

        self.assertEqual(
            hci.set_encryption_mode(1, True, True),
            pc.StatusCode.LL_ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(hci.set_diagnostic_mode(True), pc.StatusCode.LL_SUCCESS)

    def test_stats(self):
        stats, status = hci.get_pdu_filter_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci.get_memory_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci.get_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)
        stats, status = hci.get_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci.get_conn_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci.get_test_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci.get_aux_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

        stats, status = hci.get_aux_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)
        self.assertEqual(
            hci.set_connection_phy_tx_power(1, 0, ble_hci.PhyOption.P1M),
            pc.StatusCode.LL_ERROR_CODE_UNKNOWN_CONN_ID,
        )

        stats, status = hci.get_periodic_scanning_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.LL_SUCCESS)

    def test_iso(self):
        _, status = hci.get_iso_test_report()
        if status == pc.StatusCode.LL_DECODE_FAILURE:
            # ISO not enabled
            return

        status = hci.enable_iso_packet_sink(True)
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)

        status = hci.enable_autogen_iso_packets(100)
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)

        _, status = hci.get_iso_connection_stats()
        self.assertEqual(status, pc.StatusCode.LL_SUCCESS)

        pass

    def test_sniffer(self):
        # If the sniffer is disabled inside Cordio this will not return a LL_SUCCESS (lhci_cmd_vs.c)
        status = hci.enable_sniffer_packet_forwarding(True)
        self.assertTrue(
            status == pc.StatusCode.LL_SUCCESS
            or status == pc.StatusCode.LL_ERROR_CODE_UNKNOWN_HCI_CMD
        )
        if status == pc.StatusCode.LL_SUCCESS:
            self.assertEqual(
                hci.enable_sniffer_packet_forwarding(False), pc.StatusCode.LL_SUCCESS
            )


if __name__ == "__main__":
    unittest.main()
