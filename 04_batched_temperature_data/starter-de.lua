-- Existierenden Dissector aufrufen:
--   Dissector.get("Kürzel"):call(buf, pkt, tree)
--
-- Teilbuffer zu eigenständigem Buffer umwandeln (zB um ihn an einen Dissector zu übergeben):
--   buf(offset, length):tvb()
--
-- Stringkonkatenation:
--   "a" .. "b" .. "c"

local p_multitemp = Proto("multitemp", "Batched Temperature Protocol");
local f_reserved = ProtoField.uint8("multitemp.res", "reserved", base.HEX)
local f_count = ProtoField.uint8("multitemp.count", "count", base.DEC)
p_multitemp.fields = { f_reserved, f_count }

function p_multitemp.dissector(buf, pkt, tree)
    if buf(0,1):uint() == 255 then

    else

    end
end

-- Eintrag für UDP Port 4567 überschreiben
DissectorTable.get("udp.port"):add(4567, p_multitemp)
