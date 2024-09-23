from flask import Flask, jsonify, request
import jwt
import time

app = Flask(__name__)

# In-memory store for keys
keys = []

# JWKS endpoint - serves active (non-expired) public keys
@app.route('/.well-known/jwks.json')
def jwks():
    valid_keys = [key for key in keys if key['expiry'] > datetime.utcnow()]
    jwks_response = {
        "keys": [
            {
                "kty": "RSA",
                "kid": key['kid'],
                "use": "sig",
                "alg": "RS256",
                "n": key['public_key'],
            } for key in valid_keys
        ]
    }
    return jsonify(jwks_response)

# Auth endpoint - issues JWT signed with active or expired key
@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired', 'false').lower() == 'true'
    key_to_use = keys[0] if expired else next(
        (key for key in keys if key['expiry'] > datetime.utcnow()), keys[0]
    )

    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": time.time(),
    }
    if expired:
        payload["exp"] = key_to_use['expiry'] - timedelta(hours=1)
    else:
        payload["exp"] = key_to_use['expiry']

    token = jwt.encode(payload, key_to_use['private_key'], algorithm='RS256', headers={"kid": key_to_use['kid']})
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(port=8080)
