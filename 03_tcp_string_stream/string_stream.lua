local p_tzt = Proto("strings", "Demo: Zero-terminated Strings");

-- define the field as zero-terminated string, we'll mark the ending zero byte as part of this field too
local f_text = ProtoField.stringz("strings.text", "Text", base.UNICODE)
p_tzt.fields = { f_text }


function p_tzt.dissector(buf, pkt, tree)
    local start_idx = nil -- remember if we're in a PDU
    for i=0,buf:len()-1 do
        b = buf(i,1):uint() -- read next byte
        if b == 0 and start_idx ~= nil then -- we're in a PDU and it just ended
            pkt.cols['protocol'] = 'WS03'
            pkt.cols['info'] = 'Text message'
            local length = i-start_idx + 1
            local relevant_bytes = buf(start_idx, length)
            local subtree = tree:add(p_tzt, relevant_bytes)
            subtree:add(f_text, relevant_bytes)
            start_idx = nil
        elseif start_idx == nil then
            start_idx = i
        end
    end
    if start_idx ~= nil then -- TCP segment ended, but we're in the middle of a PDU
        pkt.desegment_len = DESEGMENT_ONE_MORE_SEGMENT
        pkt.desegment_offset = start_idx
    end

    return buf:len()
end


local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(4445, p_tzt)
