Link Control Commands
=====================

Disconnect
----------

Terminate an existing connection.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - DISCONNECT
      - 0x0006
      - | Connection_Handle
        | Reason
      -

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Indicates which connection is to be disconnected

.. list-table:: Reason, size = 1 octet
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - | 0x05
        | 0x13 to 0x15
        | 0x1A
        | 0x29
        | 0x3B
      - | Reason for ending the connection. Available reasons:
        | Authentication Failure (0x5)
        | Other End Terminated Connection (0x13 to 0x15)
        | Unsupported Remote Feature (0x1A)
        | Pairing with Unit Key Not Supported (0x29)
        | Unacceptable Connection Parameters (0x3B)

Return Parameters
`````````````````

None.

Event(s) Generated
``````````````````

- COMMAND\_STATUS
- DICON\_COMPLETE
- LE\_META
    - CIS\_ESTABLISHED (if issued for CIS before CIS is finished establishing)


Read Remote Version Information
-------------------------------

Obtain version information values from a remote device.

.. list-table::
    :width: 100%
    :widths: 30 10 30 30
    :header-rows: 1

    * - Command
      - OCF
      - Command Parameters
      - Return Parameters
    * - READ_REMOTE_VER_INFO
      - 0x001D
      - Connection_Handle
      -

Parameters
``````````

.. list-table:: Connection_Handle, size = 2 octets
    :width: 100%
    :widths: 20 80
    :header-rows: 1

    * - Value(s)
      - Parameter Description
    * - 0x0000 to 0x0EFF
      - Indicates which connection to obtain version info from

Return Parameters
`````````````````

None.

Event(s) Generated
``````````````````

- COMMAND\_STATUS
- READ\_REMOTE\_VERSION\_INFO\_COMPLETE


