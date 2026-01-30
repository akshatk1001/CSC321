from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import random


def sha256_key(s):
    return sha256(str(s).encode()).digest()

def sha_256_modified(s):
    digest = sha256(str(s).encode()).digest()
    value = int.from_bytes(digest, "big")
    sh = value >> (256 - 15)
    return sh

def part1_1():
    s = input("Enter the string you would like to encrypt: ")
    res = sha256_key(s)
    print(f"SHA-256 hash of '{s}': {res.hex()}")

def part1_2():
    string1 = "hello"
    string2 = "iello"

    hash1 = sha256_key(string1)
    hash2 = sha256_key(string2)

    print(f"SHA-256 hash of '{string1}': {hash1.hex()}")
    print(f"SHA-256 hash of '{string2}': {hash2.hex()}")
    print()

def part1_3_target_collision(message1):
    hash1 = sha_256_modified(message1)
    
    # print(f"Truncated SHA-256 hash of '{message1}': {hash1}")

    while True:
        message2 = random.getrandbits(64)
        
        if str(message1) == str(message2):
            print("Strings are the same here")
            continue
        
        hash2 = sha_256_modified(message2)

        if hash1 == hash2:
            print(f"Collision found with character {hash2}")
            return
        
        else:
            continue
    