ciphertext = bytes.fromhex(
    "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
)

known_prefix = b"crypto{"
partial_key = bytes(c ^ p for c, p in zip(ciphertext, known_prefix))

# XORing the known prefix reveals b"myXORke", so the full repeated key is b"myXORkey".
key = b"myXORkey"
plaintext = bytes(c ^ key[i % len(key)] for i, c in enumerate(ciphertext))

print(plaintext.decode())

