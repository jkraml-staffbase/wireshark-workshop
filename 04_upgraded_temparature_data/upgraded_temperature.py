import socket
import struct
import sys
import random
from time import sleep

def main():
    if len(sys.argv) < 2:
        exit_with_usage()
    cmd = sys.argv[1]
    if cmd == "send":
        if len(sys.argv) < 5:
            exit_with_usage()
        version = sys.argv[2]
        host = sys.argv[3]
        port = int(sys.argv[4])
        if version == "v1":
            send_v1(host, port)
        elif version == "v2":
            send_v2(host, port)
        else:
            exit_with_usage()
    elif cmd == "recv":
        if len(sys.argv) < 3:
            exit_with_usage()
        port = int(sys.argv[2])
        recv(port)
    else:
        exit_with_usage()


def exit_with_usage():
    print(f"Usage: python3 {sys.argv[0]} send <v1|v2> <host> <port>")
    print(f"       python3 {sys.argv[0]} recv <port>")
    sys.exit(1)


def send_v1(target_host: str, target_port: int):
    target = (target_host, target_port)
    id = random.randint(1, 100)
    temperature = float(10 + random.randint(0, 200) / 20)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        delta_t = random.randint(-5, 5) / 10
        temperature += delta_t
        print(f"(v1) Sending temperature data: id={id:03d}, temperature={temperature:.1f}°C")
        data = struct.pack('!Bf', id, temperature)
        udp_sock.sendto(data, target)
        sleep(2)


def send_v2(target_host: str, target_port: int):
    target = (target_host, target_port)
    id = random.randint(1, 100)
    temperature = float(10 + random.randint(0, 200) / 20)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        delta_t = random.randint(-5, 5) / 10
        temperature += delta_t
        print(f"(v2) Sending temperature data: id={id:03d}, temperature={temperature:.1f}°C")
        data = struct.pack('!BBHf', 0xFF, 0x00, id, temperature)
        udp_sock.sendto(data, target)
        sleep(2)


def recv(listen_port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', listen_port))
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {len(data)} bytes from {addr}")
        first_byte = struct.unpack_from('!B', data)[0]
        if first_byte == 0xFF:
            res1, res2, id, temperature = struct.unpack('!BBHf', data)
            print(f"  (v2) Received temperature data: id={id:05d}, temperature={temperature:.1f}")
        else:
            id, temperature = struct.unpack('!Bf', data)
            print(f"  (v1) Received temperature data: id={id:03d}, temperature={temperature:.1f}")


main()
