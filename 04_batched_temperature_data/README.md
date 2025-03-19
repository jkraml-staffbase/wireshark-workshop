# Multiple Temperature Measurements

An upgrade of the simple UDP temperature protocol from example 1: batched data.

## Old Format

This is the old format, we want as good compatibility as possible.
We'll have to break compatibility in some small way, so we define that a sensor ID of 0xFF is invalid and will serve as the marker for the new format.

| 1 byte    | 4 bytes                    |
|-----------|----------------------------|
| uint8     | float32 (big-endian)       |
| Sensor ID | Measured temperature in °C |

## New Format

The new format can accommodate multiple measurements (think of a gateway transmitting data in batches or a single device with multiple sensors).
The first byte carries the fixed value 0xFF to indicate the new format and what would have been a 4-byte measurement is now a 4-byte count.

Data in this format will show as sensor ID 0xFF for recipients only processing the old format.
The temperature value will be usually won't make sense - for small counts it will be interpreted as close to zero.

| 1 byte      | 4 bytes | n * 5 bytes |
|-------------|---------|-------------|
| --          | uint32  | old PDU     |
| always 0xFF | count   | Measurement |

## Files

- `multi_temperature.py`: Python script for sending and receiving temperature data (no requirements, should "just work"
  with Python 3)
- `multi_temperature.lua`: Wireshark dissector for this protocol, registers for UDP port 4567
- `dump.pcap`: Example capture file
- `starter-de.lua`: Starter file, to be used as a base for the workshop - German
- `starter-en.lua`: Starter file, to be used as a base for the workshop - English
