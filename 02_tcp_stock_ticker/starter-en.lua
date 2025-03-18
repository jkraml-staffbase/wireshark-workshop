local p_ticker = Proto("ticker", "Stock Price Ticker");

local f_len = ProtoField.uint8("ticker.len", "Ticker symbol length", base.DEC)
local f_symbol = ProtoField.string("ticker.symbol", "Ticker symbol", base.UNICODE)
local f_price = ProtoField.float("ticket.price", "Price in $", base.DEC)

p_ticker.fields = { f_len, f_symbol, f_price }

-- Built-in helper function for PDUs with length information at the beginning
--   dissect_tcp_pdus(buf, tree, min_header_size, get_len_func, dissect_func)
--     buf - Data buffer, passed on to the functions.
--     tree - Data model, passed on to the functions.
--     min_header_size - Number of bytes needed to determine the PDU length.
--     get_len_func - Function that calculates the PDU length from a data buffer with
--                    at least min_header_size bytes.
--                    Arguments: data buffer, packet, and offset in the buffer where
--                    PDU header starts.
--     dissect_func - Actual dissector for the PDU.
--                    Arguments are the same as for the normal dissector function:
--                    data buffer, packet, and data model.

function p_ticker.dissector(buf, pkt, tree)

end

DissectorTable.get("tcp.port"):add(5678, p_ticker)
