from enum import Enum


class Payload(Enum):
    """DTM Payload options"""

    PRBS9 = 0
    DF1 = 1
    DF2 = 2
    PRBS15 = 3
    ALL_1S = 4
    ALL_0S = 5
    HALF_ON_HALF_OFF = 6
    INV_DF1 = 7


# ADI_PAYLOAD_PRBS9 (0), ADI_PAYLOAD_11110000 (1),
# ADI_PAYLOAD_10101010 (2), ADI_PAYLOAD_PRBS15 (3),
# ADI_PAYLOAD_11111111 (4) ADI_PAYLOAD_00000000 (5),
# ADI_PAYLOAD_00001111 (6) and ADI_PAYLOAD_01010101 (7)


class PhyOption(Enum):
    """Available modulation rates"""

    PHY_1M = 0x1
    PHY_2M = 0x2
    PHY_CODED = 0x3
    PHY_CODED_S8 = 0x3
    PHY_CODED_S2 = 0x4
