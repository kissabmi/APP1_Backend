import uuid
from src.datasource.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, login, password_hash, user_id=None):
        self.id = user_id or str(uuid.uuid4())
        self.login = login
        self.password_hash = password_hash
