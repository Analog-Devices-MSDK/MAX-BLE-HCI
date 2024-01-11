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
"""Module for HCI logger handling.

Module defines a logger for test host-controller interfaces.

Attributes
----------
hci_logger : logging.Logger
    Host-controller interface logging object.

"""
import logging
from typing import Dict


class _CustomFormatter(logging.Formatter):
    """Log message formatting class.

    Attributes
    ----------
    cyan : str
        ANSI color code representing the color cyan.
    white : str
        ANSI color code representing the color white.
    green : str
        ANSI color code representing the color green.
    yellow : str
        ANSI color code representing the color yellow.
    red : str
        ANSI color code representing the color red.
    bold_red : str
        ANSI color code representing bold red.
    reset : str
        ANSI reset code.
    format_str : str
        Default logger string format.
    format_info : str
        Logger string format for info-level messages.
    format_debug : str
        Logger string format for debug-level messages.
    FORMATS : Dict[int, str]
        Dictionary containing logger messaging formats.

    """

    cyan: str = "\x1b[36;20m"
    white: str = "\x1b[37;20m"
    green: str = "\x1b[32;20m"
    yellow: str = "\x1b[33;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"
    format_str: str = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )
    format_info: str = "%(levelname)s - %(message)s"
    format_debug: str = "%(levelname)s - %(message)s"

    FORMATS: Dict[int, str] = {
        logging.DEBUG: white + format_debug + reset,
        logging.INFO: green + format_info + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Creates and returns formatted log message.

        Paremeters
        ----------
        record : logging.LogRecord
            Object containing the log record to be formatted.

        Returns
        -------
        str
            The formatted log message.

        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_formatted_logger(log_level=logging.INFO, name="BLE-HCI") -> logging.Logger:
    """Retrieves logger with basic custom format.

    The custom formatted logger applies basic coloring
    for logging of different levels.


    Parameters
    ----------
    log_level : int
        Any defined logging level such as logging.INFO.

    """
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(log_level)

    custom_handler = logging.StreamHandler()
    custom_handler.setLevel(log_level)
    custom_handler.setFormatter(_CustomFormatter())

    if not logger.handlers:
        logger.addHandler(custom_handler)

    return logger
