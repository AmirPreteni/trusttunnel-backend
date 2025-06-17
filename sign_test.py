import nacl.signing
import base64

# 1. Lag nytt nøkkelpar
signing_key = nacl.signing.SigningKey.generate()
verify_key = signing_key.verify_key

# 2. Meldingen du vil signere
message = b"Hei Amir"

# 3. Signer meldingen
signed = signing_key.sign(message)

# 4. Konverter til base64
signature_b64 = base64.b64encode(signed.signature).decode()
public_key_b64 = base64.b64encode(verify_key.encode()).decode()

# 5. Skriv ut
print("Melding:", message.decode())
print("Signatur:", signature_b64)
print("Offentlig nøkkel:", public_key_b64)