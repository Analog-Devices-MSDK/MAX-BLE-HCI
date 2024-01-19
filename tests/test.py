import secrets
import time
import unittest

from max_ble_hci import BleHci
from max_ble_hci import packet_codes as pc

from max_ble_hci.constants import PhyOption, PubKeyValidateMode

PORT = ""

hci1 = BleHci(PORT, id_tag="hci1")

MAX_U32 = 0xFFFFFFFF
A32 = 0xAAAAAAAA


class TestHci(unittest.TestCase):
    def test_reset(self):
        # Reset puts code into nice condition, make sure it works before any tests
        self.assertEqual(hci1.reset(), pc.StatusCode.SUCCESS)

    def test_commands(self):
        hci1.reset()

        self.assertEqual(hci1.set_tx_test_err_pattern(A32), pc.StatusCode.SUCCESS)
        self.assertIsNotNone(hci1.set_connection_op_flags(1, MAX_U32, True))

        key = list(secrets.token_bytes(32))
        self.assertEqual(hci1.set_256_priv_key(key), pc.StatusCode.SUCCESS)
        self.assertEqual(
            hci1.get_channel_map_periodic_scan_adv(1, False)[1],
            pc.StatusCode.SUCCESS,
        )
        self.assertIsNotNone(hci1.get_acl_test_report())

        self.assertEqual(
            hci1.set_local_num_min_used_channels(PhyOption.PHY_1M, 0, 10),
            pc.StatusCode.SUCCESS,
        )

        self.assertEqual(
            hci1.get_peer_min_num_channels_used(1)[1],
            pc.StatusCode.ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(
            hci1.set_validate_pub_key_mode(PubKeyValidateMode.ALT1),
            pc.StatusCode.SUCCESS,
        )

        addr, status = hci1.get_rand_address()

        self.assertTrue(addr > 0 or status != pc.StatusCode.SUCCESS)

        self.assertEqual(hci1.set_local_feature(0), pc.StatusCode.SUCCESS)

        self.assertEqual(hci1.set_operational_flags(0, True), pc.StatusCode.SUCCESS)

        self.assertEqual(
            hci1.set_encryption_mode(1, True, True),
            pc.StatusCode.ERROR_CODE_UNKNOWN_CONN_ID,
        )

        self.assertEqual(hci1.set_diagnostic_mode(True), pc.StatusCode.SUCCESS)

    def test_stats(self):
        stats, status = hci1.get_pdu_filter_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_memory_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)
        stats, status = hci1.get_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_conn_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_test_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_aux_adv_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)

        stats, status = hci1.get_aux_scan_stats()
        self.assertTrue(stats is not None and status == pc.StatusCode.SUCCESS)
        self.assertEqual(
            hci1.set_connection_phy_tx_power(1, 0, PhyOption.PHY_1M),
            pc.StatusCode.ERROR_CODE_UNKNOWN_CONN_ID,
        )


if __name__ == "__main__":
    unittest.main()
