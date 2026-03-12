import pwn
begin = b"label"
xored = pwn.xor(begin, 13)
print(xored.decode())