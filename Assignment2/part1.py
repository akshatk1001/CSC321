from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

with open('Assignment2/cp-logo.bmp', 'rb') as f:
    data = f.read()

# header = first 54 bytes
header = data[:54]
rest = data[54:]

def pad(message):
  padding_length = 16 - (len(message) % 16)
  padding = bytes([padding_length] * padding_length)
  return message + padding

def encrypt_ecb(data, key):
  cipher = AES.new(key, AES.MODE_ECB)
  text = b''
  for i in range(0, len(data), 16):
    block = data[i:i+16]
    text += cipher.encrypt(block)
  return text

def encrypt_cbc(data, key, iv):
  cipher = AES.new(key, AES.MODE_ECB)
  text = b''
  previous = iv
  for i in range(0, len(data), 16):
    block = data[i:i+16]
    xored = b''
    for j in range(16):
      xored += bytes([block[j] ^ previous[j]])
      
    encrypted = cipher.encrypt(xored)
    text += encrypted
    previous = encrypted
    
  return text

padded_rest = pad(rest)
key = get_random_bytes(16)
iv = get_random_bytes(16)

ecb_encrypted = encrypt_ecb(padded_rest, key)
cbc_encrypted = encrypt_cbc(padded_rest, key, iv)

with open('Assignment2/ecb_encrypted.bmp', 'wb') as f:
  f.write(header + ecb_encrypted)
    
with open('Assignment2/cbc_encrypted.bmp', 'wb') as f:
  f.write(header + cbc_encrypted)
  
  
    