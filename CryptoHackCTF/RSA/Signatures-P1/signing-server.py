import json
import socket
from Crypto.Util.number import long_to_bytes


def readline(sock):
    data = b""
    while not data.endswith(b"\n"):
        data += sock.recv(4096)
    return data.decode().strip()


def send(sock, data):
    sock.sendall(json.dumps(data).encode() + b"\n")
    return json.loads(readline(sock))


sock = socket.create_connection(("socket.cryptohack.org", 13374))
print(readline(sock))

secret_data = send(sock, {"option": "get_secret"})
encrypted_secret = secret_data["secret"]

signed = send(sock, {"option": "sign", "msg": encrypted_secret})
signature = int(signed["signature"], 16)

print(long_to_bytes(signature))
