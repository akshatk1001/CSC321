1. For task 1, how hard would it be for an adversary to solve the Diffie Hellman 
Problem (DHP) given these parameters? What strategy might the adversary 
take?

Given the parameters it would not be difficult for a bad actor to brute force the Diffie Hellman problem because the small parameters make it so that they can try all possible exponents until finding the one that produces the observed public value. Once the attacker recovers either Alice’s or Bob’s private exponent, they can compute the shared secret.

2. For task 1, would the same strategy used for the tiny parameters work for the 
large values of q and ? Why or why not?

No because when q is a 1024 bit prime the amount of numbers it could be becomes too large making it virtually impossible to compute. (2^1024 different numbers)

3. For task 2, why were these attacks possible? What is necessary to prevent it?

These attacks were possible due to the MITM approach, Mallory was able to intercept both alice and bob's public keys and send malicious values instead; forcing the shared secret to be a known value. to prevent these attacks diffie hellman must be used in conjunction with an authentication mechanism such as digitally signing the initial parameters or validating public values.

4. For task 3 part 1, while it’s very common for many people to use the same 
value for e in their key (common values are 3, 7, 216+1), it is very bad if two 
people use the same RSA modulus n. Briefly describe why this is, and what 
the ramifications are.

If two people have the exact same n, they are essentially using the same primes p and q to create their keys. An attackker can use this because if one persons private key is leaked, they can calculate the others since they have the same modukus. 