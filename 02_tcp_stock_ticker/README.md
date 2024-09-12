# Stock Ticker

Simple TCP protocol showing variable-size PDUs with a length header.

## Format

| 1 byte        | 1-4 bytes     | 4 bytes              |
|---------------|---------------|----------------------|
| unit8         | char[]        | float32 (big-endian) |
| Symbol length | Ticker symbol | Current price in USD |

## Files

- `temperature_data.py`: Python script for sending and receiving protocol data (no requirements, should "just work"
  with Python 3)
- `temperature_client.lua`: Wireshark dissector for this protocol, registers for TCP port 5678
- `dump-singles.pcap`: Example capture file, one PDU per TCP segment
- `dump-doubles.pcap`: Example capture file, two PDUs per TCP segment
- `dump-out-of-phase.pcap`: Example capture file, two PDUs halves per TCP segment (each PDU continuing in the next
  segment)
- `dump-randomly-segmented.pcap`: Example capture file, randomly segmented PDUs, no clear relation to TCP segments

