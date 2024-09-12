# Wireshark workshop

This repository contains files related to my Wireshark workshop.

The contents are sorted by protocol, each in its own directory.
The naming scheme follows the workshop structure.

## Protocols

- [Temperature Data](01_udp_temperature_data/README.md)  
  UDP protocol with fixed data length.
- [Stock Ticker](02_tcp_stock_ticker/README.md)  
  TCP protocol showing variable-size PDUs with a length header.
- [Zero Terminated Strings](03_tcp_string_stream/README.md)  
  TCP protocol showing variable-size PDUs with an end marker and no up-front length information.

## Using the Dissectors

To use the dissectors, copy or symlink the Lua files to your Wireshark plugins directory (typically
`~/.config/wireshark/plugins/` on Linux).
Then open one of the capture files in Wireshark and see if it works.

The Python scripts to generate traffic are also included.

## A Note on Licensing

Since Wireshark is GPL-licensed, and the dissectors use its Lua bindings, it is the Wireshark authors' opinion that the
dissectors must also be GPL-licensed.
