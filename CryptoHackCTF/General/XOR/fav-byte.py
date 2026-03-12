hex_string = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
ciphertext = bytes.fromhex(hex_string)

for key in range(256):
    plaintext = b""

    for char in ciphertext:
        plaintext += bytes([char ^ key])

    if plaintext.startswith(b"crypto{"):
        print(plaintext.decode())
        break
