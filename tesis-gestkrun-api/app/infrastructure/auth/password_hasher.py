from argon2 import PasswordHasher as Argon2Hasher
from argon2.exceptions import VerifyMismatchError

from app.domain.value_objects import PasswordHash


class PasswordHasherService:
    def __init__(self):
        self._hasher = Argon2Hasher()

    def hash(self, plain_password: str) -> PasswordHash:
        hashed = self._hasher.hash(plain_password)
        return PasswordHash(hashed)

    def verify(self, password_hash: PasswordHash, plain_password: str) -> bool:
        try:
            self._hasher.verify(str(password_hash), plain_password)
            return True
        except VerifyMismatchError:
            return False

    def needs_rehash(self, password_hash: PasswordHash) -> bool:
        return self._hasher.check_needs_rehash(str(password_hash))
