ADI Vendor Specific Commands
============================

Write Register
--------------

Write to an address. This function has no protections and should be
used with caution.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - REG_WRITE
      - 0x0300
      - | Write_Data_Length
        | Starting_Address
        | Write_Data
      - Status

Parameters
``````````

.. list-table:: Write_Data_Length, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Length of Write_Data in octets.

.. list-table:: Starting_Address, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Address at which to start the write.

.. list-table:: Write_Data, size = Write_Data_Length octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - Variable
      - Data that should be written.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Read Register
-------------

Read from an address. This function has no protections and should be
used with caution.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - REG_READ
      - 0x0301
      - | Read_Length
        | Starting_Address
      - | Status
        | Read_Data

Parameters
``````````

.. list-table:: Read_Length, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Length of data to read in octets.

.. list-table:: Starting_Address, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Address from which to start the read.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Read_Data, size = Read_Length octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - Variable
      - Data read from the indicated address.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Reset Connection Statistics
---------------------------

Clear all connection statistics counters.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - RESET_CONN_STATS
      - 0x0302
      - 
      - Status

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Transmitter Test
----------------

Start a transmitter test.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - TX_TEST
      - 0x0303
      - | TX_Channel
        | Packet_Length
        | Packet_Payload
        | PHY
        | Num_Packets
      - Status

Parameters
``````````

.. list-table:: TX_Channel, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0x27
      - RF channel to transmit on.
    * - All other values
      - [Reserved for future use].

.. list-table:: Packet_Length, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Length of each packet in bytes.

.. list-table:: Packet_Payload, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - PRBS9 payload.
    * - 0x01
      - Repeated 11110000 payload.
    * - 0x02
      - Repeated 10101010 payload.
    * - 0x03
      - PRBS15 payload.
    * - 0x04
      - Repeated 11111111 payload.
    * - 0x05
      - Repeated 00000000 payload.
    * - 0x06
      - Repeated 00001111 payload.
    * - 0x07
      - Repeated 01010101 payload.
    * - All other values
      - [Reserved for future use].

.. list-table:: PHY, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x01
      - Use LE 1M PHY.
    * - 0x02
      - Use LE 2M PHY.
    * - 0x03
      - Use LE Coded PHY with S=8 data coding.
    * - 0x04
      - Use LE Coded PHY with S=2 data coding.
    * - All other values
      - [Reserved for future use].

.. list-table:: Num_Packets, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000
      - Transmit continuously
    * - All other values
      - Total number of packets to send over the course of the test.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Reset Test Statistics
---------------------

Clear all test statistics counters.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - RESET_TEST_STATS
      - 0x0304
      - 
      - Status

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Receiver Test
-------------

Start a receiver test.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - RX_TEST
      - 0x0305
      - | RX_Channel
        | PHY
        | Modulation_Index
        | Num_Packets
      - Status

Parameters
``````````

.. list-table:: RX_Channel, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0x27
      - RF channel to receive on.
    * - All other values
      - [Reserved for future use].

.. list-table:: PHY, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x01
      - Use LE 1M PHY.
    * - 0x02
      - Use LE 2M PHY.
    * - 0x03
      - Use LE Coded PHY
    * - All other values
      - [Reserved for future use].

.. list-table:: Modulation_Index, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Assume transmitter has a standard modulation index.
    * - 0x01
      - Assume transmitter has a stable modulation index.
    * - All other values
      - [Reserved for future use].

.. list-table:: Num_Packets, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000
      - Receive continuously
    * - All other values
      - Total number of packets expected to be received.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get RSSI
--------

Read the RSSI values for the indicated channel.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_RSSI
      - 0x0306
      - RF_Channel
      - | Status
        | RSSI_Data

Parameters
``````````

.. list-table:: RF_Channel, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0x27
      - RF channel to retrieve the RSSI value for.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RSSI_Data, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - | RSSI value for the indicated channel (signel value).
        | Range = -127dB to 127dB

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Baseband Enable
---------------

Enable the Baseband/PHY for the local device. Must be called before
the Get RSSI command can be used.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - BB_EN
      - 0x0307
      - 
      - Status

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Baseband Disable
----------------

Disable the Baseband/PHY for the local device.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - BB_DIS
      - 0x0308
      - 
      - Status

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE



Enable Sniffer Packet Forwarding
--------------------------------

Enable or disable sniffer packet forwarding.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_SNIFFER_ENABLE
      - 0x03CD
      - | Output_Method
        | Enable
      - Status

Parameters
``````````

.. list-table:: Output_Method, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Output over HCI through tokens.
    * - All other values
      - [Reserved for future use].

.. list-table:: Enable, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable sniffer packet forwarding.
    * - 0x01
      - Enable sniffer packet forwarding.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Auxiliary Delay
-------------------

Set the auxiliary packet offset delay for the indicated advertising set.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_AUX_DELAY
      - 0x03D0
      - | Advertising_Handle
        | Auxiliary_Delay
      - Status

Parameters
``````````

.. list-table:: Advertising_Handle, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xEF
      - Advertising set identifier.

.. list-table:: Auxiliary_Delay, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00000000
      - Disable.
    * - All other values
      - Additional auxiliary packet offset delay in microseconds.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Extended Advertising Fragmentation Length
---------------------------------------------

Set the data fragmentation length for the indicated extended advertising
set.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_EXT_ADV_FRAG_LEN
      - 0x03D1
      - | Advertising_Handle
        | Fragmentation_Length
      - Status

Parameters
``````````

.. list-table:: Advertising_Handle, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xEF
      - Advertising set identifier.

.. list-table:: Fragmentation_Length, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Fragmentation length.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Extended Advertising PHY Options
------------------------------------

Set the primary and secondary PHY options for the indicated extended
advertising set.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_EXT_ADV_PHY_OPTS
      - 0x03D2
      - | Advertising_Handle
        | Primary_PHY_Opts
        | Secondary_PHY_Opts
      - Status

Parameters
``````````

.. list-table:: Advertising_Handle, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xEF
      - Advertising set identifier.

.. list-table:: Primary_PHY_Opts, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x01
      - S=2 coding preferred when transmitted on LE Coded PHY.
    * - 0x02
      - S=8 coding preferred when transmitted on LE Coded PHY.
    * - All other values
      - [Reserved for future use].

.. list-table:: Secondary_PHY_Opts, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x01
      - S=2 coding preferred when transmitted on LE Coded PHY.
    * - 0x02
      - S=8 coding preferred when transmitted on LE Coded PHY.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Extended Advertising Default PHY Options
--------------------------------------------

Set the default PHY options for extended advertising.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_EXT_ADV_DEF_PHY_OPTS
      - 0x03D3
      - PHY_Options
      - Status

Parameters
``````````

.. list-table:: PHY_Options, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x01
      - S=2 coding preferred when transmitted on LE Coded PHY.
    * - 0x02
      - S=8 coding preferred when transmitted on LE Coded PHY.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Generate ISO
------------

Request that ISO packets be generated on the indicated connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GENERATE_ISO
      - 0x03D5
      - | Connection_Handle
        | Packet_Length
        | Num_Packets
      - Status

Parameters
``````````
.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.

.. list-table:: Packet_Length, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Length of each packet in bytes.

.. list-table:: Num_Packets, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Total number of packets to send over the course of the test.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get ISO Test Report
-------------------

Retrieve statistics captured in ISO test mode.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_ISO_TEST_REPORT
      - 0x03D6
      - 
      - | Status
        | RX_ISO_Packet_Count
        | RX_ISO_Octet_Count
        | Gen_ISO_Packet_Count
        | Gen_ISO_Octet_Count

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_ISO_Packet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of received ISO packets.

.. list-table:: RX_ISO_Octet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of received ISO octets.

.. list-table:: Gen_ISO_Packet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of generated ISO packets.

.. list-table:: Gen_ISO_Octet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of generated ISO octets.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Enable ISO Sink
---------------

Enable or disable ISO packet sink.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - ENA_ISO_SINK
      - 0x03D7
      - Enable
      - Status

Parameters
``````````

.. list-table:: Enable, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable ISO sink.
    * - 0x01
      - Enable ISO sink.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Enable Auto Generate ISO
------------------------

Enable or disable automatic generation of ISO packets.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - ENA_AUTO_GEN_ISO
      - 0x03D8
      - Packet_Length
      - Status

Parameters
``````````

.. list-table:: Packet_Length, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000
      - Disable.
    * - 0x0001 to 0xFFFF
      - Packet length for auto generated ISO packets.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get CIS Statistics
------------------

Retrieve statistics for a CIS.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_CIS_STATS
      - 0x03D9
      - 
      - | Status
        | RX_Data_OK
        | RX_Data_CRC
        | RX_Data_Timeout
        | TX_Data
        | TX_Data_Err
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_Data_OK, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received packets.

.. list-table:: RX_Data_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of packets received with a CRC error.

.. list-table:: RX_Data_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of receive timeouts.

.. list-table:: TX_Data, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of packets sent.

.. list-table:: TX_Data_Err, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of data transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Auxiliary Advertising Statistics
------------------------------------

Retrieve accumulated auxiliary advertising statistics.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_AUX_ADV_STATS
      - 0x03DA
      - 
      - | Status
        | TX_Adv
        | RX_Req
        | RX_Req_CRC
        | RX_Req_Timeout
        | TX_Rsp
        | TX_Chain
        | TX_Adv_Error
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: TX_Adv, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of sent advertising packets.

.. list-table:: RX_Req, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received advertising requests.

.. list-table:: RX_Req_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising requests received with a CRC error.

.. list-table:: RX_Req_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of request receive timeouts.

.. list-table:: TX_Rsp, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of sent response packets.

.. list-table:: TX_Chain, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of sent chain packets.

.. list-table:: TX_Adv_Error, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Auxiliary Scan Statistics
-----------------------------

Retrieve accumulated auxiliary scanning statistics.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_AUX_SCAN_STATS
      - 0x03DB
      - 
      - | Status
        | RX_Adv
        | RX_Adv_CRC
        | RX_Adv_Timeout
        | TX_Req
        | RX_Rsp
        | RX_Rsp_CRC
        | RX_Rsp_Timeout
        | RX_Chain
        | RX_Chain_CRC
        | RX_Chain_Timeout
        | Scan_Error
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_Adv, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received advertising packets.

.. list-table:: RX_Adv_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising packets received with a CRC error.

.. list-table:: RX_Adv_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of receive timeouts.

.. list-table:: TX_Req, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of sent advertising requests.

.. list-table:: RX_Rsp, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received advertising response packets.

.. list-table:: RX_Rsp_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising response packets received with a CRC error.

.. list-table:: RX_Rsp_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of response receive timeout.

.. list-table:: RX_Chain, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received chain packets.

.. list-table:: RX_Chain_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of chain packets received with a CRC error.

.. list-table:: RX_Chain_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of chain receive timeouts.

.. list-table:: Scan_Error, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of scan transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.


Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Periodic Scanning Statistics
--------------------------------

Retrieve accumulated periodic scanning statistics.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_PER_SCAN_STATS
      - 0x03DC
      - 
      - | Status
        | RX_Adv
        | RX_Adv_CRC
        | RX_Adv_Timeout
        | RX_Chain
        | RX_Chain_CRC
        | RX_Chain_Timeout
        | Scan_Errors
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_Adv, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received advertising packets.

.. list-table:: RX_Adv_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising packets received with a CRC error.

.. list-table:: RX_Adv_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of receive timeouts.

.. list-table:: RX_Chain, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received chain packets.

.. list-table:: RX_Chain_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of chain packets received with a CRC error.

.. list-table:: RX_Chain_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of chain receive timeouts.

.. list-table:: Scan_Errors, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of scan transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Connection PHY TX Power
---------------------------

Set the TX power level for a specific PHY on the indicated connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_CONN_PHY_TX_PWR
      - 0x03DD
      - | Connection_Handle
        | TX_Power_Level
        | PHY
      - Status

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.

.. list-table:: TX_Power_Level, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - | TX power level to set for the indicated PHY (signed value).
        | Range = -127dBm to 20dBm

.. list-table:: PHY, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x01
      - LE 1M PHY.
    * - 0x02
      - LE 2M PHY.
    * - 0x03
      - LE Coded PHY
    * - All other values
      - [Reserved for future use].


Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Periodic Scanning/Advertising Channel Map
---------------------------------------------

Read the channel map used during periodic scanning and/or advertising.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_PER_CHAN_MAP
      - 0x03DE
      - | Handle
        | Is_Advertising
      - | Status
        | Channel_Map

Parameters
``````````

.. list-table:: Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Advertising or scanning handle. Must be 2 octets regardless of the indicated role.

.. list-table:: Is_Advertising, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Handle indicates a scanner.
    * - 0x01
      - Handle indicates an advertiser.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Channel_Map, size = 5 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - | Periodic advertising or scanning channel map such that when
        | Bit X = 0: Channel X is not in use.
        | Bit X = 1: Channel X is in use.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Scan Channel Map
--------------------

Specify the channel map used for scanning.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_SCAN_CH_MAP
      - 0x03E0
      - Channel_Map
      - Status

Parameters
``````````

.. list-table:: Channel_Map, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Parameter Description
    * - 0
      - Use channel 37 (possibly among others).
    * - 1
      - Use channel 38 (possibly among others).
    * - 2
      - Use channel 39 (possibly among others).
    * - All other bits
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Event Mask
--------------

Control which vendor-specific events are generated by the HCI for the host.
Setting a bit to 1 enables the corresponding event.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_EVENT_MASK
      - 0x03E1
      - | Event_Mask
        | Enable
      - Status

Parameters
``````````

.. list-table:: Event_Mask, size = 8 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Event
    * - 0
      - Scan Report
    * - 1
      - Diagnostic Trace
    * - All other bits
      - [Reserved for future use].

.. list-table:: Enable, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable indicated events.
    * - 0x01
      - Enable indicated events.
    * - All other values
      - [Reserved for future use].


Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Enable ACL Sink
---------------

Enable or disable asynchronous connection-oriented logical transport.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - ENA_ACL_SINK
      - 0x03E3
      - Enable
      - Status

Parameters
``````````

.. list-table:: Enable, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable ACL sink.
    * - 0x01
      - Enable ACL sink.
    * - All other values
      - [Reserved for future use].


Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Generate ACL
------------

Generate ACL packets for the indicated connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GENERATE_ACL
      - 0x03E4
      - | Connection_Handle
        | Packet_Length
        | Num_Packets
      - Status

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.

.. list-table:: Packet_Length, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Length of each packet in bytes.

.. list-table:: Num_Packets, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Total number of packets to send over the course of the test.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Enable Auto Generate ACL
------------------------

Enable or disable automatic generation of ACL packets.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - ENA_AUTO_GEN_ACL
      - 0x03E5
      - Packet_Length
      - Status

Parameters
``````````

.. list-table:: Packet_Length, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000
      - Disable.
    * - 0x0001 to 0xFFFF
      - Length of each packet in bytes.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set TX Test Error Pattern
-------------------------

Set the patter of errors for TX test mode.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_TX_TEST_ERR_PATT
      - 0x03E6
      - Error_Pattern
      - Status

Parameters
``````````

.. list-table:: Error_Pattern, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - | TX test error pattern such that for each bit in the pattern
        | 0s = CRC failure
        | 1s = No error

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Connection Operational Flags
--------------------------------

Enable or disable the operational flags for the indicated connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_CONN_OP_FLAGS
      - 0x03E7
      - | Connection_Handle
        | Flags
        | Enable
      - Status

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.

.. list-table:: Flags, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Parameter Description
    * - 0
      - [Reserved for future use].
    * - 1
      - Peripheral Controller requires immediate ACK.
    * - 2
      - Bypass end CE guard.
    * - 3
      - Central Controller retransmits after receiving NACK.
    * - 4
      - Central Controller ignores LL Connection Parameter Responses.
    * - 5
      - Central Controller unconditionally accepts LL Connection Parameter Responses.
    * - 6
      - [Reserved for future use].
    * - 7
      - Require symmetric PHYs for connection.
    * - 8
      - [Reserved for future use].
    * - 9
      - [Reserved for future use].
    * - 10
      - Enable Peripheral Controller latency wake up upon data pending.
    * - 11
      - [Reserved for future use].
    * - 12
      - [Reserved for future use].
    * - 13
      - [Reserved for future use].
    * - 14
      - [Reserved for future use].
    * - 15
      - [Reserved for future use].
    * - 16
      - [Reserved for future use].
    * - 17
      - [Reserved for future use].
    * - 18
      - Enable window widening.
    * - 19
      - Enable Peripheral Controller latency.
    * - 20
      - Enable LLCP timer.
    * - 21
      - Ignore timestamp of RX packets with a CRC error.
    * - All other bits
      - [Reserved for future use].


.. list-table:: Enable, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable indicated flags.
    * - 0x01
      - Enable indicated flags.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set P-256 Private Key
---------------------

Set or clear the P-256 private key. The private key is used for generating key
pairs and Diffie-Hellman keys until cleared.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_P256_PRIV_KEY
      - 0x03E8
      - Private_Key
      - Status

Parameters
``````````
.. list-table:: Private_Key, size = 32 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Clear private key.
    * - All other values
      - P-256 private key.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get ACL Test Report
-------------------

Retrieve the values stored ACL test counters.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_ACL_TEST_REPORT
      - 0x03E9
      - 
      - | Status
        | RX_ACL_Packet_Count
        | RX_ACL_Octet_Count
        | Gen_ACL_Packet_Count
        | Gen_ACL_Octet_Count


Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_ACL_Packet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of received ACL packets.

.. list-table:: RX_ACL_Octet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of received ACL octets.

.. list-table:: Gen_ACL_Packet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of generated ACL packets.

.. list-table:: Gen_ACL_Octet_Count, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of generated ACL octets.


Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Local Minimum Number of Used Channels
-----------------------------------------

Specify the local minimum number of used channels.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_LOCAL_MIN_USED_CHAN
      - 0x03EA
      - | PHYs
        | Power_Thresh
        | Min_Used_Channels
      - Status

Parameters
``````````

.. list-table:: PHYs, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Parameter Description
    * - 0
      - Set for LE 1M PHY (possibly among others).
    * - 1
      - Set for LE 2M PHY (possibly among others).
    * - 2
      - Set for LE Coded PHY (possibly among others).
    * - All other bits
      - [Reserved for future use].

.. list-table:: Power_Thresh, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - | Power threshold for PHYs (signed value).
        | Range = -127dBm to 127dBm

.. list-table:: Min_Used_Channels, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x02 to 0x25
      - | Minimum number of used channels.
        | Range = 2 to 37
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Peer Minimum Number of Used Channels
----------------------------------------

Read the peer device minimum number of used channels for the indicated connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_PEER_MIN_USED_CHAN
      - 0x03EB
      - Connection_Handle
      - | Status
        | Peer_Min_Used_LE1M
        | Peer_Min_Used_LE2M
        | Peer_Min_Used_LECoded

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.


Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Peer_Min_Used_LE1M, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x02 to 0x25
      - | Peer minimum number of used channels for LE 1M PHY.
        | Range = 2 to 37

.. list-table:: Peer_Min_Used_LE1M, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x02 to 0x25
      - | Peer minimum number of used channels for LE 2M PHY.
        | Range = 2 to 37

.. list-table:: Peer_Min_Used_LECoded, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x02 to 0x25
      - | Peer minimum number of used channels for LE Coded PHY.
        | Range = 2 to 37

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Validate Public Key Mode
----------------------------

Specify the mode used to validate public keys.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - VALIDATE_PUB_KEY_MODE
      - 0x03EC
      - Validate_Mode
      - Status

Parameters
``````````

.. list-table:: Validate_Mode, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Set validation mode to ALT2.
    * - 0x01
      - Set validation mode to ALT1.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set BD_ADDR
-----------

Specify the local device BD_ADDR.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_BD_ADDR
      - 0x03F0
      - BD_ADDR
      - Status

Parameters
``````````

.. list-table:: BD_ADDR, size = 6 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Device BD_ADDR.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Random Address
------------------

Read the local Random Address.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_RAND_ADDR
      - 0x03F1
      - 
      - | Status
        | Random_Address

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Random_Address, size = 6 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x000000000000
      - Random address not set.
    * - All other values.
      - Random address currently used by the local device.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Local Feature
-----------------

Enable or disable local device supported features.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_LOCAL_FEAT
      - 0x03F2
      - Feature_Mask
      - Status

Parameters
``````````

.. list-table:: Feature_Mask, size = 8 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Feature
    * - 0
      - Encryption
    * - 1
      - Connection Parameters Request Procedure
    * - 2
      - Extended Reject Indication
    * - 3
      - Peripheral-Initiatred Features Exchange
    * - 4
      - LE Ping
    * - 5
      - Data Length Extension
    * - 6
      - LL Privacy
    * - 7
      - Extended Scan Filter Policy
    * - 8
      - LE 2M PHY
    * - 9
      - Stable Modulation Index - Transmitter
    * - 10
      - Stable Modulation Index - Receiver
    * - 11
      - LE Coded PHY
    * - 12
      - LE Extended Advertising
    * - 13
      - LE Periodic Advertising
    * - 14
      - Channel Selection Algorithm #2
    * - 15
      - LE Power Class 1
    * - 16
      - Minimum Number of Used Channels
    * - 17 to 26
      - [Reserved for future use].
    * - 27
      - Remote Public Key Validation
    * - All other bits
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Operational Flags
---------------------

Enable or disable operational flags.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_OP_FLAGS
      - 0x03F3
      - | Operational_Flags
        | Enable
      - Status

Parameters
``````````

.. list-table:: Operational_Flags, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Parameter Description
    * - 0
      - Perform version exchange LLCP at connection establishment.
    * - 1
      - Peripheral Controller requires immediate ACK.
    * - 2
      - Bypass end of CE guard.
    * - 3
      - Central Controller retransmits after receiving NACK
    * - 4
      - Central Controller ignores LL Connection Parameter response.
    * - 5
      - Central controller unconditionally accepts LL Connection Parameter response.
    * - 6
      - Perform data length update LLCP at connection establishment.
    * - 7
      - Require symmetric PHYs for connection.
    * - 8
      - Perform feature exchange LLCP at connection establishment.
    * - 9
      - Peripheral Controller delays LLCP startup procedures.
    * - 10
      - Enable Peripheral Controller latency wake up upon data pending.
    * - 11
      - Enable ADI field for auxiliary scan responses.
    * - 12
      - Enable CIS master sends additional NULL PDU for ACK scheme.
    * - 13
      - Include AdvA in AUX_ADV_IND instead of ADV_EXT_IND.
    * - 14
      - Enable advertising channel randomization.
    * - 15
      - Disable power monitoring.
    * - 16
      - Enable advertising delay.
    * - 17
      - Enable scan backoff.
    * - 18
      - Enable window widening.
    * - 19
      - Enable Peripher Controller latency.
    * - 20
      - Enable LLCP timer.
    * - 21
      - Ignore timestamp of RX packets with a CRC error.
    * - 22
      - Close connection event on receiving a CRC error.
    * - All other bits
      - [Reserved for future use].

.. list-table:: Enable, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable indicated flags.
    * - 0x01
      - Enable indicated flags.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get PDU Filter Statistics
-------------------------

Retrieve accumulated PDU filter statistics.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_PDU_FILT_STATS
      - 0x03F4
      - 
      - | Status
        | Fail_PDU_Type_Filter_Count
        | Pass_PDU_Type_Filter_Count
        | Fail_Whitelist_Filter_Count
        | Pass_Whitelist_Filter_Count
        | Fail_Peer_Address_Match_Count
        | Pass_Peer_Address_Match_Count
        | Fail_Local_Address_Match_Count
        | Pass_Local_Address_Match_Count
        | Fail_Peer_RPA_Verify_Count
        | Pass_Peer_RPA_Verify_Count
        | Fail_Local_RPA_Verify_Count
        | Pass_Local_RPA_Verify_Count
        | Fail_Peer_Private_Addr_Req_Count
        | Fail_Local_Private_Addr_Req_Count
        | Fail_Peer_Addr_Resolution_Req_Count
        | Pass_Peer_Addr_Resolution_Opt_Count
        | Pass_Local_Addr_Resolution_Opt_Count
        | Peer_Addr_Resolutions_Pend_Count
        | Local_Addr_Resolutions_Pend_Count

Parameters
``````````
None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Fail_PDU_Type_Filter_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs failing PDU type filter.

.. list-table:: Pass_PDU_Type_Filter_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs passing PDU type filter.

.. list-table:: Fail_Whitelist_Filter_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs failing whitelist filter.

.. list-table:: Pass_Whitelist_Filter_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs passing whitelist filter.

.. list-table:: Fail_Peer_Address_Match_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs failing peer address match.

.. list-table:: Pass_Peer_Address_Match_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs passing peer address match.

.. list-table:: Fail_Local_Address_Match_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs failing local address match.

.. list-table:: Pass_Local_Address_Match_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs passing local address match.

.. list-table:: Fail_Peer_RPA_Verify_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of peer RPAs failing verification.

.. list-table:: Pass_Peer_RPA_Verify_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of peer RPAs passing verification.

.. list-table:: Fail_Local_RPA_Verify_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of local RPAs failing verification.

.. list-table:: Pass_Local_RPA_Verify_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of local RPAs passing verification.

.. list-table:: Fail_Peer_Private_Addr_Req_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of peer addresses failing RPA requirements.

.. list-table:: Fail_Local_Private_Addr_Req_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of local addresses failing RPA requirements.

.. list-table:: Fail_Peer_Addr_Resolution_Req_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs failing required peer address resolution.

.. list-table:: Pass_Peer_Addr_Resolution_Opt_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs passing optional peer address resolution.

.. list-table:: Pass_Local_Addr_Resolution_Opt_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of PDUs passing optional local address resolution.

.. list-table:: Peer_Addr_Resolutions_Pend_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of peer address resolutions pended.

.. list-table:: Local_Addr_Resolutions_Pend_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of local address resolutions pended.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Advertising TX Power
------------------------

Specify the TX power used when advertising.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_ADV_TX_PWR
      - 0x03F5
      - TX_Power_Level
      - Status

Parameters
``````````

.. list-table:: TX_Power_Level, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - | Advertising TX power level (signed value).
        | Range = -127dBm to 6dBm

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.


Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Connection TX Power
-----------------------

Specify the TX power used in connections.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_CONN_TX_PWR
      - 0x03F6
      - | Connection_Handle
        | TX_Power_Level
      - Status

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.

.. list-table:: TX_Power_Level, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - | Connection TX power level (signed value).
        | Range = -127dBm to 6dBm

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.


Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Encryption Mode
-------------------

Set the encryption mode for the indicated connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_ENC_MODE
      - 0x03F7
      - | Connection_Handle
        | Enable_Authentication
        | Nonce_Mode
      - Status

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.

.. list-table:: Enable_Authentication, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable authentication.
    * - 0x01
      - Enable authentication.
    * - All other values
      - [Reserved for future use].

.. list-table:: Nonce_Mode, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Do not use Nonce mode.
    * - 0x01
      - Use Nocne mode.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Channel Map
---------------

Set the channel map for the indicated connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_CHAN_MAP
      - 0x03F8
      - | Connection_Handle
        | Channel_Map
      - Status

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection identifier.

.. list-table:: Channel_Map, size = 5 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - | Channel map to use such that when
        | Bit X = 0: Channel X is masked out.
        | Bit X = 1: Channel X is included.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Set Diagnostice Mode
--------------------

Enable or disable the PAL System Assert Trap

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - SET_DIAG_MODE
      - 0x03F9
      - Enable
      - Status

Parameters
``````````

.. list-table:: Enable, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Disable System Assert Trap.
    * - 0x01
      - Enable System Assert Trap.
    * - All other values
      - [Reserved for future use].

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get System and Memory Statistics
--------------------------------

Retrieve device system and memory statistics.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_SYS_STATS
      - 0x03FA
      - 
      - | Status
        | Stack_Watermark
        | System_Assert_Count
        | Free_Memory
        | Used_Memory
        | Max_Connections
        | Connection_Context_Size
        | CS_Watermark_Usec
        | LL_Handler_Watermark_Usec
        | Sch_Handler_Watermark_Usec
        | LHCI_Handler_Watermark_Usec
        | Max_Advertising_Sets
        | Advertising_Set_Context_Size
        | Max_Extended_Scanners
        | Extended_Scanner_Context_Size
        | Max_Extended_Initiators
        | Extended_Initiator_Context_Size
        | Max_Periodic_Scanners
        | Periodic_Scanner_Context_Size
        | Max_CIGs
        | CIG_Context_Size
        | Max_CISes
        | CIS_Context_Size

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Stack_Watermark, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Amount of memory used by the stack in bytes.

.. list-table:: System_Assert_Count, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of assertion hits.
    

.. list-table:: Free_Memory, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Amount of heap memory free in bytes.

.. list-table:: Used_Memory, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Amount of heap memory used in bytes.

.. list-table:: Max_Connections, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Maximum number of connections allowed.

.. list-table:: Connection_Context_Size, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Size of the connection context in bytes.

.. list-table:: CS_Watermark_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Critical Section duration watermark in microseconds.

.. list-table:: LL_Handler_Watermark_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - LL Handler duration watermark in microseconds.

.. list-table:: Sch_Handler_Watermark_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Schedule handler duration watermark in microseconds.

.. list-table:: LHCI_Handler_Watermark_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - LHCI Handler duration watermark in microseconds.

.. list-table:: Max_Advertising_Sets, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Maximum number of advertising sets allowed.

.. list-table:: Advertising_Set_Context_Size, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Size of the advertising set context in bytes.

.. list-table:: Max_Extended_Scanners, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Maximum number of extended scanners allowed.

.. list-table:: Extended_Scanner_Context_Size, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Size of the extended scanner context in bytes.

.. list-table:: Max_Extended_Initiators, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Maximum number of extended initiators allowed.

.. list-table:: Extended_Initiator_Context_Size, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Size of the extended initiator context in bytes.

.. list-table:: Max_Periodic_Scanners, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Maximum number of periodic scanners allowed.

.. list-table:: Periodic_Scanner_Context_Size, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Size of the period scanner context in bytes.

.. list-table:: Max_CIGs, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Maximum number of CIGs allowed.

.. list-table:: CIG_Context_Size, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Size of the CIG context in bytes.

.. list-table:: Max_CISes, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Maximum number of CISes allowed.

.. list-table:: CIS_Context_Size, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Size of the CIS context in bytes.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Advertising Statistics
--------------------------

Retrieve accumulated advertising statistics.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_ADV_STATS
      - 0x03FB
      - 
      - | Status
        | TX_Adv
        | RX_Req
        | RX_Req_CRC
        | RX_Req_Timeout
        | TX_Rsp
        | TX_Adv_Error
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: TX_Adv, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of sent advertising packets.

.. list-table:: RX_Req, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received advertising requests.

.. list-table:: RX_Req_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising requests received with a CRC error.

.. list-table:: RX_Req_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of request receive timeouts.

.. list-table:: TX_Rsp, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of sent response packets.

.. list-table:: TX_Adv_Error, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Scan Statistics
-------------------

Retrieve statistics captured during scanning.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_SCAN_STATS
      - 0x03FC
      - 
      - | Status
        | RX_Adv
        | RX_Adv_CRC
        | RX_Adv_Timeout
        | TX_Req
        | RX_Rsp
        | RX_Rsp_CRC
        | RX_Rsp_Timeout
        | Scan_Error
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_Adv, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received advertising packets.

.. list-table:: RX_Adv_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising packets received with a CRC error.

.. list-table:: RX_Adv_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of receive timeouts.

.. list-table:: TX_Req, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of sent advertising requests.

.. list-table:: RX_Rsp, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received advertising response packets.

.. list-table:: RX_Rsp_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of advertising response packets received with a CRC error.

.. list-table:: RX_Rsp_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of response receive timeout.

.. list-table:: Scan_Error, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of scan transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Connection Statistics
-------------------------

Retrieve statistics captured during a connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_CONN_STATS
      - 0x03FD
      - 
      - | Status
        | RX_Data_OK
        | RX_Data_CRC
        | RX_Data_Timeout
        | TX_Data
        | TX_Data_Err
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_Data_OK, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received packets.

.. list-table:: RX_Data_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of packets received with a CRC error.

.. list-table:: RX_Data_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of receive timeouts.

.. list-table:: TX_Data, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of packets sent.

.. list-table:: TX_Data_Err, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of data transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Test Statistics
-------------------

Retrieve the statistics captured during Test Mode.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_TEST_STATS
      - 0x03FE
      - 
      - | Status
        | RX_Data_OK
        | RX_Data_CRC
        | RX_Data_Timeout
        | TX_Data
        | TX_Data_Err
        | RX_Setup_Usec
        | TX_Setup_Usec
        | RX_ISR_Usec
        | TX_ISR_Usec

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: RX_Data_OK, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of successfully received packets.

.. list-table:: RX_Data_CRC, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of packets received with a CRC error.

.. list-table:: RX_Data_Timeout, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of receive timeouts.

.. list-table:: TX_Data, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of packets sent.

.. list-table:: TX_Data_Err, size = 4 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - Number of data transaction errors.

.. list-table:: RX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX packet setup watermark in microseconds.

.. list-table:: TX_Setup_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX packet setup watermark in microseconds.

.. list-table:: RX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - RX ISR processing watermark in microseconds.

.. list-table:: TX_ISR_Usec, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - TX ISR processing watermark in microseconds.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Get Memory Pool Statistics
--------------------------

Retrieve accumulated memory pool statistics. Return parameters are organized as
such:

| Status
| Num_Pools
| Buffer_Size[0]
| Num_Buffers[0]
| Num_Alloc[0]
| Max_Alloc[0]
| Max_Req_Buffer_Size[0]
| ...
| Buffer_Size[i]
| Num_Buffers[i]
| Num_Alloc[i]
| Max_Alloc[i]
| Max_Req_Buffer_Size[i]

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - GET_POOL_STATS
      - 0x03FF
      - 
      - | Status
        | Num_Pools
        | Buffer_Size[i]
        | Num_Buffers[i]
        | Num_Alloc[i]
        | Max_Alloc[i]
        | Max_Req_Buffer_Size[i]

Parameters
``````````

None.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Num_Pools, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Number of defined pools.

.. list-table:: Buffer_Size, size = 2*Num_Pools octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Pool buffer size in bytes.

.. list-table:: Num_Buffers, size = 1*Num_Pools octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Total number of buffers.

.. list-table:: Num_Alloc, size = 1*Num_Pools octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Number of outstanding allocations.

.. list-table:: Max_Alloc, size = 1*Num_Buffers octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Maximum number of allocations.

.. list-table:: Max_Req_Buffer_Size, size = 2*Num_Pools octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Maximum requested buffer size in bytes.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE
