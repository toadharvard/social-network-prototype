import uuid
from datetime import datetime

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ConstrainedStr, EmailStr


class Password(ConstrainedStr):
    min_length = 8


class HashedPassword(Password):
    ...


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: HashedPassword


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UpdateUserSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class LoginUserScheme(BaseModel):
    email: EmailStr
    password: Password

    class Config:
        orm_mode = True


class OAuth2LoginUserForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: EmailStr = Form(),
        password: Password = Form(),
        scope: str = Form(default=""),
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None),
    ):
        super().__init__(
            grant_type, username, password, scope, client_id, client_secret
        )
        self.email = username
