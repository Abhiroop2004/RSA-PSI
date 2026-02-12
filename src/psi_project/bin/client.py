import json
import socket
import struct
from pathlib import Path

from psi_project.common import protocol, algebra

HERE = Path(__file__).resolve().parent.parent.parent
KEYS_DIR = HERE / "keys"

def load_params():
    path = KEYS_DIR / "client_keys.json"
    with open(path, "r") as f:
        return json.load(f)
HOST = '127.0.0.1'
PORT = 5000

params = load_params()
N = params["N"]
e = params["e"]
matchings = {}
stored_client_inputs = []

# Networking Helpers

def send_message(sock, data):
    payload = json.dumps(data).encode()
    length = struct.pack('!I', len(payload))
    sock.sendall(length + payload)


def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Connection closed")
        data += packet
    return data


def receive_message(sock):
    length_bytes = recv_exact(sock, 4)
    length = struct.unpack('!I', length_bytes)[0]
    payload = recv_exact(sock, length)
    return json.loads(payload.decode())

# Crypto Logic

def prepare_values():
    client_inputs = input("Enter your set of strings (comma-separated): ")
    c = [s.strip() for s in client_inputs.split(",")]
    matchings.update({s: None for s in c})
    v = len(c)
    c_bytes = [s.encode() for s in c]
    c_ = [protocol.H(c)%N for c in c_bytes]
    R_c = [algebra.random_group_element(N) for _ in range(v)]
    y = [
        algebra.group_mul(h_i, algebra.pow(r_i, e, N), N)
        for r_i, h_i in zip(R_c, c_)]
    return c, R_c, y

# main client logic

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    try:
        c, R_C, y = prepare_values()
        print("Sending y to server...")
        send_message(client, y)
        response = receive_message(client)
        print("Received response from server.")
        y_ = response["y_"]
        t = response["t"] #server's set tags
        K_c = [algebra.moddiv(y_i, r_c_i, N) for y_i, r_c_i in zip(y_, R_C)]
        t_ = [protocol.H1(str(K_c_i), N) for K_c_i in K_c] #client's computed set tags
        for i in range(len(t_)):
            matchings.update({c[i]: t_[i]})
        output = list(set(t) & set(t_))
        final_results = []  
        for t_val in output:
            for s, t_s in matchings.items():
                if t_s == t_val:
                    final_results.append(s)
        print("Intersection found:", final_results)

    finally:
        client.close()

if __name__ == "__main__":
    print("Client starting...")
    main()