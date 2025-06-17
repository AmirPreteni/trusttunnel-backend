from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import nacl.signing
import nacl.encoding

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return "✅ TrustTunnel-backend er live", 200

@app.route("/svar", methods=["POST"])
def motta_svar():
    try:
        data = request.get_json()
        melding = data.get("melding")
        signatur = base64.b64decode(data.get("signatur"))
        offentlig_nokkel = base64.b64decode(data.get("offentligNokkel"))

        verify_key = nacl.signing.VerifyKey(offentlig_nokkel)
        verify_key.verify(melding.encode("utf-8"), signatur)

        print("✅ Signatur er gyldig fra svar!")
        return jsonify({"valid": True, "message": "Svar verifisert ✅"}), 200

    except nacl.exceptions.BadSignatureError:
        return jsonify({"valid": False, "error": "Ugyldig signatur ❌"}), 401

    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)