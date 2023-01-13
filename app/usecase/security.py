from passlib.context import CryptContext

from app import dto


class SecurityUseCases:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def hash_password(self, password: dto.user.Password) -> dto.user.HashedPassword:
        return self.context.hash(password)
