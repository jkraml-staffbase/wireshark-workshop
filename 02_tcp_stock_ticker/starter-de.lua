local p_ticker = Proto("ticker", "Stock Price Ticker");

local f_len = ProtoField.uint8("ticker.len", "Ticker symbol length", base.DEC)
local f_symbol = ProtoField.string("ticker.symbol", "Ticker symbol", base.UNICODE)
local f_price = ProtoField.float("ticket.price", "Price in $", base.DEC)

p_ticker.fields = { f_len, f_symbol, f_price }

-- Eingebaute Hilfsfunktion für PDUs mit Längenangabe am Anfang
--   dissect_tcp_pdus(buf, tree, min_header_size, get_len_func, dissect_func)
--     buf - Datenbuffer, wird an die Funktionen weitergereicht.
--     tree - Datenmodell, wird an die Funktionen weitergereicht.
--     min_header_size - Anzahl Bytes, die nötig sind,
--                       um die Länge der PDU zu bestimmen.
--     get_len_func - Funktion, die aus einem Datenbuffer mit mindestens
--                    min_header_size Bytes die Lönge der PDU berechnet.
--                    Bekommt als Argumente den Datenbuffer, das Paket und
--                    den Offset im Buffer, an dem die PDU Anfängt.
--     dissect_func - Eigentlicher Dissector für die PDU.
--                    Bekommt dieselben Argumente wie die normale Dissectorfunktion:
--                    Datenbuffer, Paket und Datenmodell.

function p_ticker.dissector(buf, pkt, tree)

end

DissectorTable.get("tcp.port"):add(5678, p_ticker)
