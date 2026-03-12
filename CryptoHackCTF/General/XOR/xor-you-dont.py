ciphertext = bytes.fromhex(
    "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
)

known_prefix = b"crypto{"
partial_key = b""

for c, p in zip(ciphertext, known_prefix):
    partial_key += bytes([c ^ p])

# XORing the known prefix reveals b"myXORke", so the full repeated key is b"myXORkey".
key = b"myXORkey"
plaintext = b""

for i, c in enumerate(ciphertext):
    key_byte = key[i % len(key)]
    plaintext += bytes([c ^ key_byte])

print(plaintext.decode())
