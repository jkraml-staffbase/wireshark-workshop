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


def send(target_host: str, target_port: int):
    target = (target_host, target_port)
    id = random.randint(1, 100)
    temperature = float(10 + random.randint(0, 200) / 20)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        delta_t = random.randint(-5, 5) / 10
        temperature += delta_t
        print(f"Sending temperature data: id={id:03d}, temperature={temperature:.1f}°C")
        data = struct.pack('!Bf', id, temperature)
        udp_sock.sendto(data, target)
        sleep(2)


def recv(listen_port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', listen_port))
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {len(data)} bytes from {addr}")
        id, temperature = struct.unpack('!Bf', data)
        print(f"  Received temperature data: id={id:03d}, temperature={temperature:.1f}")


main()
