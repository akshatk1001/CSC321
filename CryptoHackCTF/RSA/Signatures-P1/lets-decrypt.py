import json
import socket
from Crypto.Hash import SHA1
from Crypto.Signature.pkcs1_15 import _EMSA_PKCS1_V1_5_ENCODE


def readline(sock):
    data = b""
    while not data.endswith(b"\n"):
        data += sock.recv(4096)
    return data.decode().strip()


def send(sock, data):
    sock.sendall(json.dumps(data).encode() + b"\n")
    return json.loads(readline(sock))


sock = socket.create_connection(("socket.cryptohack.org", 13391))
print(readline(sock))

data = send(sock, {"option": "get_signature"})
signature = int(data["signature"], 16)

msg = "I am Mallory, I own CryptoHack.org"
digest = _EMSA_PKCS1_V1_5_ENCODE(SHA1.new(msg.encode()), 256)
digest_num = int.from_bytes(digest, "big")

n = signature - digest_num
e = 1

response = send(sock, {"option": "verify", "msg": msg, "N": hex(n), "e": hex(e)})
print(response)
