from src.domain.service.auth_service_interface import AuthServiceInterface
from src.domain.service.user_service_impl import UserService


class AuthService(AuthServiceInterface):
    def __init__(self, user_service):
        self._user_service = user_service

    def register(self, login, password):
        user = self._user_service.register(login, password)
        if user is None:
            return None
        return user.user_id

    def authorize(self, login, password):
        user = self._user_service.find_by_login(login)
        if user is None:
            return None
        if not user.check_password(password):
            return None
        return user.user_id
