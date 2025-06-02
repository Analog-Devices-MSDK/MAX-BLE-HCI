# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module defines HCI-specific data types.

This module defines custom data types for HCI packet
parameters. These data types are used by the decoder
to convert and format HCI packet parameter data.

"""
# pylint: skip-file
from __future__ import annotations
from enum import Enum, Flag
from typing import List


def _get_name(obj, dtype) -> str:
    if obj.name is not None:
        return obj.name
    names = []
    for val in dtype:
        if val in obj:
            names.append(val.name)
    return "|".join(names)


class hci_type:
    """
    Base HCI type.
    """

    @staticmethod
    def from_bytes(*args) -> hci_type:
        """Typecast bytes object.

        Parameters
        ----------
        *args
            Bytes object to typecast.

        Results
        -------
        hci_type
            Typecast object.

        """
        return hci_type()


class hci_int(hci_type):
    """
    HCI signed integer type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value}"

    @staticmethod
    def from_bytes(val: bytes) -> hci_int:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_int
            Typecast object.

        """
        return hci_int(int.from_bytes(val, byteorder="little", signed=True))


class hci_uint(hci_type):
    """
    HCI unsigned integer type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value}"

    @staticmethod
    def from_bytes(val: bytes) -> hci_uint:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_uint
            Typecast object.

        """
        return hci_uint(int.from_bytes(val, byteorder="little", signed=False))


class hci_hexint(hci_type):
    """
    HCI hex integer type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"0x{self.value:X}"

    @staticmethod
    def from_bytes(val: bytes) -> hci_hexint:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Returns
        -------
        hci_l2cap_hex
            Typecast object.

        """
        return hci_hexint(int.from_bytes(val, byteorder="little"))


class hci_str(hci_type):
    """
    HCI big-endian string type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value}"

    @staticmethod
    def from_bytes(val: bytes) -> hci_str:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_str
            Typecast object.

        """
        return hci_str(int.from_bytes(val, byteorder="big", signed=False))


class hci_hexstr(hci_type):
    """
    HCI big-endian hex string type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"0x{self.value:X}"

    @staticmethod
    def from_bytes(val: bytes) -> hci_hexstr:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_hexstr
            Typecast object.

        """
        return hci_hexstr(int.from_bytes(val, byteorder="big", signed=False))


class hci_bool(hci_type):
    """
    HCI boolean type.
    """

    def __init__(self, val: bool) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value}"

    @staticmethod
    def from_bytes(val: bytes) -> hci_bool:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_bool
            Typecast object.

        """
        return hci_bool(int.from_bytes(val, byteorder="little", signed=False) > 0)


class hci_time_1p28s(hci_type):
    """
    HCI time type with 1.28s units.
    """

    def __init__(self, val: float) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value} seconds"

    @staticmethod
    def from_bytes(val: bytes) -> hci_time_1p28s:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_time_1p28s
            Typecast object.

        """
        return hci_time_1p28s(
            int.from_bytes(val, byteorder="little", signed=False) * 1.28
        )


class hci_time_p625ms(hci_type):
    """
    HCI time type with 0.625ms units.
    """

    def __init__(self, val: float) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value} milliseconds"

    @staticmethod
    def from_bytes(val: bytes) -> hci_time_p625ms:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_time_p625ms
            Typecast object.

        """
        return hci_time_p625ms(
            int.from_bytes(val, byteorder="little", signed=False) * 0.625
        )


class hci_time_1p25ms(hci_type):
    """
    HCI time type with 1.25ms units.
    """

    def __init__(self, val: float) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value} milliseconds"

    @staticmethod
    def from_bytes(val: bytes) -> hci_time_1p25ms:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_time_1p25ms
            Typecast object.

        """
        return hci_time_1p25ms(
            int.from_bytes(val, byteorder="little", signed=False) * 1.25
        )


class hci_time_p125ms(hci_type):
    """
    HCI time type with 0.125ms units.
    """

    def __init__(self, val: float) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value} milliseconds"

    @staticmethod
    def from_bytes(val: bytes) -> hci_time_p125ms:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_time_p125ms
            Typecast object.

        """
        return hci_time_p125ms(
            int.from_bytes(val, byteorder="little", signed=False) * 0.125
        )


class hci_time_p3125ms(hci_type):
    """
    HCI time type with 0.3125ms units.
    """

    def __init__(self, val: float) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value} milliseconds"

    @staticmethod
    def from_bytes(val: bytes) -> hci_time_p3125ms:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_time_p3125ms
            Typecast object.

        """
        return hci_time_p3125ms(
            int.from_bytes(val, byteorder="little", signed=False) * 0.3125
        )


class hci_time_10ms(hci_type):
    """
    HCI time type with 10ms units.
    """

    def __init__(self, val: float) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"{self.value} milliseconds"

    @staticmethod
    def from_bytes(val: bytes) -> hci_time_10ms:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_time_10ms
            Typecast object.

        """
        return hci_time_10ms(
            int.from_bytes(val, byteorder="little", signed=False) * 10.0
        )


class hci_address(hci_type):
    """
    HCI address type.
    """

    def __init__(self, val: List[str]) -> None:
        self.value = val

    def __repr__(self) -> str:
        return ":".join(self.value)

    @staticmethod
    def from_bytes(val: bytes) -> hci_address:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_address
            Typecast object.

        """
        return hci_address([hex(x) for x in val])


class hci_packet_type(hci_type):
    """
    HCI packet type.
    """

    def __init__(self, val: int):
        to_mask = self._packet_type_mask(val)
        self.name = _get_name(to_mask, self._packet_type_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_packet_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_packet_type
            Typecast object.

        """
        return hci_packet_type(int.from_bytes(val, byteorder="little", signed=False))

    class _packet_type_mask(Flag):
        NO_2DH1 = 1 << 1
        NO_3DH1 = 1 << 2
        DM1_ALLOWED = 1 << 3
        DH1_ALLOWED = 1 << 4
        NO_2DH3 = 1 << 8
        NO_3DH3 = 1 << 9
        DM3_ALLOWED = 1 << 10
        DH3_ALLOWED = 1 << 11
        NO_2DH5 = 1 << 12
        NO_3DH5 = 1 << 13
        DM5_ALLOWED = 1 << 14
        DH5_ALLOWED = 1 << 15


class hci_sync_packet_type(hci_type):
    """
    HCI sync packet type type.
    """

    def __init__(self, val: int):
        to_mask = self._sync_packet_type_mask(val)
        self.name = _get_name(to_mask, self._sync_packet_type_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_sync_packet_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_sync_packet_type
            Typecast object.

        """
        return hci_sync_packet_type(
            int.from_bytes(val, byteorder="little", signed=False)
        )

    class _sync_packet_type_mask(Flag):
        HV1_ALLOWED = 1 << 0
        HV2_ALLOWED = 1 << 1
        HV3_ALLOWED = 1 << 2
        EV3_ALLOWED = 1 << 3
        EV4_ALLOWED = 1 << 4
        EV5_ALLOWED = 1 << 5
        NO_2EV3 = 1 << 6
        NO_3EV3 = 1 << 7
        NO_2EV5 = 1 << 8
        NO_3EV5 = 1 << 9


class hci_page_scan_repetition_mode(hci_type):
    """
    HCI page scan repetition mode type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return f"R{self.value}"

    @staticmethod
    def from_bytes(val: bytes) -> hci_page_scan_repetition_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_page_scan_repetition_mode
            Typecast object.

        """
        return hci_page_scan_repetition_mode(int.from_bytes(val, byteorder="little"))


class hci_clock_offset(hci_type):
    """
    HCI clock offset type.
    """

    def __init__(self, val: int) -> None:
        self.valid = val & 0x8000 > 0
        self.value = val & 0x7FFF

    def __repr__(self) -> str:
        return f"{self.value} ({'valid' if self.valid else 'invalid'})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_clock_offset:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_clock_offset
            Typecast object.

        """
        return hci_clock_offset(int.from_bytes(val, byteorder="little"))


class hci_status(hci_type):
    """
    HCI status type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._status_codes(val)
        self.name = to_mask.name
        self.value = to_mask.value
        self.name2 = None
        try:
            to_mask = self._status_codes_opt2(val)
            self.name2 = to_mask.name
        except ValueError:
            return

    def __repr__(self) -> str:
        if self.name2 is not None:
            return f"{self.name}/{self.name2} ({self.value})"
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_status:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_status
            Typecast object.

        """
        return hci_status(int.from_bytes(val, byteorder="little"))

    class _status_codes(Enum):
        SUCCESS = 0x00
        UNKNOWN_HCI_COMMAND = 0x01
        UNKNOWN_CONNECTION_IDENTIFIER = 0x02
        HARDWARE_FAILURE = 0x03
        PAGE_TIMEOUT = 0x04
        AUTHENTICATION_FAILURE = 0x05
        PIN_OR_KEY_MISSING = 0x06
        MEMORY_CAPACITY_EXCEEDED = 0x07
        CONNECTION_TIMEOUT = 0x08
        CONNECTION_LIMIT_EXCEEDED = 0x09
        SYNCHRONOUS_CONNECTION_LIMIT_TO_A_DEVICE_EXCEEDED = 0x0A
        CONNECTION_ALREADY_EXISTS = 0x0B
        COMMAND_DISALLOWED = 0x0C
        CONNECTION_REJECTED_DUE_TO_LIMITED_RESOURCES = 0x0D
        CONNECTION_REJECTED_DUE_TO_SECURITY_REASONS = 0x0E
        CONNECTION_REJECTED_DUE_TO_UNACCEPTABLE_BD_ADDR = 0x0F
        CONNECTION_ACCEPT_TIMEOUT_EXCEEDED = 0x10
        UNSUPPORTED_FEATURE_OR_PARAMETER_VALUE = 0x11
        INVALID_HCI_COMMAND_PARAMETERS = 0x12
        REMOTE_USER_TERMINATED_CONNECTION = 0x13
        REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_LOW_RESOURCES = 0x14
        REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_POWER_OFF = 0x15
        CONNECTION_TERMINATED_BY_LOCAL_HOST = 0x16
        REPEATED_ATTEMPTS = 0x17
        PAIRING_NOT_ALLOWED = 0x18
        UNKNOWN_LMP_PDU = 0x19
        UNSUPPORTED_REMOTE_FEATURE = 0x1A
        SCO_OFFSET_REJECTED = 0x1B
        SCO_INTERCAL_REJECTED = 0x1C
        SCO_AIR_MODE_REJECTED = 0x1D
        INVALID_LMP_PARAMETERS = 0x1E
        UNSPECIFIED_ERROR = 0x1F
        UNSUPPORTED_LMP_PARAMETER_VALUE = 0x20
        ROLE_CHANGE_NOT_ALLOWED = 0x21
        LMP_RESPONSE_TIMEOUT = 0x22
        LMP_ERROR_TRANSACTION_COLLISION = 0x23
        LMP_PDU_NOT_ALLOWED = 0x24
        ENCRYPTION_MODE_NOT_ACCEPTABLE = 0x25
        LINK_KEY_CANNOT_BE_CHANGED = 0x26
        REQUESTED_QOS_NOT_SUPPORTED = 0x27
        INSTANT_PASSED = 0x28
        PAIRING_WITH_UNIT_KEY_NOT_SUPPORTED = 0x29
        DIFFERENT_TRANSACTION_COLLISION = 0x2A
        QOS_UNACCEPTABLE_PARAMETER = 0x2C
        QOS_REJECTED = 0x2D
        CHANNEL_CLASSIFICATION_NOT_SUPPORTED = 0x2E
        INSUFFICIENT_SECURITY = 0x2F
        PARAMETER_OUT_OF_MANDATORY_RANGE = 0x30
        ROLE_SWITCH_PENDING = 0x32
        RESERVED_SLOT_VIOLATION = 0x34
        ROLE_SWITCH_FAILED = 0x35
        EXTENDED_INQUIRY_RESPONSE_TOO_LARGE = 0x36
        SECURE_SIMPLE_PAIRING_NOT_SUPPORTED_BY_HOST = 0x37
        HOST_BUSY_PAIRING = 0x38
        CONNECTION_REJECTED_DUE_TO_NO_SUITABLE_CHANNEL_FOUND = 0x39
        CONTROLLER_BUSY = 0x3A
        UNACCEPTABLE_CONNECTION_PARAMETERS = 0x3B
        ADVERTISING_TIMEOUT = 0x3C
        CONNECTION_TERMINATED_DUE_TO_MIC_FAILURE = 0x3D
        CONNECTION_FAILED_TO_BE_ESTABLISHED = 0x3E
        COARSE_CLOCK_ADJUSTMENT_REJECTED_BUT_WILL_TRY_TO_ADJUST_USING_CLOCK_DRAGGING = (
            0x40
        )
        TYPE0_SUBMAP_NOT_DEFINED = 0x41
        UNKNOWN_ADVERTISING_IDENTIFIER = 0x42
        LIMIT_REACHED = 0x43
        OPERATION_CANCELLED_BY_HOST = 0x44
        PACKET_TOO_LONG = 0x45
        TOO_LATE = 0x46
        TOO_EARLY = 0x47
        INSUFFICIENT_CHANNELS = 0x48

    class _status_codes_opt2(Enum):
        INVALID_LL_PARAMETERS = 0x1E
        UNSUPPORTED_LL_PARAMETER_VALUE = 0x20
        LL_RESPONSE_TIMEOUT = 0x22
        LL_PROCEDURE_COLLISION = 0x23
        SYNCHRONIZATION_TIMEOUT = 0x3E


class hci_data_status(hci_type):
    """
    HCI data status type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Data complete (0x00)"
        if self.value == 0x01:
            return "Data incomplete, more to come (0x01)"
        if self.value == 0x02:
            return "Data incomplete/truncated, no more to come (0x02)"
        return "Failed to receive an AUX_SYNC_SUBEVENT_IND/RSP PDU"

    @staticmethod
    def from_bytes(val: bytes) -> hci_data_status:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_data_status
            Typecast object.

        """
        return hci_data_status(int.from_bytes(val, byteorder="little"))


class hci_packet_status(hci_type):
    """
    HCI packet status type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "CRC Ok"
        if self.value == 0x01:
            return "CRC Not Ok, Length/CTETime fields used to determine sampling points"
        if self.value == 0x02:
            return "CRC Not Ok, position/length of CTE determined some other way"
        return "Insufficient resources to sample"

    @staticmethod
    def from_bytes(val: bytes) -> hci_packet_status:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_packet_status
            Typecast object.

        """
        return hci_packet_status(int.from_bytes(val, byteorder="little"))


class hci_tx_status(hci_type):
    """
    HCI TX status type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "AUX_SYNC_SUBEVENT_IND was transmitted"
        return "AUX_SYNC_SUBEVENT_IND was not transmitted"

    @staticmethod
    def from_bytes(val: bytes) -> hci_tx_status:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_tx_status
            Typecast object.

        """
        return hci_tx_status(int.from_bytes(val, byteorder="little"))


class hci_role(hci_type):
    """
    HCI role type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Central"
        return "Peripheral"

    @staticmethod
    def from_bytes(val: bytes) -> hci_role:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_role
            Typecast object.

        """
        return hci_role(int.from_bytes(val, byteorder="little"))


class hci_key_flag(hci_type):
    """
    HCI key flag type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Semi-permanent"
        return "Temporary"

    @staticmethod
    def from_bytes(val: bytes) -> hci_key_flag:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_key_flag
            Typecast object.

        """
        return hci_key_flag(int.from_bytes(val, byteorder="little"))


class hci_voice_setting(hci_type):
    """
    HCI voice setting type.
    """

    _AIR_CODING_FORMATS = ["CVSD", "u-law", "A-law", "transparent data"]
    _INPUT_SAMPLE_SIZES = ["8 bits", "16 bits"]
    _INPUT_DATA_FORMATS = [
        "1's complement",
        "2's complement",
        "sign/magnitude",
        "unsigned",
    ]
    _INPUT_CODING_FORMATS = ["linear", "u-law", "A-law", "RESERVED"]

    def __init__(self, val: int) -> None:
        self.air_coding_format = self._AIR_CODING_FORMATS[(val >> 0) & 0b0011]
        self.linear_pcm_bit_position = (val >> 2) & 0b0111
        self.input_sample_size = self._INPUT_SAMPLE_SIZES[(val >> 5) & 0b0001]
        self.input_data_format = self._INPUT_DATA_FORMATS[(val >> 6) & 0b0011]
        self.input_coding_format = self._INPUT_CODING_FORMATS[(val >> 8) & 0b0011]

    def __repr__(self) -> str:
        rstr = "\n"
        rstr += f"        Air_Coding_Format={self.air_coding_format}\n"
        rstr += f"        Linear_PCM_Bit_Position={self.linear_pcm_bit_position}\n"
        rstr += f"        Input_Sample_Size={self.input_sample_size}\n"
        rstr += f"        Input_Data_Format={self.input_data_format}\n"
        rstr += f"        Input_Coding_Format={self.input_coding_format}"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_voice_setting:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_voice_setting
            Typecast object.

        """
        return hci_voice_setting(int.from_bytes(val, byteorder="little"))


class hci_retransmission_effort(hci_type):
    """
    HCI retransmission effort type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "No retransmission"
        if self.value == 0x01:
            return "At least 1 retransmission, optimize for power consumption"
        if self.value == 0x02:
            return "At least 1 retransmission, optimize for link quality"
        return "Don't care"

    @staticmethod
    def from_bytes(val: bytes) -> hci_retransmission_effort:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_retransmission_effort
            Typecast object.

        """
        return hci_retransmission_effort(int.from_bytes(val, byteorder="little"))


class hci_codec(hci_type):
    """
    HCI codec type.
    """

    def __init__(self, val: int) -> None:
        coding_format = self._coding_formats((val >> 0) & 0xFF)
        self.company_id = None
        self.codec_id = None

        if coding_format == self._coding_formats.VENDOR_SPECIFIC:
            self.company_id = (val >> 8) & 0xFFFF
            self.codec_id = (val >> 24) & 0xFFFF

        self.coding_format_name = coding_format.name
        self.coding_format_value = coding_format.value

    def __repr__(self) -> str:
        rstr = f"{self.coding_format_name} ({self.coding_format_value})"
        if self.company_id is not None:
            rstr += f", company_id={self.company_id}"
        if self.codec_id is not None:
            rstr += f", codec_id={self.codec_id}"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_codec:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_codec
            Typecast object.

        """
        return hci_codec(int.from_bytes(val, byteorder="little"))

    class _coding_formats(Enum):
        U_LAW_LOG = 0x00
        A_LAW_LOG = 0x01
        CVSD = 0x02
        TRANSPARENT = 0x03
        LINEAR_PCM = 0x04
        M_SBC = 0x05
        LC3 = 0x06
        G_792A = 0x07
        VENDOR_SPECIFIC = 0xFF


class hci_coding_format(hci_type):
    """
    HCI coding format type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._coding_formats(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_coding_format:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_coding_format
            Typecast object.

        """
        return hci_coding_format(int.from_bytes(val, byteorder="little"))

    class _coding_formats(Enum):
        U_LAW_LOG = 0x00
        A_LAW_LOG = 0x01
        CVSD = 0x02
        TRANSPARENT = 0x03
        LINEAR_PCM = 0x04
        M_SBC = 0x05
        LC3 = 0x06
        G_792A = 0x07
        VENDOR_SPECIFIC = 0xFF


class hci_pcm_data_format(hci_type):
    """
    HCI PCM data format type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "N/A"
        if self.value == 0x01:
            return "1's complement"
        if self.value == 0x02:
            return "2's complement"
        if self.value == 0x03:
            return "Sign-magnitude"
        return "Unsigned"

    @staticmethod
    def from_bytes(val: bytes) -> hci_pcm_data_format:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_pcm_data_format
            Typecast object.

        """
        return hci_pcm_data_format(int.from_bytes(val, byteorder="little"))


class hci_io_capability(hci_type):
    """
    HCI I/O capability type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "DisplayOnly"
        if self.value == 0x01:
            return "DisplayYesNo"
        if self.value == 0x02:
            return "KeyboardOnly"
        return "NoInputNoOutput"

    @staticmethod
    def from_bytes(val: bytes) -> hci_io_capability:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_io_capability
            Typecast object.

        """
        return hci_io_capability(int.from_bytes(val, byteorder="little"))


class hci_oob_data_present(hci_type):
    """
    HCI OOB data present type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "OOB authentication data not present"
        if self.value == 0x01:
            return "P-192 OOB authentication data from remote device present"
        if self.value == 0x02:
            return "P-256 OOB authentication data from remote device present"
        if self.value == 0x03:
            return "P-192 and P-256 OOB authentication data from remote device present"
        return "--Invalid value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_oob_data_present:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_oob_data_present
            Typecast object.

        """
        return hci_oob_data_present(int.from_bytes(val, byteorder="little"))


class hci_authentication_requirements(hci_type):
    """
    HCI authentication requirements type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "MITM protection not required, no bonding"
        if self.value == 0x01:
            return "MITM protection required, no bonding"
        if self.value == 0x02:
            return "MITM protection not required, dedicated bonding"
        if self.value == 0x03:
            return "MITM protection required, dedicated bonding"
        if self.value == 0x04:
            return "MITM protection not required, general bonding"
        if self.value == 0x05:
            return "MITM protection required, general bonding"
        return "--Invalid value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_oob_data_present:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_authentication_requirements
            Typecast object.

        """
        return hci_oob_data_present(int.from_bytes(val, byteorder="little"))


class hci_bt_channel_map(hci_type):
    """
    HCI BR/EDR channel map type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._bt_channel_map(val)
        self.name = _get_name(to_mask, self._bt_channel_map)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_bt_channel_map:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_bt_channel_map
            Typecast object.

        """
        return hci_bt_channel_map(int.from_bytes(val, byteorder="little"))

    class _bt_channel_map(Flag):
        CH0 = 1 << 0
        CH1 = 1 << 1
        CH2 = 1 << 2
        CH3 = 1 << 3
        CH4 = 1 << 4
        CH5 = 1 << 5
        CH6 = 1 << 6
        CH7 = 1 << 7
        CH8 = 1 << 8
        CH9 = 1 << 9
        CH10 = 1 << 10
        CH11 = 1 << 11
        CH12 = 1 << 12
        CH13 = 1 << 13
        CH14 = 1 << 14
        CH15 = 1 << 15
        CH16 = 1 << 16
        CH17 = 1 << 17
        CH18 = 1 << 18
        CH19 = 1 << 19
        CH20 = 1 << 20
        CH21 = 1 << 21
        CH22 = 1 << 22
        CH23 = 1 << 23
        CH24 = 1 << 24
        CH25 = 1 << 25
        CH26 = 1 << 26
        CH27 = 1 << 27
        CH28 = 1 << 28
        CH29 = 1 << 29
        CH30 = 1 << 30
        CH31 = 1 << 31
        CH32 = 1 << 32
        CH33 = 1 << 33
        CH34 = 1 << 34
        CH35 = 1 << 35
        CH36 = 1 << 36
        CH37 = 1 << 37
        CH38 = 1 << 38
        CH39 = 1 << 39
        CH40 = 1 << 40
        CH41 = 1 << 41
        CH42 = 1 << 42
        CH43 = 1 << 43
        CH44 = 1 << 44
        CH45 = 1 << 45
        CH46 = 1 << 46
        CH47 = 1 << 47
        CH48 = 1 << 48
        CH49 = 1 << 49
        CH50 = 1 << 50
        CH51 = 1 << 51
        CH52 = 1 << 52
        CH53 = 1 << 53
        CH54 = 1 << 54
        CH55 = 1 << 55
        CH56 = 1 << 56
        CH57 = 1 << 57
        CH58 = 1 << 58
        CH59 = 1 << 59
        CH60 = 1 << 60
        CH61 = 1 << 61
        CH62 = 1 << 62
        CH63 = 1 << 63
        CH64 = 1 << 64
        CH65 = 1 << 65
        CH66 = 1 << 66
        CH67 = 1 << 67
        CH68 = 1 << 68
        CH69 = 1 << 69
        CH70 = 1 << 70
        CH71 = 1 << 71
        CH72 = 1 << 72
        CH73 = 1 << 73
        CH74 = 1 << 74
        CH75 = 1 << 75
        CH76 = 1 << 76
        CH77 = 1 << 77
        CH78 = 1 << 78
        CH79 = 1 << 79


class hci_ble_channel_map(hci_type):
    """
    HCI BLE channel map type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._ble_channel_map(val)
        self.name = _get_name(to_mask, self._ble_channel_map)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_ble_channel_map:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_ble_channel_map
            Typecast object.

        """
        return hci_ble_channel_map(int.from_bytes(val, byteorder="little"))

    class _ble_channel_map(Flag):
        CH0 = 1 << 0
        CH1 = 1 << 1
        CH2 = 1 << 2
        CH3 = 1 << 3
        CH4 = 1 << 4
        CH5 = 1 << 5
        CH6 = 1 << 6
        CH7 = 1 << 7
        CH8 = 1 << 8
        CH9 = 1 << 9
        CH10 = 1 << 10
        CH11 = 1 << 11
        CH12 = 1 << 12
        CH13 = 1 << 13
        CH14 = 1 << 14
        CH15 = 1 << 15
        CH16 = 1 << 16
        CH17 = 1 << 17
        CH18 = 1 << 18
        CH19 = 1 << 19
        CH20 = 1 << 20
        CH21 = 1 << 21
        CH22 = 1 << 22
        CH23 = 1 << 23
        CH24 = 1 << 24
        CH25 = 1 << 25
        CH26 = 1 << 26
        CH27 = 1 << 27
        CH28 = 1 << 28
        CH29 = 1 << 29
        CH30 = 1 << 30
        CH31 = 1 << 31
        CH32 = 1 << 32
        CH33 = 1 << 33
        CH34 = 1 << 34
        CH35 = 1 << 35
        CH36 = 1 << 36
        CH37 = 1 << 37
        CH38 = 1 << 38
        CH39 = 1 << 39


class hci_qos_service(hci_type):
    """
    HCI quality of service type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "No traffic"
        if self.value == 0x01:
            return "Best effort"
        if self.value == 0x02:
            return "Guarenteed"
        return "--Invalid value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_qos_service:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_qos_service
            Typecast object.

        """
        return hci_qos_service(int.from_bytes(val, byteorder="little"))


class hci_link_policy_settings(hci_type):
    """
    HCI link policy settings type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._link_policy_settings(val)
        self.name = _get_name(to_mask, self._link_policy_settings)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_link_policy_settings:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_link_policy_settings
            Typecast object.

        """
        return hci_link_policy_settings(int.from_bytes(val, byteorder="little"))

    class _link_policy_settings(Flag):
        NONE = 0
        ENABLE_ROLE_SWITCH = 1 << 0
        ENABLE_HOLD_MODE = 1 << 1
        ENABLE_SNIFF_MODE = 1 << 2


class hci_datapath(hci_type):
    """
    HCI datapath type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Output"
        if self.value == 0x01:
            return "Input"
        return "--Invalid value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_datapath:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_datapath
            Typecast object.

        """
        return hci_datapath(int.from_bytes(val, byteorder="little"))


class hci_event_mask(hci_type):
    """
    HCI controller event mask type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._event_mask(val)
        self.name = _get_name(to_mask, self._event_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_event_mask:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_event_mask
            Typecast object.

        """
        return hci_event_mask(int.from_bytes(val, byteorder="little"))

    class _event_mask(Flag):
        NONE = 0
        INQUIRY_COMPLETE = 1 << 0
        INQUIRY_RESULT = 1 << 1
        CONNETION_COMPLETE = 1 << 2
        CONNECTION_REQUEST = 1 << 3
        DISCONNECTION_COMPLETE = 1 << 4
        AUTHENTICATION_COMPLETE = 1 << 5
        REMOTE_NAME_REQUEST_COMPLETE = 1 << 6
        ENCRYPTION_CHANGE_V1 = 1 << 7
        CHANGE_CONNECTION_LINK_KEY_COMPLETE = 1 << 8
        LINK_KEY_TYPE_CHANGED = 1 << 9
        READ_REMOTE_SUPPORTED_FEATURES_COMPLETE = 1 << 10
        READ_REMOTE_VERSION_INFORMATION_COMPLETE = 1 << 11
        QOS_SETUP_COMPLETE = 1 << 12
        HARDWARE_ERROR = 1 << 15
        FLUSH_OCCURRED = 1 << 16
        ROLE_CHANGE = 1 << 17
        MODE_CHANGE = 1 << 19
        RETURN_LINK_KEYS = 1 << 20
        PIN_CODE_REQUEST = 1 << 21
        LINK_KEY_REQUEST = 1 << 22
        LINK_KEY_NOTIFICATION = 1 << 23
        LOOPBACK_COMMAND = 1 << 24
        DATA_BUFFER_OVERFLOW = 1 << 25
        MAX_SLOTS_CHANGE = 1 << 26
        READ_CLOCK_OFFSET_COMPLETE = 1 << 27
        CONNECTION_PACKET_TYPE_CHANGED = 1 << 28
        QOS_VIOLATION = 1 << 29
        PAGE_SCAN_REPETITION_MODE_CHANGE = 1 << 31
        FLOW_SPECIFICATION_COMPLETE = 1 << 32
        INQUIRY_RESULT_WITH_RSSI = 1 << 33
        READ_REMOTE_EXTENDED_FEATURES_COMPLETE = 1 << 34
        SYNCHRONOUS_CONNECTION_COMPLETE = 1 << 43
        SYNCHRONOUS_CONNECTION_CHANGED = 1 << 44
        SNIFF_SUBRATING = 1 << 45
        EXTENDED_INQUIRY_RESULT = 1 << 46
        ENCRYPTION_KEY_REFRESH_COMPLETE = 1 << 47
        IO_CAPABILITY_REQUEST = 1 << 48
        IO_CAPABILITY_RESPONSE = 1 << 49
        USER_CONFIRMATION_REQUEST = 1 << 50
        USER_PASSKEY_REQUEST = 1 << 51
        REMOTE_OOB_DATA_REQUEST = 1 << 52
        SIMPLE_PAIRING_COMPLETE = 1 << 53
        LINK_SUPERVISION_TIMEOUT_CHANGED = 1 << 55
        ENHANCED_FLUSH_COMPLETE = 1 << 56
        USER_PASSKEY_NOTIFICATION = 1 << 58
        KEYPRESS_NOTIFICATION = 1 << 59
        REMOTE_HOST_SUPPORTED_FEATURES_NOTIFICATION = 1 << 60
        LE_META = 1 << 61


class hci_event_mask_page_2(hci_type):
    """
    HCI controller event mask page 2 type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._event_mask_page_2(val)
        self.name = _get_name(to_mask, self._event_mask_page_2)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_event_mask_page_2:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_event_mask_page_2
            Typecast object.

        """
        return hci_event_mask_page_2(int.from_bytes(val, byteorder="little"))

    class _event_mask_page_2(Flag):
        NONE = 0
        NUMBER_OF_COMPLETED_DATA_BLOCKS = 1 << 8
        TRIGGERED_CLOCK_CAPTURE = 1 << 14
        SYNCHRONIZATION_TRAIN_COMPLETE = 1 << 15
        SYNCHRONIZATION_TRAIN_RECEIVED = 1 << 16
        CONNECTIONLESS_PERIPHERAL_BROADCAST_RECEIVE = 1 << 17
        CONNECTIONLESS_PERIPHERAL_BROADCAST_TIMEOUT = 1 << 18
        TRUNCATED_PAGE_COMPLETE = 1 << 19
        PERIPHERAL_PAGE_RESPONSE_TIMEOUT = 1 << 20
        CONNECTIONLESS_PERIPHERAL_BROADCAST_CHANNEL_MAP_CHANGE = 1 << 21
        INQUIRY_RESPONSE_NOTIFICATION = 1 << 22
        AUTHENTICATED_PAYLOAD_TIMEOUT_EXPIRED = 1 << 23
        SAM_STATUS_CHANGE = 1 << 24
        ENCRYPTION_CHANGE_V2 = 1 << 25


class hci_le_event_mask(hci_type):
    """
    HCI LE event mask type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._le_event_mask(val)
        self.name = _get_name(to_mask, self._le_event_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_le_event_mask:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_le_event_mask
            Typecast object.

        """
        return hci_le_event_mask(int.from_bytes(val, byteorder="little"))

    class _le_event_mask(Flag):
        LE_CONNECTION_COMPLETE = 1 << 0
        LE_ADVERTISING_REPORT = 1 << 1
        LE_CONNECTION_UPDATE_COMPLETE = 1 << 2
        LE_READ_REMOTE_FEATURES_PAGE_0_COMPLETE = 1 << 3
        LE_LONG_TERM_KEY_REQUEST = 1 << 4
        LE_REMOTE_CONNECTION_PARAMETER_REQUEST = 1 << 5
        LE_DATA_LENGTH_CHANGE = 1 << 6
        LE_READ_LOCAL_P256_PUBLIC_KEY_COMPLETE = 1 << 7
        LE_GENERATE_DKHEY_COMPLETE = 1 << 8
        LE_ENHANCED_CONNECTION_COMPLETE_V1 = 1 << 9
        LE_DIRECTED_ADVERTISING_REPORT = 1 << 10
        LE_PHY_UPDATE_COMPLETE = 1 << 11
        LE_EXTENDED_ADVERTISING_REPORT = 1 << 12
        LE_PERIODIC_ADVERTISING_SYNC_ESTABLISHED_V1 = 1 << 13
        LE_PERIODIC_ADVERTISING_REPORT_V1 = 1 << 14
        LE_PERIODIC_ADVERTISING_SYNC_LOST = 1 << 15
        LE_SCAN_TIMEOUT = 1 << 16
        LE_ADVERTISING_SET_TERMINATED = 1 << 17
        LE_SCAN_REQUEST_RECEIVED = 1 << 18
        LE_CHANNEL_SELECTION_ALGORITHM = 1 << 19
        LE_CONNECTIONLESS_IQ_REPORT = 1 << 20
        LE_CONNECTION_IQ_REPORT = 1 << 21
        LE_CTE_REQUEST_FAILED = 1 << 22
        LE_PERIODIC_ADVERTISING_SYNC_TRANSFER_RECEIVED_V1 = 1 << 23
        LE_CIS_ESTABLISHED_V1 = 1 << 24
        LE_CIS_REQUEST = 1 << 25
        LE_CREATE_BIG_COMPLETE = 1 << 26
        LE_TERMINATE_BIG_COMPLETE = 1 << 27
        LE_BIG_SYNC_ESTABLISHED = 1 << 28
        LE_BIG_SYNC_LOST = 1 << 29
        LE_REQUEST_PEER_SCA_COMPLETE = 1 << 30
        LE_PATH_LOSS_THRESHOLD = 1 << 31
        LE_TRANSMIT_POWER_REPORTING = 1 << 32
        LE_BIGINFO_ADVERTISING_REPORT = 1 << 33
        LE_SUBRATE_CHANGE = 1 << 34
        LE_PERIODIC_ADVERTISING_SYNC_ESTABLISHED_V2 = 1 << 35
        LE_PERIODIC_ADVERTISING_REPORT_V2 = 1 << 36
        LE_PERIODIC_ADVERTISING_SYNC_TRANSFER_RECEIVED_V2 = 1 << 37
        LE_PERIODIC_ADVERTISING_SUBEVENT_DATA_REQUEST = 1 << 38
        LE_PERIODIC_ADVERTISING_RESPONSE_REPORT = 1 << 39
        LE_ENHANCED_CONNECTION_COMPLETE_V2 = 1 << 40
        LE_CIS_ESTABLISHED_V2 = 1 << 41
        LE_READ_ALL_REMOTE_FEATURES_COMPLETE = 1 << 42
        LE_CS_READ_REMOTE_SUPORTED_CAPABILITIES_COMPLETE = 1 << 43
        LE_CS_READ_REMOTE_FAE_TABLE_COMPLETE = 1 << 44
        LE_CS_SECURITY_ENABLE_COMPLETE = 1 << 45
        LE_CS_CONFIG_COMPLETE = 1 << 46
        LE_CS_PROCEDURE_ENABLE_COMPLETE = 1 << 47
        LE_CS_SUBEVENT_RESULT = 1 << 48
        LE_CS_SUBEVENT_RESULT_CONTINUE = 1 << 49
        LE_CS_TEST_END_COMPLETE = 1 << 50
        LE_MONITORED_ADVERTISERS_REPORT = 1 << 51
        LE_FRAME_SPACE_UPDATE_COMPLETE = 1 << 52


class hci_event_filter(hci_type):
    """
    HCI event filter type.
    """

    def __init__(
        self, filter_type: int, condition_type: int, condition: List[int]
    ) -> None:
        self.filter_type = self._filter_types(filter_type)
        self.condition_type = self._condition_types(condition_type)
        self.condition = condition

    def __repr__(self) -> str:
        rstr = "\n"
        rstr = (
            f"        FilterType={self.filter_type.name} ({self.filter_type.value})\n"
        )
        if self.filter_type == self._filter_types.CLEAR:
            return rstr
        rstr += f"        ConditionType={self.condition_type.name} ({self.condition_type.value})\n"
        if self.filter_type == self._filter_types.INQUIRY_RESULT:
            if self.condition_type == self._condition_types.ALL_DEVICES:
                return rstr
            rstr += f"        Condition:\n"
            if self.condition_type == self._condition_types.CLASS_OF_DEVICE:
                rstr += f"            ClassOfDevice={self.condition[0]}\n"
                rstr += f"            ClassOfDeviceMask={self.condition[1]}"
            elif self.condition_type == self._condition_types.BD_ADDR:
                rstr += f"        Condition:\n"
                rstr += f"            BD_ADDR={self.condition[0]}"
        elif self.filter_type == self._filter_types.CONNECTION_SETUP:
            if self.condition_type == self._condition_types.ALL_DEVICES:
                rstr += f"        Condition:\n"
                rstr += f"            AutoAcceptFlag={self.condition[0]}"
            elif self.condition_type == self._condition_types.CLASS_OF_DEVICE:
                rstr += f"        Condition:\n"
                rstr += f"            ClassOfDevice={self.condition[0]}\n"
                rstr += f"            ClassOfDeviceMask={self.condition[1]}\n"
                rstr += f"            AutoAcceptFlag={self.condition[2]}"
            elif self.condition_type == self._condition_types.BD_ADDR:
                rstr += f"        Condition:\n"
                rstr += f"            BD_ADDR={self.condition[0]}\n"
                rstr += f"            AutoAcceptFlag={self.condition[1]}"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_event_filter:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_event_filter
            Typecast object.

        """
        filter_type = int.from_bytes(val[0], byteorder="little")
        if filter_type == 0x00:
            return hci_event_filter(filter_type, None, None)
        condition_type = int.from_bytes(val[1], byteorder="little")
        condition = []
        if filter_type == 0x01:
            if condition_type == 0x00:
                return hci_event_filter(filter_type, condition_type, None)
            if condition_type == 0x01:
                condition.append(int.from_bytes(val[2:5], byteorder="little"))
                condition.append(int.from_bytes(val[5:], byteorder="little"))
            elif condition_type == 0x02:
                condition.append(int.from_bytes(val[2:], byteorder="little"))
            return hci_event_filter(filter_type, condition_type, condition)
        if filter_type == 0x02:
            if condition_type == 0x00:
                condition.append(int.from_bytes(val[2], byteorder="little"))
            elif condition_type == 0x01:
                condition.append(int.from_bytes(val[2:5], byteorder="little"))
                condition.append(int.from_bytes(val[5:8], byteorder="little"))
                condition.append(int.from_bytes(val[8], byteorder="little"))
            elif condition_type == 0x02:
                condition.append(int.from_bytes(val[2:8], byteorder="little"))
                condition.append(int.from_bytes(val[8], byteorder="little"))
            return hci_event_filter(filter_type, condition_type, condition)
        return hci_event_filter(filter_type, condition_type, condition)

    class _filter_types(Enum):
        CLEAR = 0x00
        INQUIRY_RESULT = 0x01
        CONNECTION_SETUP = 0x02

    class _condition_types(Enum):
        ALL_DEVICES = 0x00
        CLASS_OF_DEVICE = 0x01
        BD_ADDR = 0x02


class hci_scan_enable(hci_type):
    """
    HCI scan enable type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._scan_enable(val)
        self.name = _get_name(to_mask, self._scan_enable)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_scan_enable:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_scan_enable
            Typecast object.

        """
        return hci_scan_enable(int.from_bytes(val, byteorder="little"))

    class _scan_enable(Flag):
        INQUIRY_SCAN = 1 << 0
        PAGE_SCAN = 1 << 1


class hci_hold_mode_activity(hci_type):
    """
    HCI hold mode activity type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Maintain current power state (0x00)"
        if self.value == 0x01:
            return "Suspend page scan (0x01)"
        if self.value == 0x02:
            return "Suspend inquiry scan (0x02)"
        if self.value == 0x04:
            return "Suspend periodic inquiries (0x04)"
        return "--Invalid value--"

    @staticmethod
    def from_bytes(val: int) -> hci_hold_mode_activity:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_hold_mode_activity
            Typecast object.

        """
        return hci_hold_mode_activity(int.from_bytes(val, byteorder="little"))


class hci_flow_control_enable(hci_type):
    """
    HCI flow control enable type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._flow_control_enable(val)
        self.name = _get_name(to_mask, self._flow_control_enable)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_flow_control_enable:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_flow_control_enable
            Typecast object.

        """
        return hci_flow_control_enable(int.from_bytes(val, byteorder="little"))

    class _flow_control_enable(Flag):
        NO_FLOW_CONTROL = 0
        ACL_FLOW_CONTROL = 1 << 0
        SYNC_FLOW_CONTROL = 1 << 1


class hci_flow_control_mode(hci_type):
    """
    HCI flow control mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._flow_control_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_flow_control_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_flow_control_mode
            Typecast object.

        """
        return hci_flow_control_mode(int.from_bytes(val, byteorder="little"))

    class _flow_control_mode(Enum):
        PACKET_BASED = 0x00
        DATABLOCK_BASED = 0x01


class hci_scan_mode(hci_type):
    """
    HCI scan mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._scan_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_scan_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_scan_mode
            Typecast object.

        """
        return hci_scan_mode(int.from_bytes(val, byteorder="little"))

    class _scan_mode(Enum):
        STANDARD = 0x00
        INTERLACED = 0x01


class hci_inquiry_mode(hci_type):
    """
    HCI inquiry mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._inquiry_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_inquiry_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_inquiry_mode
            Typecast object.

        """
        return hci_inquiry_mode(int.from_bytes(val, byteorder="little"))

    class _inquiry_mode(Enum):
        STANDARD = 0x00
        INQUIRY_RESULT_WITH_RSSI = 0x01
        EXTENDED_INQUIRY_RESULT = 0x02


class hci_keypress_notification(hci_type):
    """
    HCI keypress notification type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._keypress_notification(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_keypress_notification:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_keypress_notification
            Typecast object.

        """
        return hci_keypress_notification(int.from_bytes(val, byteorder="little"))

    class _keypress_notification(Enum):
        PASSKEY_ENTRY_STARTED = 0x00
        PASSKEY_DIGIT_ENTERED = 0x01
        PASSKEY_DIGIT_ERASED = 0x02
        PASSKEY_CLEARED = 0x03
        PASSKEY_ENTRY_COMPLETED = 0x04


class hci_power_read_mode(hci_type):
    """
    HCI power read mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._power_read_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_power_read_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_power_read_mode
            Typecast object.

        """
        return hci_power_read_mode(int.from_bytes(val, byteorder="little"))

    class _power_read_mode(Enum):
        CURRENT = 0x00
        MAXIMUM = 0x01


class hci_mws_channel_type(hci_type):
    """
    HCI MWS channel type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._mws_channel_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_mws_channel_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_mws_channel_type
            Typecast object.

        """
        return hci_mws_channel_type(int.from_bytes(val, byteorder="little"))

    class _mws_channel_type(Enum):
        TDD = 0x00
        FDD = 0x01


class hci_mws_period_type(hci_type):
    """
    HCI MWS period type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._mws_period_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_mws_period_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_mws_period_type
            Typecast object.

        """
        return hci_mws_period_type(int.from_bytes(val, byteorder="little"))

    class _mws_period_type(Enum):
        DOWNLINK = 0x00
        UPLINK = 0x01
        BI_DIRECTIONAL = 0x02
        GUARD_PERIOD = 0x03


class hci_mws_transport_layer(hci_type):
    """
    HCI MWS transport layer type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._mws_transport_layer(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_mws_transport_layer:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_mws_transport_layer
            Typecast object.

        """
        return hci_mws_transport_layer(int.from_bytes(val, byteorder="little"))

    class _mws_transport_layer(Enum):
        DISABLED = 0x00
        WCI_1 = 0x01
        WCI_2 = 0x02


class hci_mws_pattern_interval_type(hci_type):
    """
    HCI MWS pattern interval type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._mws_pattern_interval_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_mws_pattern_interval_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_mws_pattern_interval_type
            Typecast object.

        """
        return hci_mws_pattern_interval_type(int.from_bytes(val, byteorder="little"))

    class _mws_pattern_interval_type(Enum):
        NO_TX_OR_RX = 0x00
        TX_ALLOWED = 0x01
        RX_ALLOWED = 0x02
        TX_AND_RX_ALLOWED = 0x03
        USE_EXTERNAL_FRAM_CONFIGURATION = 0x04


class hci_fragment(hci_type):
    """
    HCI fragment type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._fragment_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_fragment:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_fragment
            Typecast object.

        """
        return hci_fragment(int.from_bytes(val, byteorder="little"))

    class _fragment_type(Enum):
        CONTINUATION_FRAGMENT = 0x00
        STARTING_FRAGMENT = 0x01
        ENDING_FRAGMENT = 0x02
        NO_FRAGMENTATION = 0x03
        DATA_UNCHANGED = 0x04


class hci_logical_transport_type(hci_type):
    """
    HCI logical transport type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._logical_transport_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_logical_transport_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_logical_transport_type
            Typecast object.

        """
        return hci_logical_transport_type(int.from_bytes(val, byteorder="little"))

    class _logical_transport_type(Enum):
        BT_ACL = 0x00
        BT_SCO = 0x01
        BLE_CIS = 0x02
        BLE_DIS = 0x03


class hci_clock_select(hci_type):
    """
    HCI clock select type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._clock_select(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_clock_select:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_clock_select
            Typecast object.

        """
        return hci_clock_select(int.from_bytes(val, byteorder="little"))

    class _clock_select(Enum):
        LOCAL_CLOCK = 0x00
        PICONET_CLOCK = 0x01


class hci_loopback_mode(hci_type):
    """
    HCI loopback mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._loopback_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_loopback_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_loopback_mode
            Typecast object.

        """
        return hci_loopback_mode(int.from_bytes(val, byteorder="little"))

    class _loopback_mode(Enum):
        LOOPBACK_DISABLED = 0x00
        LOCAL_LOOPBACK_ENABLED = 0x01
        REMOTE_LOOPBACK_ENABLED = 0x02


class hci_advertising_type(hci_type):
    """
    HCI advertising type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._advertising_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_advertising_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_advertising_type
            Typecast object.

        """
        return hci_advertising_type(int.from_bytes(val, byteorder="little"))

    class _advertising_type(Enum):
        ADV_IND = 0x00
        HIGH_DUTY_CYCLE = 0x01
        ADV_SCAN_IND = 0x02
        ADV_NONCONN_IND = 0x03
        LOW_DUTY_CYCLE = 0x04


class hci_advertising_event_type(hci_type):
    """
    HCI advertising event type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._advertising_event_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: int) -> hci_advertising_event_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_advertising_event_type
            Typecast object.

        """
        return hci_advertising_event_type(int.from_bytes(val, byteorder="little"))

    class _advertising_event_type(Enum):
        ADV_IND = 0x00
        ADV_DIRECT_IND = 0x01
        ADV_SCAN_IND = 0x02
        ADV_NONCONN_IND = 0x03
        SCAN_RSP = 0x04


class hci_ext_advertising_event_type(hci_type):
    """
    HCI extended advertising event type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._ext_advertising_event_type(val & 0x1F)
        self.name = _get_name(to_mask, self._ext_advertising_event_type)
        self.value = to_mask.value
        self.data_status = (val >> 5) & 0x03

    def __repr__(self) -> str:
        rstr = "\n"
        if self.data_status == 0x00:
            rstr += f"        {self.name} ({self.value})\n"
            rstr += "        DataStatus=Complete"
            return rstr
        if self.data_status == 0x01:
            rstr += f"        {self.name} ({self.value})\n"
            rstr += "        DataStatus=Incomplete/Continuing"
            return rstr
        if self.data_status == 0x02:
            rstr += f"        {self.name} ({self.value})\n"
            rstr += "        DataStatus=Incomplete/Truncated"
            return rstr
        rstr += f"        {self.name} ({self.value})\n"
        rstr += "        --Invalid DataStatus--"
        return rstr

    @staticmethod
    def from_bytes(val: int) -> hci_ext_advertising_event_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_ext_advertising_event_type
            Typecast object.

        """
        return hci_ext_advertising_event_type(int.from_bytes(val, byteorder="little"))

    class _ext_advertising_event_type(Flag):
        CONNECTABLE = 1 << 0
        SCANNABLE = 1 << 1
        DIRECTED = 1 << 2
        SCAN_RSP = 1 << 3
        LEGACY_PDU = 1 << 4


class hci_address_type(hci_type):
    """
    HCI address type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._address_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_address_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_address_type
            Typecast object.

        """
        return hci_address_type(int.from_bytes(val, byteorder="little"))

    class _address_type(Enum):
        PUBLIC_DEVICE_ADDRESS = 0x00
        RANDOM_DEVICE_ADDRESS = 0x01
        PUBLIC_IDENTITY_ADDRESS = 0x02
        RANDOM_IDENTITY_ADDRESS = 0x03


class hci_advertising_channel_map(hci_type):
    """
    HCI advertising channel map type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._advertising_channel_map(val)
        self.name = _get_name(to_mask, self._advertising_channel_map)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_advertising_channel_map:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_advertising_channel_map
            Typecast object.

        """
        return hci_advertising_channel_map(int.from_bytes(val, byteorder="little"))

    class _advertising_channel_map(Flag):
        CH37 = 1 << 0
        CH38 = 1 << 1
        CH39 = 1 << 2


class hci_advertising_filter_policy(hci_type):
    """
    HCI advertising filter policy type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._advertising_filter_policy(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_advertising_filter_policy:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_advertising_filter_policy
            Typecast object.

        """
        return hci_advertising_filter_policy(int.from_bytes(val, byteorder="little"))

    class _advertising_filter_policy(Enum):
        FILTER_ACCEPT_LIST_NOT_IN_USE = 0x00
        FILTER_CONNECTION_REQUESTS = 0x01
        FILTER_SCAN_REQUESTS = 0x02
        FILTER_CONNECTION_AND_SCAN_REQUESTS = 0x03


class hci_scan_filter_policy(hci_type):
    """
    HCI scan filter policy type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._scan_filter_policy(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_scan_filter_policy:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_scan_filter_policy
            Typecast object.

        """
        return hci_scan_filter_policy(int.from_bytes(val, byteorder="little"))

    class _scan_filter_policy(Enum):
        BASIC_UNFILTERED = 0x00
        BASIC_FILTERED = 0x01
        EXTENDED_UNFILTERED = 0x02
        EXTENDED_FILTERED = 0x03
        BASIC_UNFILTERED_ALL_PDUS = 0x04
        BASIC_FILTERED_ALL_PDUS = 0x05
        EXTENDED_UNFILTERED_ALL_PDUS = 0x06
        EXTENDED_FILTERED_ALL_PDUS = 0x07
        BASIC_UNFILTERED_DECISIONS_ONLY = 0x0C
        BASIC_FILTERED_DECISIONS_ONLY = 0x0D
        EXTENDED_UNFILTERED_DECISIONS_ONLY = 0x0E
        EXTENDED_FILTERED_DECISIONS_ONLY = 0x0F


class hci_le_scan_type(hci_type):
    """
    HCI LE scan type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._le_scan_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_le_scan_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_le_scan_type
            Typecast object.

        """
        return hci_le_scan_type(int.from_bytes(val, byteorder="little"))

    class _le_scan_type(Enum):
        PASSIVE_SCANNING = 0x00
        ACTIVE_SCANNING = 0x01


class hci_packet_payload(hci_type):
    """
    HCI packet payload type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._packet_payload(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_packet_payload:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_packet_payload
            Typecast object.

        """
        return hci_packet_payload(int.from_bytes(val, byteorder="little"))

    class _packet_payload(Enum):
        PLD_PRBS9 = 0x00
        PLD_11110000 = 0x01
        PLD_10101010 = 0x02
        PLD_PRBS15 = 0x03
        PLD_11111111 = 0x04
        PLD_00000000 = 0x05
        PLD_00001111 = 0x06
        PLD_01010101 = 0x07


class hci_phy_mask(hci_type):
    """
    HCI PHY mask type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._phy_mask(val)
        self.name = _get_name(to_mask, self._phy_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_phy_mask:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_phy_mask
            Typecast object.

        """
        return hci_phy_mask(int.from_bytes(val, byteorder="little"))

    class _phy_mask(Flag):
        LE_1M = 1 << 0
        LE_2M = 1 << 1
        LE_CODED = 1 << 2


class hci_phy_options(hci_type):
    """
    HCI PHY options type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._phy_options(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_phy_options:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_phy_options
            Typecast object.

        """
        return hci_phy_options(int.from_bytes(val, byteorder="little"))

    class _phy_options(Enum):
        NO_PREFERENCE = 0x00
        S2_PREFERRED = 0x01
        S8_PREFERRED = 0x02
        S2_REQUIRED = 0x03
        S8_REQUIRED = 0x03


class hci_phy_preference(hci_type):
    """
    HCI PHY preference type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._phy_preference(val)
        self.name = _get_name(to_mask, self._phy_preference)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_phy_preference:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_phy_preference
            Typecast object.

        """
        return hci_phy_preference(int.from_bytes(val, byteorder="little"))

    class _phy_preference(Flag):
        NO_TX_PREFERENCE = 1 << 0
        NO_RX_PREFERENCE = 1 << 1


class hci_phy_select(hci_type):
    """
    HCI PHY select type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._phy_select(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_phy_select:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_phy_select
            Typecast object.

        """
        return hci_phy_select(int.from_bytes(val, byteorder="little"))

    class _phy_select(Enum):
        LE_1M = 0x01
        LE_2M = 0x02
        LE_CODED_S8 = 0x03
        LE_CODED_S2 = 0x04


class hci_advertising_event_properties(hci_type):
    """
    HCI advertising event properties type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._advertising_event_properties(val)
        self.name = _get_name(to_mask, self._advertising_event_properties)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_advertising_event_properties:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_advertising_event_properties
            Typecast object.

        """
        return hci_advertising_event_properties(int.from_bytes(val, byteorder="little"))

    class _advertising_event_properties(Flag):
        CONNECTABLE = 1 << 0
        SCANNABLE = 1 << 1
        DIRECTED = 1 << 2
        HIGH_DUTY_CYCLE = 1 << 3
        USES_LEGACY_PDUS = 1 << 4
        ANONYMOUS = 1 << 5
        INCLUDES_TX_POWER = 1 << 6
        USES_DECISION_PDUS = 1 << 7
        INCLUDES_ADVA = 1 << 8
        INCLUDES_ADI = 1 << 9


class hci_fragment_preference(hci_type):
    """
    HCI fragment preference type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._fragment_preference(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_fragment_preference:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_fragment_preference
            Typecast object.

        """
        return hci_fragment_preference(int.from_bytes(val, byteorder="little"))

    class _fragment_preference(Enum):
        NO_RESTRICTIONS = 0x00
        MINIMIZE_FRAGMENTATION = 0x01


class hci_periodic_advertising_mode(hci_type):
    """
    HCI periodic advertising mode type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "No synchronization attempt made (0x00)"
        if self.valye == 0x01:
            return "SyncTransferRcvd sent, AdvReports disabled (0x01)"
        if self.value == 0x02:
            return "SyncTransferRcvd sent, AdvReports enabled, DuplicatedFiltering disabled"
        if self.value == 0x03:
            return (
                "SyncTransferRcvd sent, AdvReports enabled, DuplicatedFiltering enabled"
            )

    @staticmethod
    def from_bytes(val: bytes) -> hci_periodic_advertising_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_periodic_advertising_mode
            Typecast object.

        """
        return hci_periodic_advertising_mode(int.from_bytes(val, byteorder="little"))


class hci_periodic_advertising_properties(hci_type):
    """
    HCI periodic advertising properties type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._periodic_advertising_properties(val)
        self.name = _get_name(to_mask, self._periodic_advertising_properties)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_periodic_advertising_properties:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_periodic_advertising_properties
            Typecast object.

        """
        return hci_periodic_advertising_properties(
            int.from_bytes(val, byteorder="little")
        )

    class _periodic_advertising_properties(Flag):
        INCLUDE_TX_POWER = 1 << 6


class hci_connection_filter_policy(hci_type):
    """
    HCI connection filter policy type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        rstr = "\n"
        if self.value == 0x00:
            rstr += "        Filter Accept List is not used to determine connections\n"
            rstr += "        Decision PDUs are ignored\n"
            rstr += "        Peer Address Type and Peer Address are used (0x00)"
        elif self.value == 0x01:
            rstr += "        Filter Accept List is used to determine connections\n"
            rstr += "        Decision PDUs are ignored\n"
            rstr += "        Peer Address Type and Peer Address are ignored (0x01)"
        elif self.value == 0x02:
            rstr += "        Filter Accept List is not used to determine connections\n"
            rstr += "        Only Decision PDUs are processed\n"
            rstr += "        Peer Address Type and Peer Address are ignored (0x02)"
        elif self.value == 0x03:
            rstr += "        Filter Accept List is used to determine connections\n"
            rstr += "        All PDUs are processed\n"
            rstr += "        Peer Address Type and Peer Address are ignored (0x03)"
        elif self.value == 0x04:
            rstr += "        All decision PDUs are processed\n"
            rstr += "        Filter Accept List is used to determine others PDUs to process\n"
            rstr += "        Peer Address Type and Peer Address are ignored (0x04)"
        else:
            rstr += "--Invalid Value--"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_connection_filter_policy:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_connection_filter_policy
            Typecast object.

        """
        return hci_connection_filter_policy(int.from_bytes(val, byteorder="little"))


class hci_sync_options(hci_type):
    """
    HCI sync options type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        rstr = ""
        if self.value & (1 << 0) == 0:
            rstr += "Listen based on advertiser info, "
        else:
            rstr += "Listen based on Periodic Advertiser List, "

        if self.value & (1 << 1) == 0:
            rstr += "enable reporting, "
        else:
            rstr += "disable reporting, "

        if self.value & (1 << 2) == 0:
            rstr += "disable duplicate filtering"
        else:
            rstr += "enable duplicate filtering"

        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_sync_options:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_sync_options
            Typecast object.

        """
        return hci_sync_options(int.from_bytes(val, byteorder="little"))


class hci_sync_cte_type(hci_type):
    """
    HCI sync CTE type type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        aoa_cte = "y" if self.value & (1 << 0) == 0 else "n"
        aod_cte_1us = "y" if self.value & (1 << 1) == 0 else "n"
        aod_cte_2us = "y" if self.value & (1 << 2) == 0 else "n"
        type3_cte = "y" if self.value & (1 << 3) == 0 else "n"
        cte_required = "n" if self.value & (1 << 4) == 0 else "y"

        rstr = "\n"
        rstr += f"        Sync w/ AoA CTE       -> {aoa_cte}\n"
        rstr += f"        Sync w/ AoD CTE (1us) -> {aod_cte_1us}\n"
        rstr += f"        Sync w/ AoD CTE (2us) -> {aod_cte_2us}\n"
        rstr += f"        Sync w/ Type3 CTE     -> {type3_cte}\n"
        rstr += f"        CTE required for sync -> {cte_required}"

        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_sync_cte_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_sync_cte_type
            Typecast object.

        """
        return hci_sync_cte_type(int.from_bytes(val, byteorder="little"))


class hci_privacy_mode(hci_type):
    """
    HCI privacy mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._privacy_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_privacy_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_privacy_mode
            Typecast object.

        """
        return hci_privacy_mode(int.from_bytes(val, byteorder="little"))

    class _privacy_mode(Enum):
        NETWORK_PRIVACY_MODE = 0x00
        DEVICE_PRIVACY_MODE = 0x01


class hci_cte_type_select(hci_type):
    """
    HCI CTE type select type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cte_type_select(val)
        self.name = _get_name(to_mask, self._cte_type_select)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cte_type_select:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cte_type_select
            Typecast object.

        """
        return hci_cte_type_select(int.from_bytes(val, byteorder="little"))

    class _cte_type_select(Flag):
        AOA_CTE = 0x00
        AOD_CTE_1US = 0x01
        AOD_CTE_2US = 0x02
        NO_CTE = 0xFF


class hci_cte_type_mask(hci_type):
    """
    HCI CTE type mask type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cte_type_mask(val)
        self.name = _get_name(to_mask, self._cte_type_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cte_type_mask:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cte_type_mask
            Typecast object.

        """
        return hci_cte_type_mask(int.from_bytes(val, byteorder="little"))

    class _cte_type_mask(Flag):
        AOA_CTE = 1 << 0
        AOD_CTE_1US = 1 << 1
        AOD_CTE_2US = 1 << 2


class hci_dh_key_type(hci_type):
    """
    HCI DHKey type type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Generated"
        if self.value == 0x01:
            return "Debug"
        return "--Invalid Value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_dh_key_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_dh_key_type
            Typecast object.

        """
        return hci_dh_key_type(int.from_bytes(val, byteorder="little"))


class hci_sleep_clock_action(hci_type):
    """
    HCI sleep clock action type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Switch to a more accurate clock"
        if self.value == 0x01:
            return "Switch to a less accurate clock"
        return "--Invalid Value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_sleep_clock_action:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_sleep_clock_action
            Typecast object.

        """
        return hci_sleep_clock_action(int.from_bytes(val, byteorder="little"))


class hci_clock_accuracy(hci_type):
    """
    HCI clock accuracy type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._clock_accuracy(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_clock_accuracy:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_clock_accuracy
            Typecast object.

        """
        return hci_clock_accuracy(int.from_bytes(val, byteorder="little"))

    class _clock_accuracy(Enum):
        PPM_500 = 0x00
        PPM_250 = 0x01
        PPM_150 = 0x02
        PPM_100 = 0x03
        PPM_75 = 0x04
        PPM_50 = 0x05
        PPM_30 = 0x06
        PPM_20 = 0x07


class hci_clock_accuracy_ranged(hci_type):
    """
    HCI clock accuracy ranged type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._clock_accuracy_ranged(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_clock_accuracy_ranged:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_clock_accuracy_ranged
            Typecast object.

        """
        return hci_clock_accuracy_ranged(int.from_bytes(val, byteorder="little"))

    class _clock_accuracy_ranged(Enum):
        PPM_251_TO_500 = 0x00
        PPM_151_TO_250 = 0x01
        PPM_101_TO_150 = 0x02
        PPM_76_TO_100 = 0x03
        PPM_51_TO_75 = 0x04
        PPM_31_TO_50 = 0x05
        PPM_21_TO_30 = 0x06
        PPM_0_TO_20 = 0x07


class hci_packing_mode(hci_type):
    """
    HCI packing mode type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "Sequential"
        if self.value == 0x01:
            return "Interleaved"
        return "--Invalid Value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_packing_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_packing_mode
            Typecast object.

        """
        return hci_packing_mode(int.from_bytes(val, byteorder="little"))


class hci_framing_mode(hci_type):
    """
    HCI framing mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._framing_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_framing_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_framing_mode
            Typecast object.

        """
        return hci_framing_mode(int.from_bytes(val, byteorder="little"))

    class _framing_mode(Enum):
        UNFRAMED = 0x00
        FRAMED_SEGMENTED = 0x01
        FRAMED_UNSEGMENTED = 0x02


class hci_iso_payload_type(hci_type):
    """
    HCI ISO payload type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._iso_payload_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_iso_payload_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_iso_payload_type
            Typecast object.

        """
        return hci_iso_payload_type(int.from_bytes(val, byteorder="little"))

    class _iso_payload_type(Enum):
        ZERO_LENGTH = 0x00
        VARIABLE_LENGTH = 0x01
        MAXIMUM_LENGTH = 0x02


class hci_address_change_reasons(hci_type):
    """
    HCI address change reasons type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._address_change_reasons(val)
        self.name = _get_name(to_mask, self._address_change_reasons)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_address_change_reasons:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_address_change_reasons
            Typecast object.

        """
        return hci_address_change_reasons(int.from_bytes(val, byteorder="little"))

    class _address_change_reasons(Flag):
        ADVERTISING_DATA_CHANGE = 1 << 0
        SCAN_RESPONSE_DATA_CHANGE = 1 << 1


class hci_decision_flags(hci_type):
    """
    HCI decision flags type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._decision_flags(val)
        self.name = _get_name(to_mask, self._decision_flags)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_decision_flags:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_decision_flags
            Typecast object.

        """
        return hci_decision_flags(int.from_bytes(val, byteorder="little"))

    class _decision_flags(Flag):
        RESOLVABLE_TAG_INCLUDED = 1 << 0
        SCAN_RESPONSE_DATA_CHANGE = 1 << 1


class hci_test_flags(hci_type):
    """
    HCI test flags type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._test_flags(val)
        self.name = _get_name(to_mask, self._test_flags)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_test_flags:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_test_flags
            Typecast object.

        """
        return hci_test_flags(int.from_bytes(val, byteorder="little"))

    class _test_flags(Flag):
        NEW_TEST_GROUP = 1 << 0
        PASS_IF_FIELD_PRESENT_AND_CHECK_PASSES = 1 << 1
        PASS_IF_FIELD_PRESENT_AND_CHECK_FAILS = 1 << 2
        PASS_IF_FIELD_NOT_PRESENT = 1 << 3


class hci_test_fields(hci_type):
    """
    HCI test fields type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        if self.value == 0x00:
            return "ResolvableTag"
        if self.value == 0x06:
            return "AdvMode"
        if self.value == 0x07:
            return "RSSI"
        if self.value == 0x08:
            return "PathLoss"
        if self.value == 0x09:
            return "AdvA"
        if 17 <= self.value <= 24:
            return f"ArbitraryData, length={self.value - 16}"
        if 33 <= self.value <= 40:
            return f"ArbitraryData, length>={self.value - 32}"
        if 49 <= self.value <= 56:
            return f"ArbitraryData, 1<=length<={self.value - 48}"
        if 240 <= self.value <= 255:
            return "VendorSpecific"
        return "--Invalid Value--"

    @staticmethod
    def from_bytes(val: bytes) -> hci_test_fields:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_test_fields
            Typecast object.

        """
        return hci_test_fields(int.from_bytes(val, byteorder="little"))


class hci_cs_role_mask(hci_type):
    """
    HCI CS role mask type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_role_mask(val)
        self.name = _get_name(to_mask, self._cs_role_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_role_mask:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_role_mask
            Typecast object.

        """
        return hci_cs_role_mask(int.from_bytes(val, byteorder="little"))

    class _cs_role_mask(Flag):
        INITIATOR = 1 << 0
        REFLECTOR = 1 << 1


class hci_cs_role_select(hci_type):
    """
    HCI CS role select type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_role_select(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_role_select:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_role_select
            Typecast object.

        """
        return hci_cs_role_select(int.from_bytes(val, byteorder="little"))

    class _cs_role_select(Enum):
        INITIATOR = 0x00
        REFLECTOR = 0x01


class hci_cs_mode(hci_type):
    """
    HCI CS mode type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_mode(val)
        self.name = _get_name(to_mask, self._cs_mode)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_mode
            Typecast object.

        """
        return hci_cs_mode(int.from_bytes(val, byteorder="little"))

    class _cs_mode(Flag):
        MODE3 = 1 << 0


class hci_rtt_capability(hci_type):
    """
    HCI RTT capability type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        rstr = "\n"
        rstr += f"        RTT_AA_Only_N={'150ns' if self.value & (1 << 0) == 0 else '10ns'}\n"
        rstr += f"        RTT_Sounding_N={'150ns' if self.value & (1 << 1) == 0 else '10ns'}\n"
        rstr += f"        RTT_Random_Payload_N"
        rstr += f"{'150ns' if self.value & (1 << 2) == 0 else '10ns'}"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_rtt_capability:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_rtt_capability
            Typecast object.

        """
        return hci_rtt_capability(int.from_bytes(val, byteorder="little"))


class hci_rtt_type(hci_type):
    """
    HCI RTT type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._rtt_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_rtt_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_rtt_type
            Typecast object.

        """
        return hci_rtt_type(int.from_bytes(val, byteorder="little"))

    class _rtt_type(Enum):
        RTT_AA_ONLY = 0x00
        RTT_SOUNDING_32BITS = 0x01
        RTT_SOUNDING_96BITS = 0x02
        RTT_RANDOM_32BITS = 0x03
        RTT_RANDOM_64BITS = 0x04
        RTT_RANDOM_96BITS = 0x05
        RTT_RANDOM_128BITS = 0x06


class hci_nadm_sounding_capability(hci_type):
    """
    HCI NADM sounding capability type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._nadm_sounding_capability(val)
        self.name = _get_name(to_mask, self._nadm_sounding_capability)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_nadm_sounding_capability:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_nadm_sounding_capability
            Typecast object.

        """
        return hci_nadm_sounding_capability(int.from_bytes(val, byteorder="little"))

    class _nadm_sounding_capability(Flag):
        PHASE_BASED_NADM = 1 << 0


class hci_nadm_random_capability(hci_type):
    """
    HCI NADM random capability type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._nadm_random_capability(val)
        self.name = _get_name(to_mask, self._nadm_random_capability)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_nadm_random_capability:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_nadm_random_capability
            Typecast object.

        """
        return hci_nadm_random_capability(int.from_bytes(val, byteorder="little"))

    class _nadm_random_capability(Flag):
        PHASE_BASED_NADM = 1 << 0


class hci_cs_sync_phy_mask(hci_type):
    """
    HCI CS sync PHY mask type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_sync_phy_mask(val)
        self.name = _get_name(to_mask, self._cs_sync_phy_mask)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_sync_phy_mask:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_sync_phy_mask
            Typecast object.

        """
        return hci_cs_sync_phy_mask(int.from_bytes(val, byteorder="little"))

    class _cs_sync_phy_mask(Flag):
        LE_2M = 1 << 1
        LE_2M_2BT = 1 << 2


class hci_cs_sync_phy_select(hci_type):
    """
    HCI CS sync PHY select type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_sync_phy_select(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_sync_phy_select:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_sync_phy_select
            Typecast object.

        """
        return hci_cs_sync_phy_select(int.from_bytes(val, byteorder="little"))

    class _cs_sync_phy_select(Enum):
        LE_1M = 0x01
        LE_2M = 0x02
        LE_2M_2BT = 0x03


class hci_cs_subfeatures(hci_type):
    """
    HCI CS subfeatures type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_subfeatures(val)
        self.name = _get_name(to_mask, self._cs_subfeatures)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_subfeatures:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_subfeatures
            Typecast object.

        """
        return hci_cs_subfeatures(int.from_bytes(val, byteorder="little"))

    class _cs_subfeatures(Flag):
        NO_TX_FAE = 1 << 1
        CHANNEL_SELECTION_ALGORITHM_3C = 1 << 2
        PHASE_BASED_RANGING = 1 << 3


class hci_cs_times(hci_type):
    """
    HCI CS times type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_times(val)
        self.name = _get_name(to_mask, self._cs_times)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_times:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_times
            Typecast object.

        """
        return hci_cs_times(int.from_bytes(val, byteorder="little"))

    class _cs_times(Flag):
        T_10US = 1 << 0
        T_20US = 1 << 1
        T_30US = 1 << 2
        T_40US = 1 << 3
        T_50US = 1 << 4
        T_60US = 1 << 5
        T_80US = 1 << 6
        T_100US = 1 << 7
        T_120US = 1 << 8


class hci_cs_times_fcs(hci_type):
    """
    HCI FCS-specific CS times type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_times_fcs(val)
        self.name = _get_name(to_mask, self._cs_times_fcs)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_times_fcs:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_times_fcs
            Typecast object.

        """
        return hci_cs_times_fcs(int.from_bytes(val, byteorder="little"))

    class _cs_times_fcs(Flag):
        T_15US = 1 << 0
        T_20US = 1 << 1
        T_30US = 1 << 2
        T_40US = 1 << 3
        T_50US = 1 << 4
        T_60US = 1 << 5
        T_80US = 1 << 6
        T_100US = 1 << 7
        T_120US = 1 << 8


class hci_tx_snr_capability(hci_type):
    """
    HCI TX SNR capability type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._tx_snr_capability(val)
        self.name = _get_name(to_mask, self._tx_snr_capability)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_tx_snr_capability:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_tx_snr_capability
            Typecast object.

        """
        return hci_tx_snr_capability(int.from_bytes(val, byteorder="little"))

    class _tx_snr_capability(Flag):
        P_18DB = 1 << 0
        P_21DB = 1 << 1
        P_24DB = 1 << 2
        P_27DB = 1 << 3
        P_30DB = 1 << 4


class hci_tx_snr_select(hci_type):
    """
    HCI TX SNR select type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._tx_snr_select(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_tx_snr_select:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_tx_snr_select
            Typecast object.

        """
        return hci_tx_snr_select(int.from_bytes(val, byteorder="little"))

    class _tx_snr_select(Enum):
        SNR_CONTROL_ADJUSTMENT_18DB = 0x00
        SNR_CONTROL_ADJUSTMENT_21DB = 0x01
        SNR_CONTROL_ADJUSTMENT_24DB = 0x02
        SNR_CONTROL_ADJUSTMENT_27DB = 0x03
        SNR_CONTROL_ADJUSTMENT_30DB = 0x04
        NO_SNR_CONTROL = 0xFF


class hci_cs_fae_table(hci_type):
    """
    HCI CS FAE table type.
    """

    def __init__(self, val: List[int]) -> None:
        allowed_ch = [*range(79)]
        allowed_ch.remove(0)
        allowed_ch.remove(1)
        allowed_ch.remove(23)
        allowed_ch.remove(24)
        allowed_ch.remove(25)
        allowed_ch.remove(77)
        allowed_ch.remove(78)
        self._allowed_ch = allowed_ch
        self.value = val

    def __repr__(self) -> str:
        rstr = "\n"
        for idx, val in enumerate(self.value):
            rstr += f"        CH{self._allowed_ch[idx]}: {val/32:.4f}ppm\n"
        rstr.strip()
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_fae_table:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_fae_table
            Typecast object.

        """
        max_byte_val = 256
        return hci_cs_fae_table([max_byte_val - x for x in val[::-1]])


class hci_cs_channel_map(hci_type):
    """
    HCI CS channel map type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_channel_map(val)
        self.name = _get_name(to_mask, self._cs_channel_map)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_channel_map:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_channel_map
            Typecast object.

        """
        return hci_cs_channel_map(int.from_bytes(val, byteorder="little"))

    class _cs_channel_map(Flag):
        CH2 = 1 << 2
        CH3 = 1 << 3
        CH4 = 1 << 4
        CH5 = 1 << 5
        CH6 = 1 << 6
        CH7 = 1 << 7
        CH8 = 1 << 8
        CH9 = 1 << 9
        CH10 = 1 << 10
        CH11 = 1 << 11
        CH12 = 1 << 12
        CH13 = 1 << 13
        CH14 = 1 << 14
        CH15 = 1 << 15
        CH16 = 1 << 16
        CH17 = 1 << 17
        CH18 = 1 << 18
        CH19 = 1 << 19
        CH20 = 1 << 20
        CH21 = 1 << 21
        CH22 = 1 << 22
        CH26 = 1 << 26
        CH27 = 1 << 27
        CH28 = 1 << 28
        CH29 = 1 << 29
        CH30 = 1 << 30
        CH31 = 1 << 31
        CH32 = 1 << 32
        CH33 = 1 << 33
        CH34 = 1 << 34
        CH35 = 1 << 35
        CH36 = 1 << 36
        CH37 = 1 << 37
        CH38 = 1 << 38
        CH39 = 1 << 39
        CH40 = 1 << 40
        CH41 = 1 << 41
        CH42 = 1 << 42
        CH43 = 1 << 43
        CH44 = 1 << 44
        CH45 = 1 << 45
        CH46 = 1 << 46
        CH47 = 1 << 47
        CH48 = 1 << 48
        CH49 = 1 << 49
        CH50 = 1 << 50
        CH51 = 1 << 51
        CH52 = 1 << 52
        CH53 = 1 << 53
        CH54 = 1 << 54
        CH55 = 1 << 55
        CH56 = 1 << 56
        CH57 = 1 << 57
        CH58 = 1 << 58
        CH59 = 1 << 59
        CH60 = 1 << 60
        CH61 = 1 << 61
        CH62 = 1 << 62
        CH63 = 1 << 63
        CH64 = 1 << 64
        CH65 = 1 << 65
        CH66 = 1 << 66
        CH67 = 1 << 67
        CH68 = 1 << 68
        CH69 = 1 << 69
        CH70 = 1 << 70
        CH71 = 1 << 71
        CH72 = 1 << 72
        CH73 = 1 << 73
        CH74 = 1 << 74
        CH75 = 1 << 75
        CH76 = 1 << 76


class hci_csa_type(hci_type):
    """
    HCI channel-select algorithm type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._csa_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_csa_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_csa_type
            Typecast object.

        """
        return hci_csa_type(int.from_bytes(val, byteorder="little"))

    class _csa_type(Enum):
        ALGORITHM_1 = 0x00
        ALGORITHM_2 = 0x01


class hci_cs_csa_type(hci_type):
    """
    HCI CS channel-select algorithm type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_csa_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_csa_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_csa_type
            Typecast object.

        """
        return hci_cs_csa_type(int.from_bytes(val, byteorder="little"))

    class _cs_csa_type(Enum):
        ALGORITHM_3b = 0x00
        ALGORITHM_3c = 0x01


class hci_cs_ch3c_shape(hci_type):
    """
    HCI CS CH3C shape type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_ch3c_shape(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_ch3c_shape:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_ch3c_shape
            Typecast object.

        """
        return hci_cs_ch3c_shape(int.from_bytes(val, byteorder="little"))

    class _cs_ch3c_shape(Enum):
        HAT_SHAPE = 0x00
        X_SHAPE = 0x01


class hci_antenna_select(hci_type):
    """
    HCI antenna select type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._antenna_select(val)
        self.name = _get_name(to_mask, self._antenna_select)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_antenna_select:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_antenna_select
            Typecast object.

        """
        return hci_antenna_select(int.from_bytes(val, byteorder="little"))

    class _antenna_select(Flag):
        FIRST_ORDERED = 1 << 0
        SECOND_ORDERED = 1 << 1
        THIRD_ORDERED = 1 << 2
        FOURTH_ORDERED = 1 << 3


class hci_cs_override_config(hci_type):
    """
    HCI CS configuration override type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        rstr = []
        if (self.value >> 0) & 0x1 == 0x1:
            rstr.extend(["Channel_Length", "Channel[i]"])
        else:
            rstr.extend(
                ["Channel_Map", "Channel_Selection_Type", "Ch3c_Shape", "Ch3c_Jump"]
            )
        if (self.value >> 2) & 0x1 == 0x1:
            rstr.append("Main_Mode_Steps")
        if (self.value >> 3) & 0x1 == 0x1:
            rstr.append("T_PM_Tone_Ext")
        if (self.value >> 4) & 0x1 == 0x1:
            rstr.append("Tone_Antenna_Permutation")
        if (self.value >> 5) & 0x1 == 0x1:
            rstr.extend(["CS_SYNC_AA_Initiator", "CS_SYNC_AA_Reflector"])
        if (self.value >> 6) & 0x1 == 0x1:
            rstr.extend(["SS_Marker1_Position", "SS_Marker2_Position"])
        if (self.value >> 7) & 0x1 == 0x1:
            rstr.append("SS_Marker_Value")
        if (self.value >> 8) & 0x1 == 0x1:
            rstr.extend(["CS_SYNC_Payload_Pattern", "CS_Sync_User_Payload"])
        if (self.value >> 10) & 0x1 == 0x1:
            rstr.append("Stable_Phase_Test")
        return ", ".join(rstr)

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_override_config:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_override_config
            Typecast object.

        """
        return hci_cs_override_config(int.from_bytes(val, byteorder="little"))


class hci_spacing_types(hci_type):
    """
    HCI spacing types type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._spacing_types(val)
        self.name = _get_name(to_mask, self._spacing_types)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_spacing_types:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_spacing_types
            Typecast object.

        """
        return hci_spacing_types(int.from_bytes(val, byteorder="little"))

    class _spacing_types(Flag):
        T_IFS_ACL_CP = 1 << 0
        T_IFS_ACL_PC = 1 << 1
        T_MCES = 1 << 2
        T_IFS_CIS = 1 << 3
        T_MSS_CIS = 1 << 4


class hci_link_type(hci_type):
    """
    HCI link type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._link_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_link_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_link_type
            Typecast object.

        """
        return hci_link_type(int.from_bytes(val, byteorder="little"))

    class _link_type(Enum):
        SCO = 0x00
        ACL = 0x01
        E_SCO = 0x02


class hci_link_packet_type(hci_type):
    """
    HCI link packet type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._link_packet_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_link_packet_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_link_packet_type
            Typecast object.

        """
        return hci_link_packet_type(int.from_bytes(val, byteorder="little"))

    class _link_packet_type(Enum):
        SCO = 0x00
        ACL = 0x01
        ISO = 0x02


class hci_lmp_features(hci_type):
    """
    HCI LMP features type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return bin(self.value)

    @staticmethod
    def from_bytes(val: bytes) -> hci_lmp_features:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_lmp_features
            Typecast object.

        """
        return hci_lmp_features(int.from_bytes(val, byteorder="little"))


class hci_le_features(hci_type):
    """
    HCI LE features type.
    """

    def __init__(self, val: int) -> None:
        self.value = val

    def __repr__(self) -> str:
        return bin(self.value)

    @staticmethod
    def from_bytes(val: bytes) -> hci_le_features:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_le_features
            Typecast object.

        """
        return hci_le_features(int.from_bytes(val, byteorder="little"))


class hci_bt_mode(hci_type):
    """
    HCI BT mode type/
    """

    def __init__(self, val: int) -> None:
        to_mask = self._bt_mode(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_bt_mode:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_bt_mode
            Typecast object.

        """
        return hci_bt_mode(int.from_bytes(val, byteorder="little"))

    class _bt_mode(Enum):
        ACTIVE = 0x00
        HOLD = 0x01
        SNIFF = 0x02


class hci_link_key_type(hci_type):
    """
    HCI link key type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._link_key_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_link_key_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_link_key_type
            Typecast object.

        """
        return hci_link_key_type(int.from_bytes(val, byteorder="little"))

    class _link_key_type(Enum):
        COMBINATION = 0x00
        DEBUG_COMBINATION = 0x03
        P192_UNAUTHENTICATED_COMBINATION = 0x04
        P192_AUTHENTICATED_COMBINATION = 0x05
        CHANGED_COMBINATION = 0x06
        P256_UNAUTHENTICATED_COMBINATION = 0x07
        P256_AUTHENTICATED_COMBINATION = 0x08


class hci_path_loss_zone(hci_type):
    """
    HCI path loss zone type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._path_loss_zone(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_path_loss_zone:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_path_loss_zone
            Typecast object.

        """
        return hci_path_loss_zone(int.from_bytes(val, byteorder="little"))

    class _path_loss_zone(Enum):
        LOW = 0x00
        MIDDLE = 0x01
        HIGH = 0x02


class hci_tx_power_reporting_reason(hci_type):
    """
    HCI TX power reporting reason type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._tx_power_reporting_reason(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_tx_power_reporting_reason:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_tx_power_reporting_reason
            Typecast object.

        """
        return hci_tx_power_reporting_reason(int.from_bytes(val, byteorder="little"))

    class _tx_power_reporting_reason(Enum):
        LOCAL_TX_POWER_CHANGED = 0x00
        REMOTE_TX_POWER_CHANGED = 0x01
        LE_READ_REMOTE_TX_POWER_LEVEL_COMMAND_COMPLETED = 0x02


class hci_cs_config_action(hci_type):
    """
    HCI CS configuration action type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_config_action(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_config_action:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_config_action
            Typecast object.

        """
        return hci_cs_config_action(int.from_bytes(val, byteorder="little"))

    class _cs_config_action(Enum):
        REMOVED = 0x00
        CREATED = 0x01


class hci_cs_procedure_done_status(hci_type):
    """
    HCI CS procedure done status type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._cs_procedure_done_status(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_procedure_done_status:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_procedure_done_status
            Typecast object.

        """
        return hci_cs_procedure_done_status(int.from_bytes(val, byteorder="little"))

    class _cs_procedure_done_status(Enum):
        COMPLETE = 0x00
        MORE_TO_COME = 0x01
        ABORTED = 0x0F


class hci_cs_abort_reason(hci_type):
    """
    HCI CS abort reason type.
    """

    def __init__(self, val: int) -> None:
        to_mask_proc = self._cs_abort_reason_procedure(val & 0x0F)
        to_mask_sub = self._cs_abort_reason_subevent((val & 0xF0) >> 4)
        self.name = [to_mask_proc.name, to_mask_sub.name]
        self.value = [to_mask_proc.value, to_mask_sub.value]

    def __repr__(self) -> str:
        rstr = "\n"
        rstr += f"        Procedure={self.name[0]} ({self.value[0]})\n"
        rstr += f"        Subevent={self.name[1]} ({self.value[1]})"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_cs_abort_reason:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_cs_abort_reason
            Typecast object.

        """
        return hci_cs_abort_reason(int.from_bytes(val, byteorder="little"))

    class _cs_abort_reason_procedure(Enum):
        NO_ABORT = 0x00
        LOCAL_HOST_OR_REMOTE_REQUEST = 0x01
        FILTERED_CHANNEL_MAP_HAS_TOO_FEW_CHANNELS = 0x02
        CHANNEL_MAP_UPDATE_INSTANT_HAS_PASSED = 0x03
        UNSPECIFIED = 0x0F

    class _cs_abort_reason_subevent(Enum):
        NO_ABORT = 0x00
        LOCAL_HOST_OR_REMOTE_REQUEST = 0x01
        NO_CS_SYNC_RECEIVED = 0x02
        SCHEDULING_CONFLICT_OR_LIMITED_RESOURCES = 0x03
        UNSPECIFIED = 0x0F


class hci_monitor_condition(hci_type):
    """
    HCI monitor condition type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._monitor_condition(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_monitor_condition:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_monitor_condition
            Typecast object.

        """
        return hci_monitor_condition(int.from_bytes(val, byteorder="little"))

    class _monitor_condition(Enum):
        DEVICE_RSSI_BELOW_LOW_THRESHOLD_LONGER_THAN_TIMEOUT_PERIOD = 0x00
        DEVICE_RSSI_GREATER_THAN_OR_EQUAL_TO_HIGH_THRESHOLD = 0x01


class hci_initiator(hci_type):
    """
    HCI initiator type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._initiator(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_initiator:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_initiator
            Typecast object.

        """
        return hci_initiator(int.from_bytes(val, byteorder="little"))

    class _initiator(Enum):
        HOST = 0x00
        CONTROLLER = 0x01
        PEER = 0x02


class hci_codec_transport(hci_type):
    """
    HCI codec transport type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._codec_transport(val)
        self.name = _get_name(to_mask, self._codec_transport)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_codec_transport:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_codec_transport
            Typecast object.

        """
        return hci_codec_transport(int.from_bytes(val, byteorder="little"))

    class _codec_transport(Flag):
        BR_EDR_ACL = 1 << 0
        BR_EDR_SCO_ESCO = 1 << 1
        LE_CIS = 1 << 2
        LE_BIS = 1 << 3


class hci_simple_pairing_options(hci_type):
    """
    HCI simple pairing options type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._simple_pairing_options(val)
        self.name = _get_name(to_mask, self._simple_pairing_options)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_simple_pairing_options:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_simple_pairing_options
            Typecast object.

        """
        return hci_simple_pairing_options(int.from_bytes(val, byteorder="little"))

    class _simple_pairing_options(Flag):
        PERFORM_REMOTE_PUBLIC_KEY_VALIDATION = 1 << 0


class hci_switching_sampling_rate(hci_type):
    """
    HCI switching sampling rate type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._switching_sampling_rate(val)
        self.name = _get_name(to_mask, self._switching_sampling_rate)
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_switching_sampling_rate:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_switching_sampling_rate
            Typecast object.

        """
        return hci_switching_sampling_rate(int.from_bytes(val, byteorder="little"))

    class _switching_sampling_rate(Flag):
        AOD_1US_SWITCHING = 1 << 0
        AOD_1US_SAMPLING = 1 << 0
        AOA_1US_SWITCHING_SAMPLING = 1 << 2


class hci_l2cap_reason(hci_type):
    """
    HCI L2CAP reason type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_reason(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_reason:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_l2cap_reason
            Typecast object.

        """
        return hci_l2cap_reason(int.from_bytes(val, byteorder="little"))

    class _l2cap_reason(Enum):
        COMMAND_NOT_UNDERSTOOD = 0x00
        SIGNALING_MTU_EXCEEDED = 0x01
        INVALID_CID_IN_REQUEST = 0x02


class hci_l2cap_connection_result(hci_type):
    """
    HCI L2CAP connection result type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_connection_result(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_connection_result:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_l2cap_connection_result
            Typecast object.

        """
        return hci_l2cap_connection_result(int.from_bytes(val, byteorder="little"))

    class _l2cap_connection_result(Enum):
        CONNECTION_SUCCESSFUL = 0x00
        CONNECTION_PENDING = 0x01
        CONNECTION_REFUSED_PSM_NOT_SUPPORTED = 0x02
        CONNECTION_REFUSED_SECURITY_BLOCK = 0x03
        CONNECTION_REFUSED_NO_RESOURCES_AVAILABLE = 0x04
        CONNECTION_REFUSED_INVALID_SOURCE_CID = 0x06
        CONNECTION_REFUSED_SOURCE_CID_ALREADY_ALLOCATED = 0x07


class hci_l2cap_configure_result(hci_type):
    """
    HCI L2CAP configure result type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_configure_result(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_configure_result:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_l2cap_configure_result
            Typecast object.

        """
        return hci_l2cap_configure_result(int.from_bytes(val, byteorder="little"))

    class _l2cap_configure_result(Enum):
        SUCCESS = 0x00
        FAILURE_UNACCEPTABLE_PARAMETERS = 0x01
        FAILURE_REJECTED = 0x02
        FAILURE_UNKNOWN_OPTIONS = 0x03
        PENDING = 0x04
        FAILURE_FLOW_SPEC_REJECTED = 0x05


class hci_l2cap_credit_connection_result(hci_type):
    """
    HCI L2CAP credit-based connection result type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_credit_connection_result(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_credit_connection_result:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_l2cap_credit_connection_result
            Typecast object.

        """
        return hci_l2cap_credit_connection_result(
            int.from_bytes(val, byteorder="little")
        )

    class _l2cap_credit_connection_result(Enum):
        CONNECTION_SUCCESSFUL = 0x00
        CONNECTION_REFUSED_SPSM_NOT_SUPPORTED = 0x02
        CONNECTION_REFUSED_NO_RESOURCES_AVAILABLE = 0x04
        CONNECTION_REFUSED_INSUFFICIENT_AUTHENTICATION = 0x05
        CONNECTION_REFUSED_INSUFFICIENT_AUTHORIZATION = 0x06
        CONNECTION_REFUSED_ENCRYPTION_KEY_SIZE_TOO_SHORT = 0x07
        CONNECTION_REFUSED_INSUFFICIENT_ENCRYPTION = 0x08
        CONNECTION_REFUSED_INVALID_SOURCE_CID = 0x09
        CONNECTION_REFUSED_SOURCE_CID_ALREADY_ALLOCATED = 0x0A
        CONNECTION_REFUSED_UNACCEPTABLE_PARAMETERS = 0x0B
        CONNECTION_REFUSED_INVALID_PARAMETERS = 0x0C
        CONNECTION_PENDING = 0x0D
        CONNECTION_PENDING_AUTHENTICATION_PENDING = 0x0E
        CONNECTION_PENDING_AUTHORIZATION_PENDING = 0x0F


class hci_l2cap_credit_reconfigure_result(hci_type):
    """
    HCI L2CAP credit-based connection reconfigure result type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_credit_reconfigure_result(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_credit_reconfigure_result:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_l2cap_credit_reconfigure_result
            Typecast object.

        """
        return hci_l2cap_credit_reconfigure_result(
            int.from_bytes(val, byteorder="little")
        )

    class _l2cap_credit_reconfigure_result(Enum):
        RECONFIGURATION_SUCCESSFUL = 0x00
        RECONFIGURATION_FAILED_REDUCTION_IN_SIZE_OF_MTU_NOT_ALLOWED = 0x01
        RECONFIGURATION_FAILED_MPS_SIZE_REDUCTION_NOT_ALLOWED_FOR_MULTIPLE_CHANNELS = (
            0x02
        )
        RECONFIGURATION_FAILED_ONE_OR_MORE_DESTINATION_CIDS_INVALID = 0x03
        RECONFIGURATION_FAILED_OTHER_UNACCEPTABLE_PARAMETERS = 0x04


class hci_l2cap_status(hci_type):
    """
    HCI L2CAP status type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_status(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_status:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_l2cap_status
            Typecast object.

        """
        return hci_l2cap_status(int.from_bytes(val, byteorder="little"))

    class _l2cap_status(Enum):
        NO_FUTHER_INFORMATION_AVAILABLE = 0x00
        AUTHENTICATION_PENDING = 0x01
        AUTHORIZATION_PENDING = 0x02


class hci_l2cap_info_type(hci_type):
    """
    HCI L2CAP info type type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_info_type(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_info_type:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Results
        -------
        hci_l2cap_info_type
            Typecast object.

        """
        return hci_l2cap_info_type(int.from_bytes(val, byteorder="little"))

    class _l2cap_info_type(Enum):
        CONNECTIONLESS_MTU = 0x01
        EXTENDED_FEATURE_MASK = 0x02
        FIXED_CHANNELS_SUPPORTED_OVER_BR_EDR = 0x03


class hci_l2cap_info_result_type(hci_type):
    """
    HCI L2CAP info result type.
    """

    def __init__(self, val: int) -> None:
        to_mask = self._l2cap_info_result(val)
        self.name = to_mask.name
        self.value = to_mask.value

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_l2cap_info_result_type:
        """Typcast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Returns
        -------
        hci_l2cap_info_result_type
            Typecast object.

        """
        return hci_l2cap_info_result_type(int.from_bytes(val, byteorder="little"))

    class _l2cap_info_result(Enum):
        SUCCESS = 0x00
        NOT_SUPPORTED = 0x01


class hci_att_error_code(hci_type):
    """
    HCI ATT protocol error code type.
    """

    def __init__(self, val: int) -> None:
        try:
            to_mask = self._att_error_code(val)
            self.name = to_mask.name
            self.value = to_mask.value
        except KeyError as err:
            if 0x80 <= val <= 0x9F:
                self.name = "APPLICATION_ERROR"
                self.value = val
            elif 0xE0 <= val <= 0xFF:
                self.name = "COMMON_PROFILE_AND_SERVICE_ERROR"
                self.value = val
            else:
                raise ValueError("Error code not defined.") from err

    def __repr__(self) -> str:
        return f"{self.name} ({self.value})"

    @staticmethod
    def from_bytes(val: bytes) -> hci_att_error_code:
        """Typcast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Returns
        -------
        hci_att_error_code
            Typecast object.

        """
        return hci_att_error_code(int.from_bytes(val, byteorder="little"))

    class _att_error_code(Enum):
        INVALID_HANDLE = 0x01
        READ_NOT_PERMITTED = 0x02
        WRITE_NOT_PERMITTED = 0x03
        INVALID_PDU = 0x04
        INSUFFICIENT_AUTHENTICATION = 0x05
        REQUEST_NOT_SUPPORTED = 0x06
        INVALID_OFFSET = 0x07
        INSUFFICIENT_AUTHORIZATION = 0x08
        PREPARE_QUEUE_FULL = 0x09
        ATTRIBUTE_NOT_FOUND = 0x0A
        ATTRIBUTE_NOT_LONG = 0x0B
        ENCRYPTION_KEY_TOO_SHORT = 0x0C
        INVALID_ATTRIBUTE_VALUE_LENGTH = 0x0D
        UNLIKELY_ERROR = 0x0E
        INSUFFICIENT_ENCRYPTION = 0x0F
        UNSUPPORTED_GROUP_TYPE = 0x10
        INSUFFICIENT_RESOURCES = 0x11
        DATABASE_OUT_OF_SYNC = 0x12
        VALUE_NOT_ALLOWED = 0x13


class hci_att_info(hci_type):
    """
    HCI ATT protocol info type.
    """

    def __init__(self, fmt: int, hdls: List[int], vals: List[int]) -> None:
        self.data_format = self._data_format_type(fmt)
        self.handles = hdls
        self.data = vals

    def __repr__(self) -> str:
        rstr = "\n"
        rstr = f"        Format={self.data_format.name} ({self.data_format.value})\n"
        for idx, (hdl, val) in enumerate(zip(self.handles, self.data)):
            rstr += f"        Handle[{idx}]=0x{hdl:2X}\n"
            if self.data_format == self._data_format_type.UUID_2B:
                rstr += f"        UUID[{idx}]=0x{val:04X}"
            else:
                rstr += f"        UUID[{idx}]=0x{val:032X}"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_att_info:
        """Typcast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Returns
        -------
        hci_att_info
            Typecast object.

        """
        fmt = int.from_bytes(val[0:1], byteorder="little")
        datalen = 2 if fmt == 0x01 else 16
        hdls = []
        data = []
        idx = 1
        while idx < len(val):
            hdls.append(int.from_bytes(val[idx : idx + 2], byteorder="little"))
            idx += 2
            data.append(int.from_bytes(val[idx : idx + datalen], byteorder="little"))
            idx += datalen
        return hci_att_info(fmt, hdls, data)

    class _data_format_type(Enum):
        UUID_2B = 0x01
        UUID_16B = 0x02


class hci_att_data(hci_type):
    """
    HCI ATT protocol attribute data type.
    """

    def __init__(self, hdl: int, val: int) -> None:
        self.handle = hdl
        self.value = val

    def __repr__(self) -> str:
        rstr = "\n"
        rstr += f"        AttributeHandle=0x{self.handle:04X}\n"
        rstr += f"        AttributeValue=0x{self.value:X}"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_att_data:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Returns
        -------
        hci_att_data
            Typecast object.

        """
        hdl = int.from_bytes(val[0:2], byteorder="little")
        val = int.from_bytes(val[2:], byteorder="big")
        return hci_att_data(hdl, val)


class hci_att_group_data(hci_type):
    """
    HCI ATT protocol attribute group data type.
    """

    def __init__(self, hdl: int, end_group: int, val: int) -> None:
        self.handle = hdl
        self.end_group = end_group
        self.value = val

    def __repr__(self) -> str:
        rstr = "\n"
        rstr += f"        AttributeHandle=0x{self.handle:04X}\n"
        rstr += f"        EndGroupHandle=0x{self.end_group:04X}\n"
        rstr += f"        AttributeValue=0x{self.value:X}"
        return rstr

    @staticmethod
    def from_bytes(val: bytes) -> hci_att_group_data:
        """Typecast bytes object.

        Parameters
        ----------
        val : bytes
            Bytes object to typecast.

        Returns
        -------
        hci_att_group_data
            Typecast object.

        """
        hdl = int.from_bytes(val[0:2], byteorder="little")
        end_group = int.from_bytes(val[2:4], byteorder="little")
        val = int.from_bytes(val[4:], byteorder="big")
        return hci_att_group_data(hdl, end_group, val)
