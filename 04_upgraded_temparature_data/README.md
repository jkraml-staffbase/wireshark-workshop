# Temperature Data

An upgrade of the simple UDP temperature protocol from example 1.

## Old Format

This is the old format, we want as good compatibility as possible.
We'll have to break compatibility in some small way, so we define that a sensor ID of 0xFF is invalid and will serve as the marker for the new format.

| 1 byte    | 4 bytes                    |
|-----------|----------------------------|
| uint8     | float32 (big-endian)       |
| Sensor ID | Measured temperature in °C |

## New Format

The new format can accommodate more sensors and contains a reserved byte for future upgrades.
The first byte is also reserved and carries the fixed value 0xFF to indicate the new format.

Data in this format will show as sensor ID 0xFF for recipients only processing the old format.
The temperature value will likely be nonsensical.

| 1 byte      | 1 byte   | 2 bytes   | 4 bytes                    |
|-------------|----------|-----------|----------------------------|
| --          | --       | uint16    | float32 (big-endian)       |
| always 0xFF | reserved | Sensor ID | Measured temperature in °C |

## Files

- `upgraded_temperature.py`: Python script for sending and receiving temperature data (no requirements, should "just work"
  with Python 3)
- `upgraded_temperature.lua`: Wireshark dissector for this protocol, registers for UDP port 4567
- `dump.pcap`: Example capture file, with mixed old and new format packets
