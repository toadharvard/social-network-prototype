from app.dto.post import *


class PostReactionRedisSet(BaseModel):
    post_id: UUID | None = None
    reaction: PostReaction | None = None
    user_id: UUID | None = None

    @property
    def key(self):
        if not self.post_id or not self.reaction:
            raise ValueError("Can't create key: check post_id or reaction value")
        return f"post:{self.post_id}:reaction:{self.reaction.value}"

    @property
    def value(self):
        if not self.user_id:
            raise ValueError("Can't create value: user_id is None")
        return str(self.user_id)
