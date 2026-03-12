import hashlib
import json
import socket
from Crypto.Hash import SHA1
from Crypto.Signature.pkcs1_15 import _EMSA_PKCS1_V1_5_ENCODE
from sympy import discrete_log


p = 20404068993016374194542464172774607695659797117423121913227131032339026169175929902244453757410468728842929862271605567818821685490676661985389839958622802465986881376139404138376153096103140834665563646740160279755212317501356863003638612390661668406235422311783742390510526587257026500302696834793248526734305801634165948702506367176701233298064616663553716975429048751575597150417381063934255689124486029492908966644747931
n = 2 * p
alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def readline(sock):
    data = b""
    while not data.endswith(b"\n"):
        data += sock.recv(4096)
    return data.decode().strip()


def send(sock, data):
    sock.sendall(json.dumps(data).encode() + b"\n")
    return json.loads(readline(sock))


def encode(msg):
    digest = _EMSA_PKCS1_V1_5_ENCODE(SHA1.new(msg.encode()), 96)
    return int.from_bytes(digest, "big")


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def base58(raw):
    num = int.from_bytes(raw, "big")
    out = ""

    while num > 0:
        num, rem = divmod(num, 58)
        out = alphabet[rem] + out

    for i in raw:
        if i == 0:
            out = "1" + out
        else:
            break

    return out


def make_address(i):
    payload = b"\x00" + hashlib.sha1(str(i).encode()).digest()[:20]
    check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58(payload + check)


sock = socket.create_connection(("socket.cryptohack.org", 13394))
print(readline(sock))

data = send(sock, {"option": "get_signature"})
signature = int(data["signature"], 16)

data = send(sock, {"option": "set_pubkey", "pubkey": hex(n)})
suffix = data["suffix"]


i = 0
while True:
    msg0 = f"This is a test {i} for a fake signature." + suffix
    digest0 = encode(msg0)
    if digest0 % 2 == 0:
        break
    i += 1


i = 1
while True:
    name = "A" * i
    msg1 = f"My name is {name} and I own CryptoHack.org" + suffix
    digest1 = encode(msg1)
    if digest1 % 2 == 0:
        break
    i += 1


i = 0
while True:
    address = make_address(i)
    msg2 = "Please send all my money to " + address + suffix
    digest2 = encode(msg2)
    if digest2 % 2 == 0:
        break
    i += 1


e0 = int(discrete_log(p, digest0, signature))
e1 = int(discrete_log(p, digest1, signature))
e2 = int(discrete_log(p, digest2, signature))

share0 = send(sock, {"option": "claim", "msg": msg0, "e": hex(e0), "index": 0})
share1 = send(sock, {"option": "claim", "msg": msg1, "e": hex(e1), "index": 1})
share2 = send(sock, {"option": "claim", "msg": msg2, "e": hex(e2), "index": 2})

s0 = bytes.fromhex(share0["secret"])
s1 = bytes.fromhex(share1["secret"])
s2 = bytes.fromhex(share2["secret"])

flag = xor(xor(s0, s1), s2)
print(flag)
