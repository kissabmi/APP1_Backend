from functools import wraps

from flask import jsonify, request

from src.datasource.repository.user_repository import UserRepository


class UserAuthenticator:
    def __init__(self, jwt_provider):
        self._jwt_provider = jwt_provider
        self._user_repo = UserRepository()

    def authenticate(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "authorization required"}), 401

            token = auth_header.split(' ', 1)[1]
            user_id = self._jwt_provider.validate_access_token(token)
            if user_id is None:
                return jsonify({"error": "invalid or expired token"}), 401

            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        return decorated
