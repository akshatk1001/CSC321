# Diffie-Hellman Code
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

'''
HEX VALUES FOR TESTING:
q = B10B8F96 A080E01D DE92DE5E AE5D54EC 52C99FBC FB06A3C6 9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C013ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD7098488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708DF1FB2BC 2E4A4371
g = A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28AD662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24855E6EEB 22B3B2E5
'''

def pad(message):
    padding_length = 16 - (len(message) % 16)
    padding = bytes([padding_length] * padding_length)
    return message + padding

def read_hex():
    hex_string = input("Enter the hex value: ")
    new = hex_string.split()
    new = ''.join(new)
    return int(new, 16)

def main():
    # Public parameters
    # q = int(input("Enter a prime number (q): "))
    # g = int(input("Enter a prime base value (g): "))
    q = read_hex()
    g = read_hex()
    
    # Alice's private and public keys
    a_priv = int(input("Enter Alice's private key: "))
    a_pub = (g ** a_priv) % q 
    print(f"Alice's private key XA: {a_priv}")
    print(f"Alice's public key YA: {a_pub}")

    # Bob's private and public keys
    b_priv = int(input("Enter Bob's private key: "))
    b_pub = (g ** b_priv) % q
    print(f"Bob's private key XB: {b_priv}")
    print(f"Bob's public key YB: {b_pub}")

    # Generating the shared secret key
    key_alice = (b_pub ** a_priv) % q
    key_bob = (a_pub ** b_priv) % q
    
    print("\n Shared Secret Keys without Truncation: ")
    print(f"Alice: {key_alice}")
    print(f"Bob: {key_bob}")
    print("Are both keys equal? ", key_alice == key_bob)


    # Creating public iv and cipher based on truncated key
    iv = get_random_bytes(16)

    # Converting Alice to SHA-256 and truncating to 16 bytes
    alice_byte_key = str(key_alice).encode('utf-8')
    alice_hash_digest = (hashlib.sha256(alice_byte_key).digest())[:16]

    alice_cipher = AES.new(alice_hash_digest, AES.MODE_CBC, iv)

    # Getting and cleaning Alice's message
    user_msg = input("\n Enter a message to encrypt: ")
    pad_user_msg = pad(user_msg.encode('utf-8'))
    
    # Encrypting message
    encrypted_alice_msg = alice_cipher.encrypt(pad_user_msg)

    print("--------------------------------")
    print("Alice's Original Message: ", user_msg)
    print(f"Alice's Encrypted Message: {encrypted_alice_msg}")

    '''
    We know that we can just use Alice's iv and cipher to decrypt the message,
    but the purpose of the lab is to show that Bob can decrypt the message using
    the shared secret key he generated.
    '''

    # Creating Bob's truncated key
    bob_byte_key = str(key_bob).encode('utf-8')
    bob_hash_digest = (hashlib.sha256(bob_byte_key).digest())[:16]

    # Creating cipher based on truncated key
    bob_cipher = AES.new(bob_hash_digest, AES.MODE_CBC, iv)

    # Decrypting message
    decrypted_text= bob_cipher.decrypt(encrypted_alice_msg).decode('utf-8')
    print(f"\n Bob's Decrypted Message: {decrypted_text}") 


if __name__ == "__main__":
    main()