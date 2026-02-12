import json
import socket
import struct
from pathlib import Path

# import shared modules from package
from psi_project.common import protocol, algebra

HERE = Path(__file__).resolve().parent.parent.parent  # -> src/psi_project
KEYS_DIR = HERE / "keys"  # project_root/keys (relative to package)

def load_params():
    path = KEYS_DIR / "server_keys.json"
    with open(path, "r") as f:
        return json.load(f)
    
HOST = '127.0.0.1'
PORT = 5000

params = load_params()
N = params["N"]
e = params["e"]
d = params["d"]

# Networking Helpers

def send_message(conn, data):
    payload = json.dumps(data).encode()
    length = struct.pack('!I', len(payload))
    conn.sendall(length + payload)


def recv_exact(conn, n):
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            raise ConnectionError("Connection closed")
        data += packet
    return data


def receive_message(conn):
    length_bytes = recv_exact(conn, 4)
    length = struct.unpack('!I', length_bytes)[0]
    payload = recv_exact(conn, length)
    return json.loads(payload.decode())

# Cryptographic Logic

def prepare_values():
    print("RSA params: ", d, N)

    server_inputs = input("Enter your set of strings (comma-separated): ")
    s = [s_i.strip() for s_i in server_inputs.split(",")]
    s_bytes = [s_i.encode() for s_i in s]
    s_ = [protocol.H(c) for c in s_bytes]
    K_s = [algebra.pow(s_i, d, N) for s_i in s_]
    t = [protocol.H1(str(K_s_i), N) for K_s_i in K_s]
    return t

def process_client_request(y):
    return [algebra.pow(y_i, d, N) for y_i in y]

# main server loop

def main():
    t = prepare_values()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("Server waiting for connection...")
    conn, addr = server.accept()
    print(f"Connected by {addr}")

    try:
        y = receive_message(conn)
        print("Received y from client.")
        y_ = process_client_request(y)

        response = { "y_": y_, "t": t }
        send_message(conn, response)
        print("Response sent to client.")
    finally:
        conn.close()
        server.close()

if __name__ == "__main__":
    print("Server starting...")
    main()