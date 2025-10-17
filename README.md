# MAX-BLE-HCI

Python3 BLE HCI over serial Directed to MAX Vendor Specific Commands

Read the [Docs](https://analog-devices-msdk.github.io/MAX-BLE-HCI/)

## Install from PyPi

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
max_ble_hci -h
usage: max_ble_hci [-h] [--version] [-b BAUDRATE] [-efc] [-m MONPORT] [-i IDTAG] [-c [COMMANDS ...]] [--startup-script STARTUP_SCRIPT] [-t TRACE_LEVEL]
                   serial_port

        Bluetooth Low Energy HCI tool.
        This tool is used in tandem with the BLE controller examples. 
        This tool sends HCI commands through the serial port to the target device. 
        It will receive and print the HCI events received from the target device.
        Serial port is configured as 8N1, no flow control, default baud rate of 115200
        

positional arguments:
  serial_port           Serial port path or COM#

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -b BAUDRATE, --baud BAUDRATE
                        Serial port baud rate. Default: 115200
  -efc, --enable-flow-control
                        Enable flow control Default: False
  -m MONPORT, --monitor-trace-port MONPORT
                        Monitor Trace Msg Serial Port path or COM#. Default: None
  -i IDTAG, --id-tag IDTAG
                        Board ID tag for printing trace messages. Default: None
  -c [COMMANDS ...], --commands [COMMANDS ...]
                        Commands to run on startup.
                                If more than 1, separate commands with a semicolon (;).
  --startup-script STARTUP_SCRIPT
                        Filepath to to run startup commands. 
                                Commands should be newline seperated
  -t TRACE_LEVEL, --trace_level TRACE_LEVEL
                        Set the trace level
                                0: Error only
                                1: Warning/Error
                                2: Info/Warning/Error
                                3: All messages
                                Default: 3
```

The cli requires a serial port to connect the HCI to and is passed in through the command line.
Once connected, you can type the help command as such, and begin to explore the CLI.

```bash
>>> help
usage:  [-h]
        {clear,cls,update,sysreset,setflash,erase,addr,memstats,adv-start,adv-stop,scan,init,data-len,send-acl,sink-acl,adv-stats,as,scan-stats,ss,conn-stats,cs,test-stats,ts,rssi,reset,tx-test,tx,txtestvs,txvs,rx-test,rx,rx-test-vs,rxvs,end-test,end,reset-ts,rsts,reset-cs,rscs,reset-adv-stats,rsas,reset-scan-stats,rsss,set-phy,sp,tx-power,txp,discon,dc,set-chmap,cmd,exit,quit,q,ls,cd,pwd,shell,run,help,h}
        ...

positional arguments:
  {clear,cls,update,sysreset,setflash,erase,addr,memstats,adv-start,adv-stop,scan,init,data-len,send-acl,sink-acl,adv-stats,as,scan-stats,ss,conn-stats,cs,test-stats,ts,rssi,reset,tx-test,tx,txtestvs,txvs,rx-test,rx,rx-test-vs,rxvs,end-test,end,reset-ts,rsts,reset-cs,rscs,reset-adv-stats,rsas,reset-scan-stats,rsss,set-phy,sp,tx-power,txp,discon,dc,set-chmap,cmd,exit,quit,q,ls,cd,pwd,shell,run,help,h}
    clear (cls)         Clear the screen
    update              update the firmware
    sysreset            reset the firmware
    setflash            set the flash start address
    erase               erase the flash
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
    ls                  List directory
    cd                  change working directory
    pwd                 print working directory
    shell               run command via os shell
    run                 run command via os
    help (h)            Show help message

options:
  -h, --help            show this help message and exit

options:
  -h, --help            show this help message and exit
```

### Scripting

Scripts can be used at startup and during runtime. The script should be a text file with the newline seperated commands entered as you would using the cli directly.

#### Example (init.txt)

``` txt
reset
addr 00:11:22:33:44:55
```

```bash
max_ble_hci --startup-script init.txt
```

Or while in the CLI

```bash
>>> run init.txt
```

## Decoding Tools

HCI decoding tools are installed by default as part of the package and can be accessed by running

```console
me@example ~ $ hci_decoder -h
usage: hci_decoder [-h] {packet,file,sniff} ...

hcitools: HCI decoding tools

positional arguments:
  {packet,file,sniff}
    packet             Decode an HCI packet
    file               Decode HCI packets from a file
    sniff              Sniff/Decode HCI packets on a serial port (CTRL-C to exit)

optional arguments:
  -h, --help           show this help message and exit
```

The CLI can be operated in three modes: packet decoder mode, file decoder mode, and serial sniffing mode. Operation for each of these modes is described in the following sections.

### Packet Decoder Mode

The HCI decoding tools packet decoder takes a single HCI packet as input and outputs the decoded packet information. It can be accessed by running

```console
me@example ~ $ hci_decoder packet -h
usage: hci_decoder packet [-h] hci_packet

positional arguments:
  hci_packet  Hci packet to decode

optional arguments:
  -h, --help  show this help message and exit
```

**Usage Example: Reset Command**  

```console
me@example ~ $ hci_decoder packet 01030c00
PacketType=Command
Command=CONTROLLER.RESET
Length=0
Params: None
```

### File Decoder Mode

The HCI decoding tools file decoder works similarly to the packet decoder, with the exception that it takes a filepath as input and parses all HCI commands present in the file. It can be accessed by running

```console
me@example ~ $ hci_decoder file -h
usage: hci_decoder file [-h] [-t PKT_TAG] [-c2h C2H_TAG] [-h2c H2C_TAG] [-o OUTPUT_PATH] [--is-bytes] filepath

positional arguments:
  filepath              Path to the file to decode

optional arguments:
  -h, --help            show this help message and exit
  -t PKT_TAG, --tag PKT_TAG
                        Leading characters on HCI packet lines, can be used more than once
  -c2h C2H_TAG, --c2h-tag C2H_TAG
                        Leading characters on ctrl2host HCI packet lines, can replace tags
  -h2c H2C_TAG, --h2c-tag H2C_TAG
                        Leading characters on host2ctrl HCI packet lines, can replace tags
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        Specify a file in which to write output (default prints to console)
  --is-bytes            Indicate file to decode is a binary file, tags are ignored
```

**Usage Example: Text File**  

test.txt:
```
DUT>01030c00
DUT<040e0401030c00
DUT>0134200400000001
DUT<040e0401342000
DUT>011f2000
DUT<040e06011f20000000
```

```console
me@example ~ $ hci_decoder file text.txt -h2c "DUT>" -c2h "DUT<"
[Host-->Controller]
PacketType=Command
Command=CONTROLLER.RESET
Length=0
Params: None

[Controller-->Host]
PacketType=Event
EventCode=COMMAND_COMPLETE
Length=4
NumHciCommand=1
Command=CONTROLLER.RESET
Params:
    Status=SUCCESS (0)

[Host-->Controller]
PacketType=Command
Command=LE_CONTROLLER.LE_TRANSMITTER_TEST_V2
Length=4
Params:
    TX_Channel=0
    Test_Data_Length=0
    Packet_Payload=PLD_PRBS9 (0)
    PHY=LE_1M (1)

[Controller-->Host]
PacketType=Event
EventCode=COMMAND_COMPLETE
Length=4
NumHciCommand=1
Command=LE_CONTROLLER.LE_TRANSMITTER_TEST_V2
Params:
    Status=SUCCESS (0)

[Host-->Controller]
PacketType=Command
Command=LE_CONTROLLER.LE_TEST_END
Length=0
Params: None

[Controller-->Host]
PacketType=Event
EventCode=COMMAND_COMPLETE
Length=6
NumHciCommand=1
Command=LE_CONTROLLER.LE_TEST_END
Params:
    Status=SUCCESS (0)
    Num_Packets=0
```

### Serial Sniffing Mode

The HCI decoding tools CLI offers a sniffing mode which is capable of decoding HCI communication across a serial connection in real time. It can be accessed by running

```console
me@example ~ $ hci_decoder sniff -h
usage: hci_decoder sniff [-h] [-m {ctrl2host,c2h,host2ctrl,h2c,bidirectional,both}] [-o OUTPUT_FILE] [-b BAUD] [-bs {5,6,7,8}] [-p {E,M,N,O,S}] [-s {1,1.5,2}] [-t TIMEOUT] [-w WRITE_TIMEOUT] [-i INTER_BYTE_TIMEOUT] [--xonxoff] [--rtscts]
                         [--dsrdtr] [--exclusive]
                         serial_port

positional arguments:
  serial_port           Serial port to sniff

optional arguments:
  -h, --help            show this help message and exit
  -m {ctrl2host,c2h,host2ctrl,h2c,bidirectional,both}, --mode {ctrl2host,c2h,host2ctrl,h2c,bidirectional,both}
                        IO path to sniff
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Specify a file in which to write output (default prints to console)
  -b BAUD, --baudrate BAUD
                        Serial port baud rate
  -bs {5,6,7,8}, --bytesize {5,6,7,8}
                        Serial port byte size
  -p {E,M,N,O,S}, --parity {E,M,N,O,S}
                        Serial port parity (Even, Mark, None, Odd, or Space)
  -s {1,1.5,2}, --stopbits {1,1.5,2}
                        Serial port stop bits
  -t TIMEOUT, --timeout TIMEOUT
                        Read timeout in seconds, may interfere with flow control
  -w WRITE_TIMEOUT, --write-timeout WRITE_TIMEOUT
                        Write timeout in seconds, may interfere with flow control
  -i INTER_BYTE_TIMEOUT, --inter-byte-timeout INTER_BYTE_TIMEOUT
                        Inter character timeout in seconds, may interfere with flow control
  --xonxoff             Enable software flow control
  --rtscts              Enable rts/cts hardware flow control
  --dsrdtr              Enable dsr/dtr hardware flow control
  --exclusive           Set exclusive access mode
```

In order to allow for uninterrupted communication across the sniffed serial line, the serial sniffer mode will create a proxy port, which must be used as the primary serial port. See the example below for more information.  

**Usage Example: Serial Sniffer**  

In one console window, start the sniffer CLI.

```console
me@example ~ $ hci_decoder sniff /dev/ttyUSB0 -b 115200
=============================================
Sniffer Proxy Port: /dev/pts/4
=============================================

```

In a second console window, connect `max_ble_hci` to the proxy port and send an HCI command.  

```console
me@example ~ $ max_ble_hci /dev/pts/4 -b 115200
Bluetooth Low Energy HCI tool
Serial port: /dev/pts/4
8N1 115200
>>> reset
INFO - 2025-05-28 11:59:12.836623  DUT>01030c00
INFO - 2025-05-28 11:59:12.843363  DUT<040e0401030c00
StatusCode.SUCCESS
>>>
```

You should see the following output on the sniffer terminal.  

```console
me@example ~ $ hci_decoder sniff /dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O92E-if00-port0 -b 115200
=============================================
Sniffer Proxy Port: /dev/pts/4
=============================================
[Host-->Controller]
PacketType=Command
Command=CONTROLLER.RESET
Length=0
Params: None

[Controller-->Host]
PacketType=Event
EventCode=COMMAND_COMPLETE
Length=4
NumHciCommand=1
Command=CONTROLLER.RESET
Params:
    Status=SUCCESS (0)
```

Use `Ctrl-C` to exit the sniffer mode.

## Contributing

Contributions are encouraged!
Pull requests must pass all GitHub Actions unless directly waved by an admin of the repository.

### Python Versioning

This package is designed to support Python 3.8 and up. Non backwards compatible features will not be accepted (ex Use of match which was introduced in 3.10)

### Style Guidlines

MAX-BLE-HCI is formatted using the Black formatter.
It can be installed via pip using ```pip install black```
