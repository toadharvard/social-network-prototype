import sqlalchemy
from fastapi import APIRouter, Body, Depends, HTTPException

from app import dto
from app.deps import *
from app.usecase import UseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=dto.user.UserResponse,
    dependencies=[Depends(validate_email)],
)
async def create_user(
    payload: dto.user.CreateUserSchema = Body(),
    use_case: UseCase = Depends(),
) -> dto.user.UserResponse:
    payload.password = use_case.security.hash_password(payload.password)
    try:
        user = use_case.user.create(obj_in=payload)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return user


@router.post("/login")
async def get_token(
    payload: dto.user.OAuth2LoginUserForm = Depends(),
    use_case: UseCase = Depends(),
):
    user = use_case.user.authenticate(dto.user.LoginUserScheme.from_orm(payload))
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": use_case.token.create(user.id),
        "token_type": "bearer",
    }


@router.delete("/takeout", response_model=dto.user.UserResponse)
async def delete_user(
    user=Depends(get_current_user),
    use_case: UseCase = Depends(),
):
    return use_case.user.remove(id=user.id)
