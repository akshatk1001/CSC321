from Crypto.PublicKey import RSA

with open("General/Data-Formats/privacy_enhanced_mail_1f696c053d76a78c2c531bb013a92d4a.pem", "r") as f:
    key = RSA.import_key(f.read())

print(key.d)
