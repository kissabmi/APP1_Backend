class JwtRequest:
    def __init__(self, login, password):
        self.login = login
        self.password = password


class JwtResponse:
    def __init__(self, access_token, refresh_token):
        self.type = "Bearer"
        self.access_token = access_token
        self.refresh_token = refresh_token

    def to_dict(self):
        return {
            "type": self.type,
            "accessToken": self.access_token,
            "refreshToken": self.refresh_token
        }


class RefreshJwtRequest:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token
