import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship

from app.db.postgres import DeclarativeBase


class BaseAlchemyModel(DeclarativeBase):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=text("now()"),
    )


class User(BaseAlchemyModel):
    __tablename__ = "users"
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="owner")


class Post(BaseAlchemyModel):
    __tablename__ = "posts"
    title = Column(TEXT, nullable=False)
    content = Column(TEXT, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="posts")
