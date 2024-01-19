Status Commands
===============

Read RSSI
---------

Read the Received Signal Strength Indication (RSSI) from the
Controller.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_RSSI
      - 0x0005
      - Handle
      - | Status
        | Handle
        | RSSI

Parameters
``````````

.. list-table:: Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection handle for which the RSSI should be read.

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

.. list-table:: Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Connection handle for which RSSI has been read.

.. list-table:: RSSI, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x00 to 0xFF
      - | RSSI (signed value).
        | Range: -127dBm to 20dBm, 127 if invalid.

Event(s) Generated
``````````````````

- COMMAND_COMPLETE