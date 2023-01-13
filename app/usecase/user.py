from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select

from app import dto
from app.db.postgres.connection import get_session
from app.db.postgres.models import User
from app.usecase.crud import CRUDBase
from app.usecase.security import SecurityUseCases
from app.usecase.token import TokenUseCases


class UserUseCases(
    CRUDBase[User, dto.user.CreateUserSchema, dto.user.UpdateUserSchema]
):
    def __init__(
        self,
        session=Depends(get_session),
        security: SecurityUseCases = Depends(),
        token: TokenUseCases = Depends(),
    ):
        super().__init__(User, session)
        self.security = security
        self.token = token

    def get_by_email(self, email: EmailStr) -> User:
        return self.session.scalar(select(User).where(User.email == email))

    def authenticate(self, payload: dto.user.LoginUserScheme) -> User | None:
        user = self.get_by_email(payload.email)
        if not user:
            return None
        if not self.security.verify_password(payload.password, user.password):
            return None
        return user

    def authorize(self, token: str) -> User | None:
        payload = self.token.decode(token)
        return self.get(id=payload.sub)
