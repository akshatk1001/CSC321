# !pip install pycryptodome

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from part1 import pad, encrypt_cbc

# Original message
message = b'userid=456;userdata=admin/true;session-id=31337/;'
print(f"Plaintext before byte-flip: {message.decode('ascii')}", "\n")

# Generate key and IV
key = get_random_bytes(16)
iv = get_random_bytes(16)

def submit(user_message):
    # prepend the string userid=456; userdata=
    new_msg = user_message.replace(b';', b'%3B').replace(b'=', b'%3D')
    new_msg = b'userid=456;userdata=' + new_msg + b';session-id=31337'

    new_msg = pad(new_msg)

    print('encrypted input', encrypt_cbc(new_msg, key, iv), "\n")
    return encrypt_cbc(new_msg, key, iv)

def verify(ciphered):
    #pyAesCrypt.decryptFile(ciphered)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphered)

    print('decrypted message: ', decrypted, "\n")
    return b';admin=true;' in decrypted

def attack():
    user = b'A' * 16 + b':admin<false:'
    ct = submit(user)

    prefix = b'userid=456;userdata='
    block_size = 16

    start = len(prefix) + 16
    modified = bytearray(ct)

    def flip(plain_index, from_ch, to_ch):
        block = plain_index // block_size
        offset = plain_index % block_size
        modified[(block - 1) * block_size + offset] ^= (from_ch ^ to_ch)

    flip(start + 0,  ord(':'), ord(';'))
    flip(start + 6,  ord('<'), ord('='))
    flip(start + 11, ord(':'), ord(';'))

    return bytes(modified)

print(verify(attack()))
