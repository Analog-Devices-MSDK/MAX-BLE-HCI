from dataclasses import dataclass


@dataclass
class AdvParams:
    interval_min = 0x60
    interval_max = 0x60
    adv_type = 0x3
    own_addr_type = 0
    peer_addr_type = 0
    peer_addr = 0
    channel_map = 0x7
    filter_policy = 0


@dataclass
class ScanParams:
    scan_type: int = 0x1
    scan_interval: int = 0x100
    scan_window: int = 0x100
    addr_type: int = 0x0
    filter_policy: int = 0x0


@dataclass
class ConnParams:
    peer_addr: int
    scan_interval: int = 0xA000
    scan_window: int = 0xA000
    init_filter_policy: int = 0x0
    peer_addr_type: int = 0x0
    own_addr_type: int = 0x0
    conn_interval_min: int = 0x6
    conn_interval_max: int = 0x6
    max_latency: int = 0x0000
    sup_timeout: int = 0x64
    min_ce_length: int = 0x0F10
    max_ce_length: int = 0x0F10


@dataclass
class TxTestCfg:
    pass
