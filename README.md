# MAX-BLE-HCI

Python3 BLE HCI over serial Directed to MAX Vendor Specific Commands

Read the [Docs](https://analog-devices-msdk.github.io/MAX-BLE-HCI/)

## Insatll from PyPi

MAX-BLE-HCI is hosted via PyPi and can be installed with the following command

```bash
pip install max-ble-hci
```

## Installation from source

 If you prefer to use the most up to date version, you can also install from source.

 The intsall.sh or .bat are used to install the library into your Python site packages and be done as such.

On Linux or MacOS

```bash
sudo chmod +x install.sh
./install.sh
```

On Windows

```cmd
install.bat
```

## Basic Usage

The BLE-HCI is a mostly generic library, which is capable of driving any BLE devices which can communicate using the UART transport.

To use with Analog Devices, Inc. BLE capable MAX32 microcontrollers, please flash one of the following examples to the chip you are using

- [MAX32655](https://github.com/Analog-Devices-MSDK/msdk/tree/main/Examples/MAX32655/Bluetooth/BLE5_ctr)
- [MAX32665](https://github.com/Analog-Devices-MSDK/msdk/tree/main/Examples/MAX32665/Bluetooth/BLE5_ctr)
- [MAX32690](https://github.com/Analog-Devices-MSDK/msdk/tree/main/Examples/MAX32690/Bluetooth/BLE5_ctr)

If you have not yet set up an installation of the Analog-Devices-MSDK, please follow the instructions found here <https://github.com/Analog-Devices-MSDK/msdk/tree/main>

Once the board is flashed refer to the README in the example to configure your board.

Locate the serial port to which the HCI is connected to. If for example, your serial port is COM5, the following code would be used to reset the device.

```python
from max_ble_hci import BleHci

port_name = "COM5"

hci = BleHci(port_name)
hci.reset()

```

## Command Line Interface (CLI)

By default, the CLI capable of driving the BLE-HCI is installed as part of the package and can be accessed by running

```bash
max_ble_hci --version
```

The cli requires a serial port to connect the HCI to and is passed in through the command line.
Once connected, you can type the help command as such, and begin to explore the CLI.

```bash
usage:  [-h]
        {clear,cls,addr,memstats,adv-start,adv-stop,scan,init,data-len,send-acl,sink-acl,adv-stats,as,scan-stats,ss,conn-stats,cs,test-stats,ts,rssi,ls,pwd,run,reset,tx-test,tx,txtestvs,txvs,rx-test,rx,rx-test-vs,rxvs,end-test,end,reset-ts,rsts,reset-cs,rscs,reset-adv-stats,rsas,reset-scan-stats,rsss,set-phy,sp,tx-power,txp,discon,dc,set-chmap,cmd,exit,quit,q,help,h}
        ...

positional arguments:
  {clear,cls,addr,memstats,adv-start,adv-stop,scan,init,data-len,send-acl,sink-acl,adv-stats,as,scan-stats,ss,conn-stats,cs,test-stats,ts,rssi,ls,pwd,run,reset,tx-test,tx,txtestvs,txvs,rx-test,rx,rx-test-vs,rxvs,end-test,end,reset-ts,rsts,reset-cs,rscs,reset-adv-stats,rsas,reset-scan-stats,rsss,set-phy,sp,tx-power,txp,discon,dc,set-chmap,cmd,exit,quit,q,help,h}
    clear (cls)         Clear the screen
    addr                Set the device address.
    memstats            Get BLE stack memory usage statistics
    adv-start           Start advertising
    adv-stop            Stop advertising
    scan                Send scanning commands and print scan reports, ctrl-c to exit.
    init                Send the initiating commands to open a connection
    data-len            Set the max data length
    send-acl            Send ACL packets
    sink-acl            Sink ACL packets, do not send events to host
    adv-stats (as)      Get the advertising stats
    scan-stats (ss)     Get the scan stats
    conn-stats (cs)     Get the connection stats
    test-stats (ts)     Get the test stats
    rssi                Get an RSSI sample using CCA
    ls                  List directory
    pwd                 print working directory
    run                 run command via os
    reset               Sends an HCI reset command
    tx-test (tx)        Execute the transmitter test.
    txtestvs (txvs)     Execute the vendor-specific transmitter test
    rx-test (rx)        Execute the receiver test
    rx-test-vs (rxvs)   Execute the vendor-specific receiver test
    end-test (end)      End the Tx/Rx test, print the number of correctly received packets
    reset-ts (rsts)     Reset accumulated stats from DTM
    reset-cs (rscs)     Reset accumulated stats from connection mode
    reset-adv-stats (rsas)
                        Reset accumulated stats from connection mode
    reset-scan-stats (rsss)
                        Reset accumulated stats from connection mode
    set-phy (sp)        Set the PHY.
    tx-power (txp)      Set the Tx power
    discon (dc)         Send the command to disconnect
    set-chmap           Set the connection channel map to a given channel.
    cmd                 Send raw HCI command
    exit (quit, q)      Exit the program
    help (h)            Show help message

options:
  -h, --help            show this help message and exit
```

## Contributing

Contributions are encouraged!
Pull requests must pass all GitHub Actions unless directly waved by an admin of the repository.

### Python Versioning

This package is designed to support Python 3.8 and up. Non backwards compatible features will not be accepted (ex Use of match which was introduced in 3.10)

### Style Guidlines

MAX-BLE-HCI is formatted using the Black formatter.
It can be installed via pip using ```pip install black```
