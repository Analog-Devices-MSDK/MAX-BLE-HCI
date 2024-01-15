import sys
from typing import List 
import glob
import os
import serial

def get_serial_ports() -> List[str]:
    """Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    SERIAL_LIST_LINUX = "/dev/serial/by-id"

    if os.path.exists(SERIAL_LIST_LINUX):
        dir_list = os.listdir(SERIAL_LIST_LINUX)

        for i, file in enumerate(dir_list):
            dir_list[i] = os.path.join(SERIAL_LIST_LINUX, file)
        if dir_list:
            result.extend(dir_list)

    return result
