from src.datasource.db import db
from src.datasource.repository.game_repository import GameRepository
from src.datasource.repository.user_repository import UserRepository
from src.domain.service.game_service_impl import GameService
from src.domain.service.user_service_impl import UserService
from src.domain.service.auth_service_impl import AuthService
from src.domain.service.jwt_provider import JwtProvider
from src.web.middleware.authenticator import UserAuthenticator
from src.web.route.auth_controller import create_auth_blueprint
from src.web.route.game_controller import create_game_blueprint


class Container:
    def __init__(self):
        self._game_repository = None
        self._user_repository = None
        self._game_service = None
        self._user_service = None
        self._auth_service = None
        self._jwt_provider = None
        self._authenticator = None

    def get_game_repository(self):
        if self._game_repository is None:
            self._game_repository = GameRepository()
        return self._game_repository

    def get_user_repository(self):
        if self._user_repository is None:
            self._user_repository = UserRepository()
        return self._user_repository

    def get_game_service(self):
        if self._game_service is None:
            self._game_service = GameService(self.get_game_repository())
        return self._game_service

    def get_user_service(self):
        if self._user_service is None:
            self._user_service = UserService(self.get_user_repository())
        return self._user_service

    def get_jwt_provider(self):
        if self._jwt_provider is None:
            self._jwt_provider = JwtProvider()
        return self._jwt_provider

    def get_auth_service(self):
        if self._auth_service is None:
            self._auth_service = AuthService(self.get_user_service(), self.get_jwt_provider())
        return self._auth_service

    def get_authenticator(self):
        if self._authenticator is None:
            self._authenticator = UserAuthenticator(self.get_jwt_provider())
        return self._authenticator

    def get_auth_blueprint(self):
        return create_auth_blueprint(self.get_auth_service(), self.get_authenticator())

    def get_game_blueprint(self):
        return create_game_blueprint(self.get_game_service(), self.get_authenticator())
