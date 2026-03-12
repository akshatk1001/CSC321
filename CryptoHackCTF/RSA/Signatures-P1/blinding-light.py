import json
import math
import random
import socket
from Crypto.Util.number import bytes_to_long, long_to_bytes


def readline(sock):
    data = b""
    while not data.endswith(b"\n"):
        data += sock.recv(4096)
    return data.decode().strip()


def send(sock, data):
    sock.sendall(json.dumps(data).encode() + b"\n")
    return json.loads(readline(sock))


sock = socket.create_connection(("socket.cryptohack.org", 13376))
print(readline(sock))

pubkey = send(sock, {"option": "get_pubkey"})
n = int(pubkey["N"], 16)
e = int(pubkey["e"], 16)

admin = b"admin=True"
admin_num = bytes_to_long(admin)

while True:
    r = random.randint(2, n - 1)
    if math.gcd(r, n) != 1:
        continue

    blinded_num = (admin_num * pow(r, e, n)) % n
    blinded_bytes = long_to_bytes(blinded_num)

    if admin not in blinded_bytes:
        break


signed = send(sock, {"option": "sign", "msg": blinded_bytes.hex()})
blinded_sig = int(signed["signature"], 16)

r_inv = pow(r, -1, n)
real_sig = (blinded_sig * r_inv) % n

answer = send(sock, {"option": "verify", "msg": admin.hex(), "signature": hex(real_sig)})
print(answer)
