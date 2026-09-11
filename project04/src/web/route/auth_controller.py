import base64
from flask import Blueprint, jsonify, request


def create_auth_blueprint(auth_service):
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        if data is None or 'login' not in data or 'password' not in data:
            return jsonify({"error": "login and password required"}), 400

        user_id = auth_service.register(data['login'], data['password'])
        if user_id is None:
            return jsonify({"error": "login already exists"}), 400

        return jsonify({"ok": True, "user_id": user_id}), 201

    @auth_bp.route('/login', methods=['POST'])
    def login():
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return jsonify({"error": "authorization required"}), 401

        try:
            encoded = auth_header.split(' ', 1)[1]
            decoded = base64.b64decode(encoded).decode('utf-8')
            login, password = decoded.split(':', 1)
        except Exception:
            return jsonify({"error": "invalid authorization format"}), 401

        user_id = auth_service.authorize(login, password)
        if user_id is None:
            return jsonify({"error": "invalid credentials"}), 401

        return jsonify({"ok": True, "user_id": user_id}), 200

    return auth_bp
