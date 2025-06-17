from flask import Flask, request, jsonify
import base64
import nacl.signing
from ai.ai_guardian import gpt_ai  # 👈 AI-analyse-funksjon

app = Flask(__name__)

# 🔏 Verifiser signatur med offentlig nøkkel
def verify_signature(message: str, signature_b64: str, public_key_b64: str) -> bool:
    try:
        message_bytes = message.encode('utf-8')
        signature_bytes = base64.b64decode(signature_b64)
        public_key_bytes = base64.b64decode(public_key_b64)
        verify_key = nacl.signing.VerifyKey(public_key_bytes)
        verify_key.verify(message_bytes, signature_bytes)
        return True
    except Exception as e:
        print("❌ Verifisering feilet:", e)
        return False

# 🌐 API-endepunkt: POST /verify
@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    message = data.get('message')
    signature = data.get('signature')
    public_key = data.get('public_key')

    if not message or not signature or not public_key:
        return jsonify({'valid': False, 'error': 'Mangler data'}), 400

    # ✅ Verifiser signatur
    signature_valid = verify_signature(message, signature, public_key)

    # 🧠 Kjør AI-analyse i tillegg (valgfritt)
    ai_vurdering = gpt_ai(message)

    return jsonify({
        'valid': signature_valid,
        'ai': ai_vurdering
    })

# 🚀 Start Flask-server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)