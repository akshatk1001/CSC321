from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import random


def sha256_key(s):
    return sha256(str(s).encode()).digest()

def sha_256_modified(s):
    digest = sha256(str(s).encode()).digest()
    value = int.from_bytes(digest, "big")
    print(value)
    sh = value >> (256 - 30)
    print(sh)

def part1_1():
    s = input("Enter the string you would like to encrypt: ")
    res = sha256_key(s)
    print(f"SHA-256 hash of '{s}': {res.hex()}")

def part2_2():
    string1 = "hello"
    string2 = "iello"

    hash1 = sha256_key(string1)
    hash2 = sha256_key(string2)

    print(f"SHA-256 hash of '{string1}': {hash1.hex()}")
    print(f"SHA-256 hash of '{string2}': {hash2.hex()}")
    print()

# def part3_3():


sha_256_modified("mynameakshat")