from cryptography import x509

with open("General/Data-Formats/2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der", "rb") as f:
    cert = x509.load_der_x509_certificate(f.read())

public_key = cert.public_key()
print(public_key.public_numbers().n)
