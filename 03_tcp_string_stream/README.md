# Zero Terminated Strings

Simple TCP protocol showing variable-size PDUs with an end marker and no up-front length information.

## Format

| n bytes | 1 byte     |
|---------|------------|
| char[]  | 0x00       |
| Text    | end marker |

## Files

- `string_stream.py`: Python script for sending and receiving protocol data (no requirements, should "just work"
  with Python 3)
- `string_stream.lua`: Wireshark dissector for this protocol, registers for TCP port 4445
- `dump-singles.pcap`: Example capture file, one PDU per TCP segment
- `dump-doubles.pcap`: Example capture file, two PDUs per TCP segment
- `dump-out-of-phase.pcap`: Example capture file, two PDUs halves per TCP segment (each PDU continuing in the next
  segment)
- `dump-randomly-segmented.pcap`: Example capture file, randomly segmented PDUs, no clear relation to TCP segments
