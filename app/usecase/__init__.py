from fastapi import Depends

from .post import PostUseCases
from .security import SecurityUseCases
from .token import TokenUseCases
from .user import UserUseCases


class UseCase:
    def __init__(
        self,
        security: SecurityUseCases = Depends(),
        token: TokenUseCases = Depends(),
        user: UserUseCases = Depends(),
        post: PostUseCases = Depends(),
    ) -> None:
        self.security: SecurityUseCases = security
        self.token: TokenUseCases = token
        self.user: UserUseCases = user
        self.post: PostUseCases = post


__all__ = ["UseCase"]
