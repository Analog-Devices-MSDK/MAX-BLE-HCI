Informational Commands
======================

Read Local Version Information
------------------------------

Read the version information values for the local Controller.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_LOCAL_VER_INFO
      - 0x0001
      - 
      - | Status
        | HCI_Version
        | HCI_Subversion
        | LMP_Version
        | Company_Identifier
        | LMP_Subversion

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

.. list-table:: HCI_Version, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - HCI specification version supported by the Controller.

.. list-table:: HCI_Subversion, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Controller HCI revision, vendor-specific.

.. list-table:: LMP_Version, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Current LMP version supported by the Controller.

.. list-table:: Company_Identifier, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Company ID for the manufacturer of the Controller.

.. list-table:: LMP_Subversion, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Controller Current LMP subversion, vendor-specific.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Read Local Supported Commands
-----------------------------

Reads the list of HCI commands supported by the local Controller.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_LOCAL_SUP_CMDS
      - 0x0002
      - 
      - | Status
        | Supported_Commands

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
      - Command completed successfully.
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Supported_Commands, size = 64 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - | Bit mask for each HCI command, such that when
        | Bit X = 1: Command indicated by Bit X is supported.
        | Bit X = 0: Command indicated by Bit X is not supported.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Read Local Supported Features
-----------------------------

Reads a list of features supported by the local Controller.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_LOCAL_SUP_FEAT
      - 0x0003
      - 
      - | Status
        | LMP_Features

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
      - Command completed successfully.
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: LMP_Features, size = 8 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - | Bit mask for LMP features, such that when
        | Bit X = 1: Feature indicated by Bit X is supported
        | Bit X = 0: Feature indicated by Bit X is not supported

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Read Buffer Size
----------------

Read the maximum data size of HCI ACL and Synchronous packets
sent from the Host to the Controller.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_BUF_SIZE
      - 0x0005
      - 
      - | Status
        | ACL_Data_Packet_Length
        | Synchronous_Data_Packet_Length
        | Total_Num_ACL_Data_Packets
        | Total_Num_Synchronous_Data_Packets

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
      - Command completed successfully.
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: ACL_Data_Packet_Length, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0001 to 0xFFFF
      - Maximum length (in octets) of data for HCI ACL packets that the Controller can accept.

.. list-table:: Synchronous_Data_Packet_Length, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Maximum length (in octets) of data for HCI Synchronous packets that the Controller can accept.

.. list-table:: Total_Num_ACL_Data_Packets, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0001 to 0xFFFF
      - Total number of HCI ACL packets that can be stored in the data buffers of the Controller.

.. list-table:: Total_Num_Synchronous_Data_Packets, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0xFFFF
      - Total number of HCI Synchronous Data packets that can be stored in the data buffers of the Controller.

Event(s) Generated
```````````````````

- COMMAND_COMPLETE


Read BD_ADDR
------------

Read the Public Device Address.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_BD_ADDR
      - 0x0009
      - 
      - | Status
        | BD_ADDR

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
      - Command completed successfully.
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: BD_ADDR, size = 6 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - N/A
      - BD_ADDR of the device.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Read Local Supported Codecs
---------------------------

Read a list of the Bluetooth SIG approved codecs from the
Controller. Return parameters are organized as such:

| Status
| Num_Supported_Standard_Codecs
| Standard_Codec_ID[0]
| Standard_Codec_Transport[0]
| ...
| Standard_Codec_ID[i]
| Standard_Codec_Transport[i]
| Num_Supported_Vendor_Specific_Codecs
| Vendor_Specific_Codec_ID[0]
| Vendor_Specific_Codec_Transport[0]
| ...
| Vendor_Specific_Codec_ID[k]
| Vendor_Specific_Codec_Transport[k]

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_LOCAL_SUP_CODECS
      - 0x000D
      - 
      - | Status
        | Num_Supported_Standard_Codecs
        | Standard_Codec_ID[i]
        | Standard_Codec_Transport[i]
        | Num_Supported_Vendor_Specific_Codecs
        | Vendor_Specific_Codec_ID[k]
        | Vendor_Specific_Codec_Transport[k]

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
      - Command completed successfully.
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Num_Supported_Standard_Codecs, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Total number of codecs supported.

.. list-table:: Standard_Codec_ID, size = 1*Num_Supported_Standard_Codecs octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Codec identifier.

.. list-table:: Standard_Codec_Transport, size = 1*Num_Supported_Standard_Codecs octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Parameter Description
    * - 0
      - Codec supported over BR/EDR ACL.
    * - 1
      - Codec supported over BR/EDR SCO and eSCO.
    * - 2
      - Codec supported over LE CIS.
    * - 3
      - Codec supported over LE BIS.
    * - All other bits
      - [Reserved for future use].

.. list-table:: Num_Supported_Vendor_Specific_Codecs, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Total number of vendor-specific codecs supported.

.. list-table:: Vendor_Specific_Codec_ID, size = 4*Num_Supported_Vendor_Specific_Codecs octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Octet Number
      - Parameter Description
    * - 0 and 1
      - Company identifier.
    * - 2 and 3
      - Vendor-defined codec ID.

.. list-table:: Vendor_Specific_Codec_Transport, size = 1*Num_Supported_Vendor_Specific_Codecs octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Bit Number
      - Parameter Description
    * - 0
      - Codec supported over BR/EDR ACL.
    * - 1
      - Codec supported over BR/EDR SCO and eSCO.
    * - 2
      - Codec supported over LE CIS.
    * - 3
      - Codec supported over LE BIS.
    * - All other bits
      - [Reserved for future use].

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Read Local Supported Codec Capabilities
---------------------------------------

Read a list of capabilities supported by the controller for the
indicated codec. Return parameters are organized as such:

| Status
| Num_Codec_Capabilities
| Codec_Capability_Length[0]
| Codec_Capability[0]
| ...
| Codec_Capability_Length[i]
| Codec_Capability[i]

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_LOCAL_SUP_CODEC_CAP
      - 0x000E
      - | Codec_ID
        | Logical_Transport_Type
        | Direction
      - | Status
        | Num_Codec_Capabilities
        | Codec_Capability_Length[i]
        | Codec_Capability[i]

Parameters
``````````

.. list-table:: Codec_ID, size = 5 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Octet Number
      - Parameter Description
    * - 0
      - Codec ID, or 0xFF for vendor-specific codec.
    * - 1 to 2
      - Company ID, ignored if octet 0 is not 0xFF.
    * - 3 to 4
      - Vendor-defined codec ID, ignored if octet 0 is not 0xFF.

.. list-table:: Logical_Transport_Type, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - BR/EDR ACL
    * - 0x01
      - BR/EDR SCO or eSCO
    * - 0x02
      - LE CIS
    * - 0x03
      - LE BIS
    * - All other values
      - [Reserved for future use].

.. list-table:: Direction, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Input (Host to Controller)
    * - 0x01
      - Output (Controller to Host)

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully.
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Num_Codec_Capabilities, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Number of codec capabilities returned.

.. list-table:: Codec_Capability_Length, size = 1*Num_Codec_Capabilities octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - Length of the corresponding Codec_Capability field.

.. list-table:: Codec_Capability, size = SUM(Codec_Capability_Length) octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - Variable
      - Codec-specific capability data.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE


Read Local Supported Controller Delay
-------------------------------------

Read the range of supported Controller delays for the indicated
codec.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_LOCAL_SUP_CONTROLLER_DLY
      - 0x000F
      - | Codec_ID
        | Logical_Transport_Type
        | Direction
        | Codec_Configuration_Length
        | Codec_Configuration
      - | Status
        | Min_Controller_Delay
        | Max_Controller_Delay

Parameters
``````````

.. list-table:: Codec_ID, size = 5 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Octet Number
      - Parameter Description
    * - 0
      - Codec ID, or 0xFF for vendor-specific codec.
    * - 1 to 2
      - Company ID, ignored if octet 0 is not 0xFF.
    * - 3 to 4
      - Vendor-defined codec ID, ignored if octet 0 is not 0xFF.

.. list-table:: Logical_Transport_Type, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - BR/EDR ACL
    * - 0x01
      - BR/EDR SCO or eSCO
    * - 0x02
      - LE CIS
    * - 0x03
      - LE BIS
    * - All other values
      - [Reserved for future use].

.. list-table:: Direction, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Input (Host to Controller)
    * - 0x01
      - Output (Controller to Host)

.. list-table:: Codec_Configuration_Length, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value
      - Parameter Description
    * - 0x00 to 0xFF
      - Length of codec configuration.
    
.. list-table:: Codec_Configuration, size = Codec_Configuration_Length octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value
      - Parameter Description
    * - Variable
      - Codec-specific configuration data.

Return Parameters
`````````````````

.. list-table:: Status, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00
      - Command completed successfully.
    * - 0x01 to 0xFF
      - Command failed.

.. list-table:: Min_Controller_Delay, size = 3 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Values(s)
      - Parameter Description
    * - 0x000000 to 0x3D0900
      - | Minimum Controller delay in microseconds.
        | Time range: 0s to 4s

.. list-table:: Max_Controller_Delay, size = 3 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x000000 to 0x3D0900
      - | Maximum Controller delay in microseconds
        | Time range: 0s to 4s

Event(s) Generated
``````````````````

- COMMAND_COMPLETE
