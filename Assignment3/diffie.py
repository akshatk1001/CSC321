# Diffie-Hellman Code
from email import message
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(message):
    padding_length = 16 - (len(message) % 16)
    padding = bytes([padding_length] * padding_length)
    return message + padding

def main():
    # Public parameters
    q = int(input("Enter a prime number (q): "))
    g = int(input("Enter a prime base value (g): "))
    
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