class UserServiceInterface:
    def register(self, login, password):
        raise NotImplementedError

    def find_by_login(self, login):
        raise NotImplementedError

    def find_by_id(self, user_id):
        raise NotImplementedError
