from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.postgres.connection import get_session
from app.db.postgres.models import Post, User
from app.db.redis.connection import redis
from app.db.redis.models import PostReactionRedisSet
from app.dto.post import CreatePostSchema, PostReaction, PostResponse, UpdatePostSchema
from app.usecase.crud import CRUDBase


class PostUseCases(CRUDBase[Post, CreatePostSchema, UpdatePostSchema]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Post, session)

    def add_reaction(self, db_obj: Post, user: User, reaction: PostReaction):
        rk = PostReactionRedisSet(post_id=db_obj.id, user_id=user.id, reaction=reaction)
        self.remove_all_reactions(db_obj, user)
        with redis.pipeline(transaction=True) as pipe:
            pipe.sadd(rk.key, rk.value)
            pipe.execute()

    def remove_reaction(self, db_obj: Post, user: User, reaction: PostReaction):
        rk = PostReactionRedisSet(post_id=db_obj.id, user_id=user.id, reaction=reaction)
        redis.srem(rk.key, rk.value)

    def remove_all_reactions(
        self,
        db_obj: Post,
        user: User,
    ):
        rk = PostReactionRedisSet(post_id=db_obj.id, user_id=user.id)
        with redis.pipeline(transaction=True) as pipe:
            for to_delete in PostReaction:
                rk.reaction = to_delete
                pipe.srem(rk.key, rk.value)
            pipe.execute()

    def enrich_with_reactions(self, db_obj: Post) -> PostResponse:
        rk = PostReactionRedisSet(post_id=db_obj.id)
        resp = PostResponse.from_orm(db_obj)
        resp.reactions = {}
        for reaction in PostReaction:
            rk.reaction = reaction
            resp.reactions |= {reaction: redis.scard(rk.key)}

        return resp
