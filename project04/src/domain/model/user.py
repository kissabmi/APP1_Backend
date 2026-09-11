import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, login, password_hash, user_id=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.login = login
        self.password_hash = password_hash

    @staticmethod
    def create(login, password):
        return User(login, generate_password_hash(password))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
