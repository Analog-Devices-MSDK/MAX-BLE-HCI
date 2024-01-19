#! /usr/bin/env python3
###############################################################################
#
#
# Copyright (C) 2023 Maxim Integrated Products, Inc., All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of Maxim Integrated
# Products, Inc. shall not be used except as stated in the Maxim Integrated
# Products, Inc. Branding Policy.
#
# The mere transfer of this software does not imply any licenses
# of trade secrets, proprietary technology, copyrights, patents,
# trademarks, maskwork rights, or any other form of intellectual
# property whatsoever. Maxim Integrated Products, Inc. retains all
# ownership rights.
#
##############################################################################
#
# Copyright 2023 Analog Devices, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################
"""Contains data classes used for HCI function parameters/returns."""
# pylint: disable=too-many-arguments,too-many-locals,too-many-instance-attributes
from typing import Optional
from dataclasses import dataclass

from .constants import AddrType


@dataclass
class AdvParams:
    """Advertising parameters data container."""

    interval_min: int = 0x60
    """Minimum advertising interval."""

    interval_max: int = 0x60
    """Maximum advertising interval."""

    adv_type: int = 0x3
    """Advertising type."""

    own_addr_type: AddrType = AddrType.PUBLIC
    """Own device address type."""

    peer_addr_type: AddrType = AddrType.PUBLIC
    """Connectable peer device address type."""

    peer_addr: int = 0
    """Connectable peer device address."""

    channel_map: int = 0x7
    """Advertising channel map."""

    filter_policy: int = 0
    """Advertising filter policy."""

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


@dataclass
class ScanParams:
    """Scan parameters data container."""

    scan_type: int = 0x1
    """Scan type."""

    scan_interval: int = 0x100
    """Scan interval."""

    scan_window: int = 0x100
    """Scan duration."""

    addr_type: AddrType = AddrType.PUBLIC
    """Own device address type."""

    filter_policy: int = 0x0
    """Scanning filter policy."""

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


@dataclass
class ConnParams:
    """Connection parameters data container."""

    peer_addr: int
    """Connectable peer device address."""

    scan_interval: int = 0x100
    """Scan interval."""

    scan_window: int = 0x100
    """Scan duration."""

    init_filter_policy: int = 0x0
    """Initiator filter policy."""

    peer_addr_type: AddrType = AddrType.PUBLIC
    """Connectable peer device address type."""

    own_addr_type: AddrType = AddrType.PUBLIC
    """Own device address type."""

    conn_interval_min: int = 0x6
    """Connection interval minimum."""

    conn_interval_max: int = 0x6
    """Connection interval maximum."""

    max_latency: int = 0x0000
    """Maximum peripheral latency."""

    sup_timeout: int = 0x64
    """Supervision timeout."""

    min_ce_length: int = 0x0F10
    """Minimum connection event length."""

    max_ce_length: int = 0x0F10
    """Maximum connection event length."""

    def __post_init__(self):
        if not 0x4 <= self.scan_interval <= 0x4000:
            raise ValueError("Scane interval must be between 0x4 - 0x4000")
        if not 0x4 <= self.scan_window <= 0x4000:
            raise ValueError("Scane window must be between 0x4 - 0x4000")

        if not self.init_filter_policy in [0, 1]:
            raise ValueError(
                f"Init filter policy must be 0x0 or 0x1 {self.init_filter_policy}"
            )

        if not isinstance(self.peer_addr_type, AddrType):
            raise TypeError(
                "Attribute peer_addr_type must be of type AddrType, ",
                f"not {type(self.peer_addr_type).__name__}",
            )

        if self.peer_addr > 2**48 - 1:
            raise ValueError("Peer address must be representable by 6 octets")

        if not isinstance(self.own_addr_type, AddrType):
            raise TypeError(
                "Attribute own_addr_type must be of type AddrType, ",
                f"not {type(self.own_addr_type).__name__}",
            )

        if not 0x6 <= self.conn_interval_max <= 0xC80:
            raise ValueError("Connection interval min must be between 0x6 - 0xC80")

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


class DataPktStats:
    """Generic data stats container for CM and DTM."""

    def __init__(
        self,
        rx_data: int,
        rx_data_crc: int,
        rx_data_timeout: int,
        tx_data: int,
        err_data: int,
        rx_setup: int,
        tx_setup: int,
        rx_isr: int,
        tx_isr: int,
    ) -> None:
        self.rx_data = rx_data
        """Number of packets received correctly."""

        self.rx_data_crc = rx_data_crc
        """Number of packets received with a CRC error."""

        self.rx_data_timeout = rx_data_timeout
        """Number of RX timeouts."""

        self.tx_data = tx_data
        """Number of correctly transmitted packets."""

        self.err_data = err_data
        """Number of data transaction errors."""

        self.rx_setup = rx_setup
        """RX packet setup watermark in microseconds."""

        self.tx_setup = tx_setup
        """TX packet setup watermark in microseconds."""

        self.rx_isr = rx_isr
        """RX ISR processing watermark in microseconds."""

        self.tx_isr = tx_isr
        """TX ISR processing watermark in microseconds."""

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)

    def per(self, peer_tx_data: Optional[int] = None) -> float:
        """Calculate PER.

        Calculates the Packet Error Rate of the current set of
        statistics. If number of peer TX packets is not provided,
        the value is inferred from the number of correctly received
        packets, the number of CRC errors, and the number of timeouts
        recorded by the receiver.

        Parameters
        ----------
        peer_tx_data : Optional[int], optional
            Number of packets transmitted by the peer device.

        Returns
        -------
        float
            Calculated PER value.

        """
        if peer_tx_data:
            return 100 - 100 * (self.rx_data / peer_tx_data)
        return 100 - self.rx_data / (
            self.rx_data + self.rx_data_crc + self.rx_data_timeout
        )


@dataclass
class AdvPktStats:
    """Advertising statistics data container."""

    tx_adv: int = None
    """Number of sent advertising packets."""

    rx_req: int = None
    """Number of advertising requests received correctly."""

    rx_req_crc: int = None
    """Number of advertising requests received with a CRC error."""

    rx_req_timeout: int = None
    """Number of RX timeouts."""

    tx_resp: int = None
    """Number of response packets sent."""

    err_adv: int = None
    """Number of advertising transaction errors."""

    rx_setup: int = None
    """RX packet setup watermark in microseconds."""

    tx_setup: int = None
    """TX packet setup watermark in microseconds."""

    rx_isr: int = None
    """RX ISR processing watermark in microseconds."""

    tx_isr: int = None
    """TX ISR processing watermark in microseconds."""

    tx_chain: Optional[int] = None
    """
    Number of chain packets sent.
    
    .. note::
        Value is only returned when retrieving auxiliary advertising statistics.
    
    """

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


@dataclass
class ScanPktStats:
    """Scanning statistics data container."""

    rx_adv: int = None
    """Number of advertising packets received correctly."""

    rx_adv_crc: int = None
    """Number of advertising packets received with a CRC error."""

    rx_adv_timeout: int = None
    """Number of RX timeouts."""
    tx_req: int = None
    """Number of advertising requests sent."""
    rx_rsp: int = None
    """Number of advertising response packets received correctly."""

    rx_rsp_crc: int = None
    """Number of advertising response packets received with a CRC error."""

    rx_rsp_timeout: int = None
    """Number of advertising response RX timeouts."""
    err_scan: int = None
    """Number of scan transaction errors."""
    rx_setup: int = None
    """RX packet setup watermark in microseconds."""

    tx_setup: int = None
    """TX packet setup watermark in microseconds."""
    rx_isr: int = None
    """RX ISR processing watermark in microseconds."""

    tx_isr: int = None
    """TX ISR processing watermark in microseconds."""
    rx_chain: Optional[int] = None
    """
    Number of chain packets received correctly.
    
    .. note::
        Value is only returned when retrieving auxiliary scanning statistics.
    
    """

    rx_chain_crc: Optional[int] = None
    """
    Number of chain packets received with a CRC error.
    
    .. note::
        Value is only returned when retrieving auxiliary scanning statistics.

    """

    rx_chain_timeout: Optional[int] = None
    """
    Number of chain packet RX timeouts.
    
    .. note::
        Value is only returned when retrieving auxiliary scanning statistics.
    
    """

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


@dataclass
class MemPktStats:
    """Memory statistics data container."""

    stack: int = None
    """Number of bytes used by the stack."""

    sys_assert_cnt: int = None
    """Number of times assertions hit."""

    free_mem: int = None
    """Memory free for stack usage."""

    used_mem: int = None
    """Memory used by stack."""

    max_connections: int = None
    """Maximum number of connections allowed."""

    conn_ctx_size: int = None
    """Number of bytes used for connection context."""

    cs_watermark_lvl: int = None
    """Critical section watermark duration in microseconds."""

    ll_watermark_lvl: int = None
    """Link layer handler watermark level in microseconds."""

    sch_watermark_lvl: int = None
    """Scheduler handler watermark level in microseconds."""

    lhci_watermark_lvl: int = None
    """LHCI handler watermark level in microseconds."""

    max_adv_sets: int = None
    """Maximum number of advertising sets."""

    adv_set_ctx_size: int = None
    """Advertising set context size in bytes."""

    ext_scan_max: int = None
    """Maximum number of extended scanners."""

    ext_scan_ctx_size: int = None
    """Extended scanners context size in bytes."""

    ext_init_ctx_size: int = None
    """Extended initiators context size in bytes."""

    max_num_ext_init: int = None
    """Maximum number of extended initiators."""

    max_per_scanners: int = None
    """Maximum number of periodic scanners."""

    per_scan_ctx_size: int = None
    """Periodic scanners context size in bytes."""

    max_cig: int = None
    """Maximim number of CIG."""

    cig_ctx_size: int = None
    """CIG context size in bytes."""

    cis_ctx_size: int = None
    """CIS context size in bytes."""

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


@dataclass
class PduPktStats:
    """PDU statistics data container."""

    fail_pdu: int = None
    """Number of PDUs failing PDU type filter."""

    pass_pdu: int = None
    """Number of PDUs passing PDU type filter."""

    fail_whitelist: int = None
    """Number of PDUs failing whitelist filter."""

    pass_whitelist: int = None
    """Number of PDUs passing whitelist filter."""

    fail_peer_addr_match: int = None
    """Number of PDUs failing peer address match."""

    pass_peer_addr_match: int = None
    """Number of PDUs passing peer address match."""

    fail_local_addr_match: int = None
    """Number of PDUs failing local address match."""

    pass_local_addr_match: int = None
    """Number of PDUs passing local address match."""

    fail_peer_rpa_verify: int = None
    """Number of peer RPAs failing verification."""

    pass_peer_rpa_verify: int = None
    """Number of peer RPAs passing verification."""

    fail_local_rpa_verify: int = None
    """Number of local RPAs failing verification."""

    pass_local_rpa_verify: int = None
    """Number of local RPAs passing verification."""

    fail_peer_priv_addr: int = None
    """Number of peer addresses failing RPA requirements."""

    fail_local_priv_addr: int = None
    """Number of local addresses failing RPA requirements."""

    fail_peer_addr_res_req: int = None
    """Number of PDUs failing required peer address resolution."""

    pass_peer_addr_res_req: int = None
    """Number of PDUs passing required peer address resolution."""

    pass_local_addr_res_opt: int = None
    """Number of PDUs passing optional local address resolution."""

    peer_res_addr_pend: int = None
    """Number of peer address resolutions pended."""

    local_res_addr_pend: int = None
    """Number of local address resolutions pended."""

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


@dataclass
class TestReport:
    """ISO/ACL test report data container."""

    rx_pkt_count: int = None
    """Number of packets received."""

    rx_oct_count: int = None
    """Number of octets received."""

    gen_pkt_count: int = None
    """Number of generated packets."""

    gen_oct_count: int = None
    """Number of generated octets."""

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)


@dataclass
class PoolStats:
    """Memory pool statistics data container."""

    buf_size: int = None
    """Buffer size."""

    num_buf: int = None
    """Number of buffers."""

    num_alloc: int = None
    """Number of allocations."""

    max_alloc: int = None
    """Maximum number of allocations."""

    max_req_len: int = None
    """Maximum required length."""

    def __repr__(self) -> str:
        print_lns = []
        for key, val in self.__dict__.items():
            if val is None:
                continue
            print_lns.append(f"{key}:  {val}")

        return "\n".join(print_lns)
