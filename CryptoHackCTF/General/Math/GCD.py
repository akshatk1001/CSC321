def gcd(a, b):
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a

print(gcd(12, 8))

a = 66528
b = 52920

print(gcd(a, b))
