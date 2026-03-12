from glob import glob
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from factordb.factordb import FactorDB


for pem_file in sorted(glob("RSA/Primes-P2/keys_and_messages/*")):
    if not pem_file.endswith(".pem"):
        continue

    num = pem_file.split("/")[-1].split(".")[0]

    with open(pem_file, "rb") as f:
        pub = RSA.import_key(f.read())

    n = pub.n
    e = pub.e

    fdb = FactorDB(n)
    fdb.connect()
    factors = fdb.get_factor_list()

    if len(factors) != 2:
        continue

    p = int(factors[0])
    q = int(factors[1])

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    priv = RSA.construct((n, e, d))
    cipher = PKCS1_OAEP.new(priv)

    with open(f"RSA/Primes-P2/keys_and_messages/{num}.ciphertext", "r") as f:
        ct = bytes.fromhex(f.read().strip())
        pt = cipher.decrypt(ct)
        print(f"{num}.ciphertext:", pt)