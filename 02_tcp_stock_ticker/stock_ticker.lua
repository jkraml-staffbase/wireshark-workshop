local p_ticker = Proto("ticker", "Stock Price Ticker");

local f_len = ProtoField.uint8("ticker.len", "Ticker symbol length", base.DEC)
local f_symbol = ProtoField.string("ticker.symbol", "Ticker symbol", base.UNICODE)
local f_price = ProtoField.float("ticket.price", "Price in $", base.DEC)

p_ticker.fields = { f_len, f_symbol, f_price }

function p_ticker.dissector(buf, pkt, tree)
    -- use built-in helper function for PDU which give their length somewhere at the beginning
    dissect_tcp_pdus(buf, tree, 1, calc_pdu_len, pdu_dissector, true)
    -- buf and tree are passed on to the functions
    -- 1 is the minimum data needed to determine PDU size
    -- calc_pdu_len calculates the expected PDU size
    -- pdu_dissector dissects the PDU once we have all bytes
    -- true is the "desegment" argument, meaning assemble PDUs crossing segment boundaries
end

function calc_pdu_len(buf, pkt, offset)
    -- read symbol length from first byte at offset
    -- we know it'll be available, since dissect_tcp_pdus gets called with 1 as its 3rd argument
    local symbol_len_data = buf(offset,1)
    return 1 + symbol_len_data:uint() + 4
end

function pdu_dissector(buf, pkt, tree)
    pkt.cols['protocol'] = 'WS02'
    pkt.cols['info'] = 'Stock price'
    local symbol_len = buf(0,1):uint()
    local subtree = tree:add(p_ticker, buf(0,1+symbol_len+4))
    local offset = 0
    subtree:add(f_len, buf(offset,1))
    offset = offset + 1
    subtree:add(f_symbol, buf(offset,symbol_len))
    offset = offset + symbol_len
    subtree:add(f_price, buf(offset,4))
    offset = offset + 4
    return offset
end

local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(5678, p_ticker)
