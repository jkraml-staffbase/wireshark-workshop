-- Define protocol
local p_tempdata = Proto("tempdata", "Temperature Data Demo Protocol");

-- Define protocol fields and their data types
local f_sensorid = ProtoField.uint8("tempdata.sid", "Sensor ID", base.DEC)
local f_temp = ProtoField.float("tempdata.temp", "Temperature in °C", base.DEC)

-- Associate fields with protocol
p_tempdata.fields = { f_sensorid, f_temp }

-- Protocol dissector function for parsing packets
function p_tempdata.dissector(buf, pkt, tree)
    -- simple demo, a proper implementation would do some sanity checks first

    -- set basic packet information for display
    pkt.cols['protocol'] = 'WS01'
    pkt.cols['info'] = 'Temperature measurement'

    -- mark specific byte ranges for display
    local subtree = tree:add(p_tempdata, buf(0,5))
    subtree:add(f_sensorid, buf(0,1))
    subtree:add(f_temp, buf(1,4))
end

-- Register protocol with Wireshark for UDP port 4567
local udp_tbl = DissectorTable.get("udp.port")
udp_tbl:add(4567, p_tempdata)
