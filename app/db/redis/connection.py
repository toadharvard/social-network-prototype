from redis import Redis

from app.config import settings

redis = Redis(host=settings.redis_host, port=settings.redis_port)  # type: ignore
assert redis.ping() == True
