from flask import Blueprint, jsonify, request
from src.domain.model.jwt import JwtRequest


def create_auth_blueprint(auth_service, authenticator):
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
        data = request.get_json()
        if data is None or 'login' not in data or 'password' not in data:
            return jsonify({"error": "login and password required"}), 400

        jwt_request = JwtRequest(data['login'], data['password'])
        jwt_response = auth_service.authorize(jwt_request.login, jwt_request.password)
        if jwt_response is None:
            return jsonify({"error": "invalid credentials"}), 401

        return jsonify(jwt_response.to_dict()), 200

    @auth_bp.route('/refresh', methods=['POST'])
    def refresh():
        data = request.get_json()
        if data is None or 'refreshToken' not in data:
            return jsonify({"error": "refreshToken required"}), 400

        jwt_response = auth_service.refresh_access_token(data['refreshToken'])
        if jwt_response is None:
            return jsonify({"error": "invalid or expired refresh token"}), 401

        return jsonify(jwt_response.to_dict()), 200

    @auth_bp.route('/refresh-full', methods=['POST'])
    def refresh_full():
        data = request.get_json()
        if data is None or 'refreshToken' not in data:
            return jsonify({"error": "refreshToken required"}), 400

        jwt_response = auth_service.refresh_refresh_token(data['refreshToken'])
        if jwt_response is None:
            return jsonify({"error": "invalid or expired refresh token"}), 401

        return jsonify(jwt_response.to_dict()), 200

    @auth_bp.route('/me', methods=['GET'])
    @authenticator.authenticate
    def me(user_id):
        from src.datasource.repository.user_repository import UserRepository
        user = UserRepository().find_by_id(user_id)
        if user is None:
            return jsonify({"error": "user not found"}), 404
        return jsonify({"user_id": user.id, "login": user.login}), 200

    return auth_bp
