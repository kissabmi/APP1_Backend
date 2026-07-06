from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token


class JwtProvider:
    ACCESS_EXPIRES = timedelta(minutes=30)
    REFRESH_EXPIRES = timedelta(days=7)

    def generate_access_token(self, user):
        return create_access_token(
            identity=str(user.user_id),
            additional_claims={"type": "access"},
            expires_delta=self.ACCESS_EXPIRES
        )

    def generate_refresh_token(self, user):
        return create_refresh_token(
            identity=str(user.user_id),
            additional_claims={"type": "refresh"},
            expires_delta=self.REFRESH_EXPIRES
        )

    def generate_tokens(self, user):
        return self.generate_access_token(user), self.generate_refresh_token(user)

    def validate_access_token(self, token):
        """Returns user_id (str) if valid, None otherwise."""
        return self._validate_token(token, "access")

    def validate_refresh_token(self, token):
        """Returns user_id (str) if valid, None otherwise."""
        return self._validate_token(token, "refresh")

    def _validate_token(self, token, expected_type):
        try:
            decoded = decode_token(token)
        except Exception:
            return None
        if decoded.get("type") != expected_type:
            return None
        return decoded.get("sub")
