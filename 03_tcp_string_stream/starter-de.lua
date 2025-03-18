local p_zts = Proto("strings", "Zero-terminated Strings");

-- Wir definieren das Feld als Null-terminierte Strings, dadurch with das Null-Byte Teil des Feldes
local f_text = ProtoField.stringz("strings.text", "Text", base.UNICODE)
p_zts.fields = { f_text }

-- Lua for Loop
--   for i = 0, 100 do
--     …
--   end
--
-- Bufferlänge
--   buf:len()
--
-- Desegmentierung Anfordern (wird am Parameter gesetzt, muss nicht separat zurückgegeben werden)
--   pkt.desegment_len = <Anzahl Bytes> oder DESEGMENT_ONE_MORE_SEGMENT
--   pkt.desegment_offset = <offset nach letztem PDU byte>

function p_zts.dissector(buf, pkt, tree)

end

DissectorTable.get("tcp.port"):add(4445, p_zts)
