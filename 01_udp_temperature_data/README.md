# Temperature Data

Simple UDP protocol emulating a IoT device sending temperature data.

## Format

| 1 byte    | 4 bytes                    |
|-----------|----------------------------|
| uint8     | float32 (big-endian)       |
| Sensor ID | Measured temperature in °C |

## Files

- `temperature_data.py`: Python script for sending and receiving temperature data (no requirements, should "just work" with Python 3)
- `temperature_data.lua`: Wireshark dissector for this protocol, registers for UDP port 4567
- `dump.pcap`: Example capture file
- `starter-de.lua`: Starter file, to be used as a base for the workshop - German
- `starter-en.lua`: Starter file, to be used as a base for the workshop - English
