from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import base64

def verify_signature(message: str, signature_b64: str, public_key_b64: str) -> bool:
    try:
        public_key_bytes = base64.b64decode(public_key_b64)
        signature_bytes = base64.b64decode(signature_b64)
        verify_key = VerifyKey(public_key_bytes)
        verify_key.verify(message.encode(), signature_bytes)
        return True
    except BadSignatureError:
        return False
    except Exception as e:
        print("Feil under verifisering:", e)
        return False