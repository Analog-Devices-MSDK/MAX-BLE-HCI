import secrets
import unittest
import sys
import os

if os.path.exists("../"):
    sys.path.append("../")

from max_ble_hci import BleHci, utils
from max_ble_hci import packet_codes as pc
from max_ble_hci.constants import PhyOption, PubKeyValidateMode

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03NOCL-if00-port0"

hci1 = BleHci(PORT, id_tag="hci1", timeout=5)

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


    def test_utils(self):
        
        expected_fips1 = [170, 187, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_fips2 = [104, 101, 108, 108, 111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        fips1 = hci1._convert_fips197(0xAABB)
        fips2 = hci1._convert_fips197('hello')
        self.assertEqual(fips1, expected_fips1)
        self.assertEqual(fips2, expected_fips2)

        ans = utils.to_le_nbyte_list(0xAABB, 4)
        self.assertEqual(ans, [0xBB,0xAA, 0x00, 0x00])

        ans = utils.le_list_to_int(ans)
        self.assertEqual(ans, 0xAABB)


        good_data = [1,2,3,4]
        ans = utils.can_represent_as_bytes(good_data)
        self.assertTrue(ans)

        bad_data = [1,2009,3,4]
        ans = utils.can_represent_as_bytes(bad_data)
        self.assertFalse(ans)


        address = utils.convert_str_address('00:11:22:33:44:55')
        self.assertEqual(address, 0x001122334455)


        self.assertEqual(utils.bytes_needed_to_represent(0), 1)
        self.assertEqual(utils.bytes_needed_to_represent(1), 1)



        



if __name__ == "__main__":
    unittest.main()
