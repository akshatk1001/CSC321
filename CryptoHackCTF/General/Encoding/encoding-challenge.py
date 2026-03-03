from pwn import * # pip install pwntools
import json
import codecs
from Crypto.Util.number import *

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


while True:
    received = json_recv()

    if "flag" in received:
        print(received["flag"])
        break

    typ = received["type"]
    enc = received["encoded"]

    if typ == "base64":
        decoded = base64.b64decode(enc).decode()

    elif typ == "hex":
        decoded = bytes.fromhex(enc).decode()

    elif typ == "rot13":
        decoded = codecs.decode(enc, "rot_13")

    elif typ == "bigint":
        decoded = long_to_bytes(int(enc, 16)).decode()

    elif typ == "utf-8":
        decoded = "".join(chr(c) for c in enc)

    json_send({"decoded": decoded})