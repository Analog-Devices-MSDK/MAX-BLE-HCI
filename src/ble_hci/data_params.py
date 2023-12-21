from dataclasses import dataclass
from enum import Enum


@dataclass
class AdvParams:
    interval_min: int = 0x60
    interval_max: int = 0x60
    adv_type: int = 0x3
    own_addr_type: int = 0
    peer_addr_type: int = 0
    peer_addr: int = 0
    channel_map: int = 0x7
    filter_policy: int = 0


@dataclass
class ScanParams:
    scan_type: int = 0x1
    scan_interval: int = 0x100
    scan_window: int = 0x100
    addr_type: int = 0x0
    filter_policy: int = 0x0


class PeerAddrType(Enum):
    PUBLIC = 0
    RANDOM = 1
    PUBLIC_IDENTITY = 2
    RANDOM_IDENTITY = 3


@dataclass
class ConnParams:
    peer_addr: int
    scan_interval: int = 0x100
    scan_window: int = 0x100
    init_filter_policy: int = 0x0
    peer_addr_type: int = 0x0
    own_addr_type: int = 0x0
    conn_interval_min: int = 0x6
    conn_interval_max: int = 0x6
    max_latency: int = 0x0000
    sup_timeout: int = 0x64
    min_ce_length: int = 0x0F10
    max_ce_length: int = 0x0F10

    def __post_init__(self):
        if not 0x4 <= self.scan_interval <= 0x4000:
            raise ValueError("Scane interval must be between 0x4 - 0x4000")
        if not 0x4 <= self.scan_window <= 0x4000:
            raise ValueError("Scane window must be between 0x4 - 0x4000")

        if not self.init_filter_policy in [0, 1]:
            raise ValueError(
                f"Init filter policy must be 0x0 or 0x1 {self.init_filter_policy}"
            )

        if self.peer_addr_type not in [0, 1, 2, 3]:
            raise ValueError("Invalid peer address type")

        if self.peer_addr > 2**48 - 1:
            raise ValueError("Peer address must be representable by 6 octets")

        if self.own_addr_type not in [0, 1, 2, 3]:
            raise ValueError("Invalid peer address type")

        if not 0x6 <= self.conn_interval_max <= 0xC80:
            raise ValueError("Connection interval min must be between 0x6 - 0xC80")


@dataclass
class TxTestCfg:
    pass
