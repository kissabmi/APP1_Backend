from src.domain.service.auth_service_interface import AuthServiceInterface
from src.domain.model.jwt import JwtResponse


class AuthService(AuthServiceInterface):
    def __init__(self, user_service, jwt_provider):
        self._user_service = user_service
        self._jwt_provider = jwt_provider

    def register(self, login, password):
        user = self._user_service.register(login, password)
        if user is None:
            return None
        return user.user_id

    def authorize(self, login, password):
        """Validate credentials and return JwtResponse."""
        user = self._user_service.find_by_login(login)
        if user is None or not user.check_password(password):
            return None
        access, refresh = self._jwt_provider.generate_tokens(user)
        return JwtResponse(access, refresh)

    def refresh_access_token(self, refresh_token):
        user_id = self._jwt_provider.validate_refresh_token(refresh_token)
        if user_id is None:
            return None
        user = self._user_service.find_by_id(user_id)
        if user is None:
            return None
        access, refresh = self._jwt_provider.generate_tokens(user)
        return JwtResponse(access, refresh)

    def refresh_refresh_token(self, refresh_token):
        user_id = self._jwt_provider.validate_refresh_token(refresh_token)
        if user_id is None:
            return None
        user = self._user_service.find_by_id(user_id)
        if user is None:
            return None
        access, refresh = self._jwt_provider.generate_tokens(user)
        return JwtResponse(access, refresh)
