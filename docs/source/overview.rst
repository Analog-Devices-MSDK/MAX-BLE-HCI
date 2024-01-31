Overview
========

The MAX BLE HCI python library houses an implementation for
a standard BLE Host-Controller Interface (HCI). The implementation
contains:

    - Serializers/deserializers for all BLE-standard HCI packet types
    - Definitions for BLE-standard constants such as PHY type, address type, payload type, etc.
    - Opcode Group Field (OGF) and Opcode Command Field (OCF) definitions for all standard HCI commands.
    - OCF and OGF definitions for all Analog Devices vendor specific commands
    - Convenience functions for many common HCI commands
    - Support for the creation/use of custom vendor-specific commands.

Documentation for the library can be viewed in full in the :doc:`API Reference <modules>` tab.

Host-Controller Interface
-------------------------

A host controller interface is a thin layer used in BT and BLE which transports
packets from the host to the controller (commands) and vice versa (events). HCI
interface is standardized by the `Bluetooth SIG Spec`_.

.. image:: /images/ble_stack_diagram.jpeg
    :width: 100%

MAX BLE HCI Library Structure
-----------------------------
The MAX BLE HCI library is organized into modules as follows:

    - **ble_hci**: Contains the full HCI implementation. Important members:
        - *BleHci* -- HCI implementation, class
    - **contants**: Contains BLE-standard HCI constants. Important members:
        - *Endian* -- Endianness definitions, enum
        - *PhyOption* -- PHY type definitions, enum
        - *PayloadOption* -- Payload type definitions, enum
        - *AddrType* -- Address type definitions, enum
    - **data_params**: Contains data classes for select HCI parameters/returns. Important members:
        - *AdvParams* -- Container for advertising parameters, dataclass
        - *ScanParams* -- Container for scan parameters, dataclass
        - *ConnParams* -- Container for connection parameters, dataclass
    - **hci_packets**: Contains HCI packet serializers/deserializers. Important members:
        - *CommandPacket* -- HCI command packet serializer, class
        - *EventPacket* -- HCI event packet deserializer, class
    - **packet_codes**: Contains BLE-standard HCI packet codes. Important members:
        - *EventCode* -- HCI event return codes, enum
        - *StatusCode* -- HCI event status codes, enum
    - **packet_defs**: Contains BLE-standard HCI packet definitions. Important members:
        - *PacketType* -- HCI packet types, enum
        - *OGF* -- HCI Opcode Group Fields, enum
        - *OCF* -- HCI Opcode Command Fields, dataclass

.. note::

    Not all members of a module are necessarily displayed here. See the :doc:`API Reference <modules>` tab
    to view all members of each library module.

Support Information
-------------------
Supported OS
````````````
- Windows
- Linux
- MacOS

Supported Parts
```````````````
- Vendor specific commands:
    - MAX32655
    - MAX32665
    - MAX32690
- BLE standard commands:
    - Any BLE-enabled chip

.. _`Bluetooth SIG Spec`: https://www.bluetooth.com/specifications/specs/core-specification-5-3/