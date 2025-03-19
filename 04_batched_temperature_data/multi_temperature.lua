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

local p_multitemp = Proto("multitemp", "Batched Temperature Protocol");
local f_reserved = ProtoField.uint8("multitemp.res", "reserved", base.HEX)
local f_count = ProtoField.uint8("multitemp.count", "count", base.DEC)
p_multitemp.fields = { f_reserved, f_count }

function p_multitemp.dissector(buf, pkt, tree)
    local simple_dissector = Dissector.get("tempdata")

    if buf(0,1):uint() == 255 then
        local subtree = tree:add(p_multitemp, buf)
        subtree:add(f_reserved, buf(0,1))
        subtree:add(f_count, buf(1,4))

        local count = buf(1,4):uint()
        local measurements_tree = subtree:add("Measurements")
        for i=0,count-1 do
        local offset = 5+i*5
        simple_dissector:call(buf(offset,5):tvb(), pkt, measurements_tree)
        end

        pkt.cols['protocol'] = "BTMP"
        pkt.cols['info'] = count .. " Temperature measurements"
    else
        simple_dissector:call(buf, pkt, tree)
    end
end

DissectorTable.get("udp.port"):add(4567, p_tempdata2) -- overwrite UDP port 4567 registration
