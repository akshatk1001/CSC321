from Crypto.Util import number
from math import gcd

# find multiplicative inverse of e mod phi
def mod_inverse(e, phi):
    old_r, r = e, phi # cur, next remainders
    old_s, s = 1, 0 # cur, next coefficients
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    return old_s % phi


def generate_keys(bits):
    e = 65537

    while True:
            p = number.getPrime(bits)
            q = number.getPrime(bits)

            if p == q:
                continue

            n = p * q
            phi = (p - 1) * (q - 1)

            if gcd(e, phi) != 1:
                continue

            d = mod_inverse(e, phi)
            return (e, n), (d, n) 


def encrypt(m, public_key):
    e, n = public_key
    return pow(m, e, n)


def decrypt(c, private_key):
    d, n = private_key
    return pow(c, d, n)
    

def string_to_int(s):
    hex_string = s.encode('ascii').hex()
    return int(hex_string, 16)


# Convert integer to string
def int_to_string(num):
    hex_string = hex(num)[2:]
    if len(hex_string) % 2 == 1:
        hex_string = '0' + hex_string
    return bytes.fromhex(hex_string).decode('ascii')


if __name__ == "__main__":
    public, private = generate_keys(512)
    e, n = public
    d, n2 = private
    
    print(f"Public key: e={e}, n={n}")
    print(f"Private key: d={d}")
    
    text = input("Enter a message: ")
    msg_int = string_to_int(text)
    cipher = encrypt(msg_int, public)
    print(f"Encrypted: {cipher}")

    decrypted = decrypt(cipher, private)
    print(f"Decrypted int: {decrypted}")
    
    decrypted_text = int_to_string(decrypted)
    print(f"Decrypted text: {decrypted_text}")
    print(f"Works: {text == decrypted_text}")
