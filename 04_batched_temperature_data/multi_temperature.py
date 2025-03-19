import random
import socket
import struct
import sys
from time import sleep
from typing import Sequence
from typing import Set


def main():
    if len(sys.argv) < 2:
        exit_with_usage()
    cmd = sys.argv[1]
    if cmd == "send":
        if len(sys.argv) < 4:
            exit_with_usage()
        host = sys.argv[2]
        port = int(sys.argv[3])
        send(host, port)
    elif cmd == "recv":
        if len(sys.argv) < 3:
            exit_with_usage()
        port = int(sys.argv[2])
        recv(port)
    else:
        exit_with_usage()


def exit_with_usage():
    print(f"Usage: python3 {sys.argv[0]} send <host> <port>")
    print(f"       python3 {sys.argv[0]} recv <port>")
    sys.exit(1)


def assemble_v1_payload(id: int, temperature: float) -> bytes:
    return struct.pack('!Bf', id, temperature)


def send(target_host: str, target_port: int):
    target = (target_host, target_port)
    temps_by_ids: dict[int, float] = dict()
    for i in range(10):
        id = random.randint(1, 100)
        temperature = float(10 + random.randint(0, 200) / 20)
        temps_by_ids[i] = temperature

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        ids_to_update = random_selection(temps_by_ids.keys())
        sensor_data = b""
        for id in ids_to_update:
            delta_t = random.randint(-5, 5) / 10
            temps_by_ids[id] += delta_t
            sensor_data += assemble_v1_payload(id, temps_by_ids[id])
        print(f"(v2) Sending temperature data for {len(ids_to_update):d} sensors")
        data = struct.pack('!BI', 0xFF, len(ids_to_update)) + sensor_data
        udp_sock.sendto(data, target)
        sleep(2)


def random_selection(c: Set[int]) -> Sequence[int]:
    subset_size = random.randint(0, len(c))
    return random.sample(list(c), subset_size)


def recv(listen_port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', listen_port))
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {len(data)} bytes from {addr}")
        first_byte = struct.unpack_from('!B', data)[0]
        if first_byte == 0xFF:
            count = struct.unpack_from('!I', data, offset=1)[0]
            print(f"  (v2) Received temperature data for {count:d} sensors")
            for i in range(count):
                offset = 5 + i*5
                (id, temperature) = struct.unpack_from('!Bf', data, offset=offset)
                print(f"        id={id:03d}, temperature={temperature:.1f}")
        else:
            id, temperature = struct.unpack('!Bf', data)
            print(f"  (v1) Received temperature data: id={id:03d}, temperature={temperature:.1f}")


main()
