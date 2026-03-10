def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    gcd_value, next_u, next_v = extended_gcd(b, a % b)

    u = next_v
    v = next_u - (a // b) * next_v

    return gcd_value, u, v


p = 26513
q = 32321

gcd_value, u, v = extended_gcd(p, q)

print(gcd_value)
print(u, v)
print(min(u, v))
