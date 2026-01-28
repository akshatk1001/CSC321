from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import random
from part3 import generate_keys, encrypt, decrypt, mod_inverse

def sha256_key(s):
    return sha256(str(s).encode()).digest()


def aes_encrypt(msg, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(msg.encode(), AES.block_size))
    return cipher.iv, ct


def aes_decrypt(iv, ct, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()


# Mallory attack
def attack():
    alice_pub, alice_priv = generate_keys(512)
    e, n = alice_pub
    
    s = random.randint(2, n - 1)
    c = encrypt(s, alice_pub)
    
    # Mallory intercepts and modifies
    r = 2
    c_prime = (c * pow(r, e, n)) % n
    
    # Alice decrypts modified ciphertext
    s_prime = decrypt(c_prime, alice_priv)
    
    # Alice encrypts message with mallory key
    k_alice = sha256_key(s_prime)
    msg = "Hi Bob!"
    iv, c0 = aes_encrypt(msg, k_alice)
    
    r_inv = mod_inverse(r, n)
    s_recovered = (s_prime * r_inv) % n
    
    # Mallory decrypts message
    s_prime_recomputed = (s_recovered * r) % n   # equals Alice's s_prime
    k_mallory = sha256_key(s_prime_recomputed)
    decrypted = aes_decrypt(iv, c0, k_mallory)
    
    print(f"Original s: {s}")
    print(f"Recovered s: {s_recovered}")
    print(f"Match: {s == s_recovered}")
    print(f"Decrypted message: {decrypted}")


# Signature forgery
def forge_signature():
    pub, priv = generate_keys(512)
    e, n = pub
    d, n2 = priv
    
    m1 = 42
    m2 = 100

    sig1 = pow(m1, d, n)
    sig2 = pow(m2, d, n)
    
    # Forge signature for m3 = m1 * m2
    m3 = m1 * m2
    sig3 = (sig1 * sig2) % n
    
    # Verify
    verified = pow(sig3, e, n)
    
    print(f"m3 = {m3}")
    print(f"Forged sig verifies: {verified == m3}")


# malleability ex2
def financial_attack():
    pub, priv = generate_keys(512)
    e, n = pub
    
    # Alice encrypts transfer amount
    amount = 100
    c = encrypt(amount, pub)
    
    c_modified = (c * pow(2, e, n)) % n
    
    decrypted_amount = decrypt(c_modified, priv)
    
    print(f"Original amount: ${amount}")
    print(f"Decrypted from modified c: ${decrypted_amount}")
    print(f"Amount multiplied by: {decrypted_amount // amount}")


if __name__ == "__main__":
    attack()
    print()
    forge_signature()
    print()
    financial_attack()