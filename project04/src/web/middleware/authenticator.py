import base64
from functools import wraps
from flask import request, jsonify


class UserAuthenticator:
    def __init__(self, auth_service):
        self._auth_service = auth_service

    def authenticate(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Basic '):
                return jsonify({"error": "authorization required"}), 401

            try:
                encoded = auth_header.split(' ', 1)[1]
                decoded = base64.b64decode(encoded).decode('utf-8')
                login, password = decoded.split(':', 1)
            except Exception:
                return jsonify({"error": "invalid authorization format"}), 401

            user_id = self._auth_service.authorize(login, password)
            if user_id is None:
                return jsonify({"error": "invalid credentials"}), 401

            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        return decorated
