local p_zts = Proto("strings", "Zero-terminated Strings");

-- define the field as zero-terminated string, making the ending zero byte part of this field too
local f_text = ProtoField.stringz("strings.text", "Text", base.UNICODE)
p_zts.fields = { f_text }

-- Lua for loop
--   for i = 0, 100 do
--     …
--   end
--
-- Get buffer length
--   buf:len()
--
-- Request desegmentation
--   pkt.desegment_len = <num bytes> or DESEGMENT_ONE_MORE_SEGMENT
--   pkt.desegment_offset = <offset after last PDU byte>

function p_zts.dissector(buf, pkt, tree)

end

DissectorTable.get("tcp.port"):add(4445, p_zts)
