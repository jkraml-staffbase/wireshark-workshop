# Temperature Data

Simple UDP protocol emulating a IoT device sending temperature data.

## Format

| 1 byte    | 4 bytes                    |
|-----------|----------------------------|
| unit8     | float32 (big-endian)       |
| Sensor ID | Measured temperature in °C |

## Files

- `temperature_data.py`: Python script for sending and receiving temperature data
- `temperature_client.lua`: Wireshark dissector for this protocol, registers for UDP port 4567
- `dump.pcap`: Example capture file
