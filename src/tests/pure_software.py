import secrets
import unittest
import sys
import os

from max_ble_hci import BleHci, utils
from max_ble_hci import packet_codes as pc
from max_ble_hci.constants import PhyOption, PubKeyValidateMode




class Software(unittest.TestCase):
   
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
