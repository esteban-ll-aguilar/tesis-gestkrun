from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


class JWTProvider:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    def create_access_token(self, user_id: str, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": user_id, "role": role, "type": "access", "exp": expire}
        return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {"sub": user_id, "type": "refresh", "exp": expire}
        return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except JWTError:
            return {}

    def get_user_id_from_token(self, token: str) -> str | None:
        payload = self.decode_token(token)
        return payload.get("sub")

    def is_access_token(self, token: str) -> bool:
        payload = self.decode_token(token)
        return payload.get("type") == "access"

    def is_refresh_token(self, token: str) -> bool:
        payload = self.decode_token(token)
        return payload.get("type") == "refresh"
