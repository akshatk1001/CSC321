from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import random
import matplotlib.pyplot as plt
import time


def sha256_key(s):
    return sha256(str(s).encode()).digest()

def sha_256_modified(s, numbits = 15):
    digest = sha256(str(s).encode()).digest()
    value = int.from_bytes(digest, "big")
    sh = value >> (256 - numbits)
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

def part1_3_target_collision(message1, bitstoremove):
    hash1 = sha_256_modified(message1, bitstoremove)
    
    # print(f"Truncated SHA-256 hash of '{message1}': {hash1}")

    num_inputs = 0
    while True:
        message2 = random.getrandbits(64)
        num_inputs += 1
        
        if str(message1) == str(message2):
            print("Strings are the same here")
            continue
        
        hash2 = sha_256_modified(message2, bitstoremove)

        if hash1 == hash2:
            # print(f"Collision found with character {hash2}")
            return num_inputs
        
        else:
            continue

    

def create_graphs(message):
    times = []
    num_inputs_list = []
    bit_lengths = [i for i in range(2, 29)]

    for bit in bit_lengths:
        start = time.time()
        num_inputs = part1_3_target_collision(message, bit)
        end = time.time()
        total = end - start
        times.append(total)
        print(f"Time taken for {bit} bits: {total} seconds, {num_inputs} inputs")
        num_inputs_list.append(num_inputs)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(bit_lengths, times)
    plt.xlabel("Digest size (bits)")
    plt.ylabel("Collision time (seconds)")
    plt.title("Digest size vs Collision time")
    
    plt.subplot(1, 2, 2)
    plt.plot(bit_lengths, num_inputs_list, color='orange')
    plt.xlabel("Digest size (bits)")
    plt.ylabel("Number of inputs")
    plt.title("Digest size vs Number of inputs")
    
    plt.tight_layout()
    plt.show()

    return

create_graphs("example")
