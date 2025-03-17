-- This part if from the first example
local p_tempdata = Proto("tempdata", "Temperature Data Demo Protocol");
local f_sensorid = ProtoField.uint8("tempdata.sid", "Sensor ID", base.DEC)
local f_temp = ProtoField.float("tempdata.temp", "Temperature in °C", base.DEC)
p_tempdata.fields = { f_sensorid, f_temp }

function p_tempdata.dissector(buf, pkt, tree)
    pkt.cols['protocol'] = 'WS01'
    pkt.cols['info'] = 'Temperature measurement'
    local subtree = tree:add(p_tempdata, buf(0,5))
    subtree:add(f_sensorid, buf(0,1))
    subtree:add(f_temp, buf(1,4))
end

local udp_tbl = DissectorTable.get("udp.port")
udp_tbl:add(4567, p_tempdata) -- this registration will be overwritten later

-- (end of copied code from first part)

-- New combined protocol below

local p_tempdata2 = Proto("temps2", "Temprature 2 proto");
local f_v2_reserved1 = ProtoField.uint8("tempdata.res1", "reserved - old ID", base.HEX)
local f_v2_reserved2 = ProtoField.uint8("tempdata.res2", "reserved - future use", base.HEX)
local f_v2_sensorid = ProtoField.uint16("tempdata.id", "Sensor ID", base.HEX)
local f_v2_temp = ProtoField.float("tempdata.value", "Temperature in °C", base.DEC)
p_tempdata2.fields = { f_v2_reserved1, f_v2_reserved2, f_v2_sensorid, f_v2_temp }

function p_tempdata2.dissector(buf, pkt, tree)
    if buf(0,1):uint() ~= 255 then
      Dissector.get("tempdata"):call(buf, pkt, tree)
    else
      pkt.cols['protocol'] = "WS04"
      pkt.cols['info'] = "Temperature measurement"

      local subtree = tree:add(p_tempdata2, buf(0,8))
      subtree:add(f_v2_reserved1, buf(0,1))
      subtree:add(f_v2_reserved2, buf(1,1))
      subtree:add(f_v2_sensorid, buf(2,2))
      subtree:add(f_v2_temp, buf(4,4))
    end
end

DissectorTable.get("udp.port"):add(4567, p_tempdata2) -- overwrite UDP port 4567 registration
