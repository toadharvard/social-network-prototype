from datetime import datetime, timedelta, timezone
from typing import Any

import jose
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from app import dto
from app.config import settings

from .security import SecurityUseCases


class TokenUseCases:
    def __init__(self, security: SecurityUseCases = Depends()):
        self.security = security

    def create(self, subject: str | Any, expires_delta: timedelta | None = None) -> str:
        expires_delta = expires_delta or timedelta(
            minutes=settings.access_token_expire_minutes
        )

        expire = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(
            {"exp": expire, "sub": str(subject)},
            settings.secret_key,
            algorithm=settings.jwt_encode_algorithm,
        )

    def decode(self, token: str) -> dto.token.TokenPayload:
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.jwt_encode_algorithm]
            )
            return dto.token.TokenPayload(**payload)
        except (jose.JWTError, ValidationError):
            raise dto.exceptions.InvalidCredentials
