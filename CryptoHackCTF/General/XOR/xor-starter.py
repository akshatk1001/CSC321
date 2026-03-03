import pwn
begin = "label"
xored = pwn.xor(begin, 13)
print(str(xored))