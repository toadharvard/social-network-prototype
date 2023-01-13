from datetime import datetime
from enum import Enum
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, conint


class PostReaction(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class PostBaseSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class CreatePostRequest(PostBaseSchema):
    ...


class CreatePostSchema(CreatePostRequest):
    owner_id: UUID


class UpdatePostSchema(PostBaseSchema):
    ...


class PostResponse(PostBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    reactions: dict[PostReaction, int] = {reaction: 0 for reaction in PostReaction}

    class Config:
        use_enum_values = True


class PageRequest(BaseModel):
    skip: conint(ge=0) = Query(default=0)  # type: ignore
    limit: conint(ge=0, le=500) = Query(default=50)  # type: ignore
