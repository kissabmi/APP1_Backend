class AuthServiceInterface:
    def register(self, login, password):
        raise NotImplementedError

    def authorize(self, login, password):
        raise NotImplementedError
