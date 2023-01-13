from fastapi import Body, Depends, HTTPException, Path
from httpx import AsyncClient

from app.config import settings
from app.dto.exceptions import InvalidCredentials
from app.dto.user import CreateUserSchema
from app.usecase import UseCase


def get_current_user(
    use_case: UseCase = Depends(),
    token: str = Depends(settings.oauth2),
):
    try:
        user = use_case.user.authorize(token)
    except InvalidCredentials as e:
        raise HTTPException(status_code=403, detail=e.detail)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_post(
    post_id=Path(),
    use_case: UseCase = Depends(),
):
    post = use_case.post.get(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def get_user(*, is_post_owner: bool):
    def wrapper(post=Depends(get_current_post), user=Depends(get_current_user)):
        if is_post_owner and user.id == post.owner_id:
            return user
        if not is_post_owner and user.id != post.owner_id:
            return user
        raise HTTPException("You can't perform this action")

    return wrapper


async def validate_email(payload: CreateUserSchema = Body()):
    if not settings.emailhunter_api_key or not settings.emailhunter_api_url:
        return
    async with AsyncClient() as client:
        resp = await client.get(
            settings.emailhunter_api_url,
            params={
                "email": payload.email,
                "api_key": settings.emailhunter_api_key,
            },
        )
        if 200 == resp.status_code and resp.json()["data"]["status"] in (
            "valid",
            "accept_all",
            "webmail",
        ):
            return

    raise HTTPException(
        status_code=400,
        detail="Bad email address or email validation server is dead :(",
    )
