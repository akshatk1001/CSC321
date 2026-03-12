import json
import socket
from Crypto.Util.number import bytes_to_long

def readline(sock):
    data = b""
    while not data.endswith(b"\n"):
        data += sock.recv(4096)
    return data.decode().strip()


def send(sock, data):
    sock.sendall(json.dumps(data).encode() + b"\n")
    return json.loads(readline(sock))

vote = b"\x00VOTE FOR PEDRO"
vote_num = bytes_to_long(vote)

bits = 8 * len(vote)
mod = 1 << bits
x = 1
size = 1

while size < bits:
    size = min(size * 2, bits)
    new_mod = 1 << size
    top = x * x * x - vote_num
    bottom = pow(3 * x * x, -1, new_mod)
    x = (x - top * bottom) % new_mod

sock = socket.create_connection(("socket.cryptohack.org", 13375))
print(readline(sock))
ans = send(sock, {"option": "vote", "vote": hex(x)[2:]})
print(ans)
