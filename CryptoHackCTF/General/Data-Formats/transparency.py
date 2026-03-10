import hashlib
import subprocess

result = subprocess.run(
    [
        "openssl",
        "pkey",
        "-outform",
        "der",
        "-pubin",
        "-in",
        "General/Data-Formats/transparency_afff0345c6f99bf80eab5895458d8eab.pem",
    ],
    capture_output=True,
)

fingerprint = hashlib.sha256(result.stdout).hexdigest()

print(fingerprint)
