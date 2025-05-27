# Copyright (c) 2024 Analog Devices, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Module contains parameter definition utilities.

This module defines the `HciParam` and `HciParamIdxRef`
classes, which are used to structure packet parameters
and reference previous parameters, respectively.

"""
from dataclasses import dataclass
from typing import NamedTuple, Optional
from .types import hci_type

class HciParam(NamedTuple):
    """HCI parameter information container.

    Parameters
    ----------
    label : str
        HCI parameter label.
    length : int, optional
        HCI parameter length.
    dtype : hci_type
        HCI parameter type.

    Attributes
    ----------
    label : str
        Parameter label.
    length : int, optional
        Parameter length. Unbounded if `None`.
    dtype : hci_type
        Parameter type.

    """
    label: str
    length: Optional[int]
    dtype: hci_type

@dataclass
class HciParamIdxRef:
    """HCI parameter index reference.

    Parameters
    ----------
    ref : int
        HCI parameter index reference value.

    Attributes
    ----------
    ref : int
        Parameter index reference value.

    """
    ref: int
