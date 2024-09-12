import random
import socket
import sys
from time import sleep

# random words
adjectives = [
    "awesome",
    "benevolent",
    "courageous",
    "diligent",
    "energetic",
    "fearless",
    "gracious",
    "humble",
    "intelligent",
    "joyful",
    "kind",
    "loving",
    "magnificent",
    "noble"
]
nouns = [
    "apple",
    "banana",
    "cherry",
    "date",
    "elderberry",
    "fig",
    "grape",
    "honeydew",
    "imbe",
    "jackfruit",
    "kiwi",
    "lemon",
    "mango",
    "nectarine"
]


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
    while True:
        print(f"Connecting to {target}")
        try:
            tcp_sock = socket.create_connection(target)
        except Exception as e:
            print("Error while connecting")
            print(e)
            sleep(1)
            continue
        send_loop(tcp_sock)
        try:
            tcp_sock.close()
        except Exception as e:
            print("Failed to close socket")
            print(e)
        sleep(1)


def send_loop(tcp_sock: socket.socket):
    # data_gen = one_pdu_per_packet
    # data_gen = two_pdus_per_packet
    # data_gen = single_pdus_out_of_phase
    data_gen = randomly_split_pdus

    for packet in data_gen():
        try:
            tcp_sock.send(packet)
        except Exception as e:
            print("Error while sending")
            print(e)
            return

        sleep(random.random())


def one_pdu_per_packet():
    while True:
        yield generate_pdu()


def two_pdus_per_packet():
    while True:
        yield generate_pdu() + generate_pdu()


def single_pdus_out_of_phase():
    first_pdu = generate_pdu()
    first_half, next_half = split(first_pdu, len(first_pdu) // 2)
    yield first_half
    while True:
        buf = next_half
        next_pdu = generate_pdu()
        first_half, next_half = split(next_pdu, len(next_pdu) // 2)
        buf += first_half
        yield buf


def randomly_split_pdus():
    buf = b''
    while True:
        data = generate_pdu()
        buf = buf + data
        to_send, buf = split(buf, random.randint(1, len(buf)))
        yield to_send


def generate_pdu() -> bytes:
    text = ""
    for c in range(random.randint(1, 4)):
        adjective = adjectives[random.randint(0, len(adjectives) - 1)]
        noun = nouns[random.randint(0, len(nouns) - 1)]
        phrase = f"{adjective} {noun}"
        if len(text) == 0:
            text = phrase
        else:
            text = f"{text},{phrase}"
    return text.encode() + b'\0'


def recv(listen_port: int):
    tcp_sock = socket.create_server(('', listen_port), backlog=1, reuse_port=True)
    while True:
        conn, addr = tcp_sock.accept()
        print(f"Connection from {addr}")
        try:
            recv_loop(conn)
        except Exception as e:
            print("Error while receiving")
            print(e)
            break
    try:
        tcp_sock.close()
    except Exception as e:
        print("Failed to close socket")
        print(e)


def recv_loop(conn: socket.socket):
    while True:
        data = conn.recv(1024)
        if not data:
            # no data received, client has disconnected
            return
        print(".", end="", flush=True)  # just print a dot for each message to show we're receiving, don't interpret


def split(buf: bytes, n: int) -> (bytes, bytes):
    return buf[:n], buf[n:]


main()
