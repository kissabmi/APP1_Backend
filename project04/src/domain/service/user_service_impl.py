from src.domain.model.user import User
from src.domain.service.user_service_interface import UserServiceInterface
from src.datasource.repository.user_repository import UserRepository
from src.datasource.model.user import UserModel


class UserService(UserServiceInterface):
    def __init__(self, repository):
        self._repository = repository

    def register(self, login, password):
        existing = self._repository.find_by_login(login)
        if existing:
            return None
        user = User.create(login, password)
        model = UserModel(login=user.login, password_hash=user.password_hash, user_id=user.user_id)
        self._repository.save(model)
        return user

    def find_by_login(self, login):
        model = self._repository.find_by_login(login)
        if model is None:
            return None
        return User(model.login, model.password_hash, model.id)

    def find_by_id(self, user_id):
        model = self._repository.find_by_id(user_id)
        if model is None:
            return None
        return User(model.login, model.password_hash, model.id)
