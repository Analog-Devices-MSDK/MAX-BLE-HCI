# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module defines an ACL ATT packet deserializer.

This module contains the definition of the `AttPacket` class,
which can be used to deserialize, decode, and format ACL ATT
protocol packets.

"""
from __future__ import annotations
from typing import List, Tuple, Union, Optional
from ..packet_codes.acl import ATTProtocolCodes
from ..utils._packet_structs.att_struct import get_params
from ..utils.params import HciParam, HciParamIdxRef


class AttPacket:
    # pylint: disable=too-many-instance-attributes
    """ACL ATT packet deserializer.

    ACL ATT packet format:

    - Attribute opcode         -> bytes=[0:1]
    - Parameters               -> bytes=[1:X]
    - Authentication Signature -> bytes=[X:]

    Parameters
    ----------
    code : ATTProtocolCodes
        Packet-defined ATT protocol opcode.
    auth_flag : bool
        Packet-defined authentication signature flag.
    cmd_flag : bool
        Packet-defined command flag.
    params : bytes
        Packet-defined parameters.
    auth_signature : int, optional
        Packet-defined authentication signature, if used.

    Attributes
    ----------
    code : ATTProtocolCodes
        ATT protocol opcode
    auth_flag : bool
        Authentication signature flag.
    cmd_flag : bool
        Command flag.
    params : bytes
        Packet parameters.
    auth_signature : int, optional
        Authentication signature, if present.

    """

    def __init__(
        self,
        code: ATTProtocolCodes,
        auth_flag: bool,
        cmd_flag: bool,
        params: bytes,
        auth_signature: Optional[int] = None
    ) -> None:
        self.code = code
        self.auth_flag = auth_flag
        self.cmd_flag = cmd_flag
        self.params = params
        self.auth_signature = auth_signature
        self._p_idx = None
        self._p_vals = None

    @staticmethod
    def from_bytes(packet: bytes) -> AttPacket:
        """Create an `AttPacket` object from bytes.

        Deserializes an ACL ATT packet from a bytes object.

        Parameters
        ----------
        packet : bytes
            Packet to deserialize.

        Returns
        -------
        AttPacket
            Deserialized packet.

        """
        att_opcode = int.from_bytes(packet[0:1], byteorder="little")
        code = ATTProtocolCodes(att_opcode >> 0 & 0x3F)
        cmd_flag = att_opcode & 0x40 > 0
        auth_flag = att_opcode & 0x80 > 0
        auth_signature = None
        params = packet[1:]
        if auth_flag:
            auth_signature = int.from_bytes(packet[-12:], byteorder="little")
            params = packet[1:-12]
        return AttPacket(code, auth_flag, cmd_flag, params, auth_signature=auth_signature)

    def parse_packet(self) -> str:
        """Parse and format a deserialized ATT packet.

        Returns
        -------
        str
            The formatted ATT packet.

        """
        rstr = f"AttOpcode={self.code.name}\n"
        rstr += f"AuthenticationFlag={self.auth_flag}\n"
        rstr += f"CommandFlag={self.cmd_flag}\n"
        rstr += f"AuthenticationSignature={self.auth_signature}\n"
        self._p_idx = 0
        params = get_params(self.code)
        if params is None:
            rstr += "Params: None\n"
            return rstr
        rstr += "Params:\n"
        self._p_vals = []
        idx = 0
        for param in params:
            p_str, idx = self._parse_param(param, idx)
            rstr += p_str
        return rstr

    def _parse_param(self, param: Union[HciParam, List[HciParam]], idx: int) -> Tuple[str, int]:
        # pylint: disable=too-many-branches
        """
        Parse a single parameter.
        """
        rstr = ""
        if isinstance(param, list):
            idxref = param.pop(0).ref
            maxidx = 0
            if idxref is None:
                try:
                    maxidx = int(
                        (len(self.params) - self._p_idx)/sum(p.length for p in param)
                    )
                except TypeError:
                    subidx = 0
                    while self._p_idx < len(self.params):
                        for subparam in param:
                            p_str, idx = self._parse_param(subparam, idx)
                            rstr += p_str.format(subidx)
                        subidx += 1
                    return rstr, idx
            else:
                maxidx = self._p_vals[idx + idxref].value
            for subidx in range(maxidx):
                for subparam in param:
                    p_str, idx = self._parse_param(subparam, idx)
                    rstr += p_str.format(subidx)
            return rstr, idx

        p_len = len(self.params) - self._p_idx if param.length is None else param.length
        if isinstance(p_len, HciParamIdxRef):
            if p_len.ref is None:
                p_len = len(self.params) - self._p_idx
            elif p_len.ref < 0:
                p_len = self._p_vals[idx + p_len.ref].value
            else:
                p_len = self._p_vals[p_len.ref].value
        if p_len < 0:
            p_len = len(self.params) - self._p_idx - abs(p_len)
        p_val = param.dtype.from_bytes(self.params[self._p_idx:self._p_idx + p_len])
        self._p_idx += p_len
        idx += 1
        rstr += f"    {param.label}={p_val}\n"
        self._p_vals.append(p_val)
        return rstr, idx
