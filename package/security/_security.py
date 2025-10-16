import os
import hmac
import hashlib
from flask import request, jsonify

APPLICATION_API_KEY = os.getenv("APPLICATION_API_KEY")
HMAC_SECRET_KEY = os.getenv("HMAC_SECRET_KEY").encode()

def Security(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        signature = request.headers.get('x-signature')

        if api_key != APPLICATION_API_KEY:
            return jsonify({'error': 'Unauthorized: Invalid API key'}), 401

        body = request.get_data()
        expected_sig = hmac.new(HMAC_SECRET_KEY, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            return jsonify({'error': 'Unauthorized: Invalid signature'}), 401

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper