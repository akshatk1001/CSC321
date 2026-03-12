from sympy import factorint


n = 510143758735509025530880200653196460532653147
factors = sorted(factorint(n))

print(factors[0])
