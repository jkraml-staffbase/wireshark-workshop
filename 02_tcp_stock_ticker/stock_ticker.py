import random
import socket
import string
import struct
import sys
from time import sleep
from typing import Dict

# some NASDAQ ticker symbols or different lengths
ticker_symbols = [
    "AAPL",
    "NVDA",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "BRK",
    "LLY",
    "TSM",
    "AVGO",
    "TSLA",
    "JPM",
    "WMT",
    "NVO",
    "UNH",
    "XOM",
    "V",
    "MA",
    "PG",
    "JNJ",
    "COST",
    "ORCL",
    "HD",
    "ASML",
    "ABBV",
    "BAC",
    "KO",
    "MRK",
    "NFLX",
    "AZN",
    "CVX",
    "SAP"
]

# keep track of price so they don't jump around too much
current_prices: Dict[string, float] = {t: float(100 + random.randint(1, 1000)) for t in ticker_symbols}


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
            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_sock.connect(target)
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
    data_gen = one_pdu_per_packet
    # data_gen = two_pdus_per_packet
    # data_gen = single_pdus_out_of_phase
    # data_gen = randomly_split_pdus

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


def generate_pdu():
    price_change = 1.0 + (float(random.randint(-5, 5)) / 10.0)
    symbol = ticker_symbols[random.randint(0, len(ticker_symbols) - 1)]
    price = current_prices[symbol]
    price *= price_change
    current_prices[symbol] = price

    print(f"Generated price data: {symbol} @ ${price:.2f}")

    symbol_data = symbol.encode()
    return struct.pack('B', len(symbol_data)) + symbol_data + struct.pack('!f', price)


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
    buf = b''
    while True:
        data = conn.recv(4096)
        if not data:
            # no data received, client has disconnected
            return
        buf += data
        while True:
            if len(buf) < 1:
                # not enough data to read length field
                break
            symbol_len_data = buf[0:1]
            symbol_len = struct.unpack('B', symbol_len_data)[0]
            pdu_len = 1 + symbol_len + 4
            if len(buf) < pdu_len:
                # not enough data to extract PDU
                break
            pdu = buf[:pdu_len]
            remaining_data = buf[pdu_len:]

            symbol_data = pdu[1:1 + symbol_len]
            price_data = pdu[1 + symbol_len:]
            symbol = symbol_data.decode()
            price = struct.unpack('!f', price_data)[0]
            print(f"Received price data: {symbol} @ ${price:.2f}")

            buf = remaining_data


def split(buf: bytes, n: int) -> (bytes, bytes):
    return buf[:n], buf[n:]


main()
