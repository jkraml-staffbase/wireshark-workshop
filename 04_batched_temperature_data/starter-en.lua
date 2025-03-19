-- Call existing Dissector:
--   Dissector.get("abbreviation"):call(buf, pkt, tree)
--
-- Convert partial buffer view to normal buffer (eg to pass to a dissector):
--   buf(offset, length):tvb()
--
-- String concatenation:
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

-- Overwrite entry for UDP port 4567
DissectorTable.get("udp.port"):add(4567, p_t2)
