from src.datasource.db import db
from src.datasource.model.user import UserModel


class UserRepository:
    def save(self, user_model):
        db.session.add(user_model)
        db.session.commit()

    def find_by_login(self, login):
        return UserModel.query.filter_by(login=login).first()

    def find_by_id(self, user_id):
        return UserModel.query.get(user_id)
