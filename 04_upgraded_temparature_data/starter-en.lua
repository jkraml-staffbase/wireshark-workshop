-- Call existing Dissector:
--   Dissector.get("abbreviation"):call(buf, pkt, tree)

local p_t2 = Proto("temps2", "Temprature v2 Protocol");

local v2_res1_feld = ProtoField.uint8("temps2.res1", "reserved 1", base.HEX)
local v2_res2_feld = ProtoField.uint8("temps2.res2", "reserved 2", base.HEX)

-- Same abbreviation as in Version 1
local v2_sensor_id_feld = ProtoField.uint16("tempdata.id", "Sensor ID", base.HEX)
local v2_temperatur_feld = ProtoField.float("tempdata.value", "Value in °C")

p_t2.fields = { v2_res1_feld, v2_res2_feld, v2_sensor_id_feld, v2_temperatur_feld }

function p_t2.dissector(buf, pkt, tree)

end

-- Overwrite entry for UDP Prort 4567
DissectorTable.get("udp.port"):add(4567, p_t2)
