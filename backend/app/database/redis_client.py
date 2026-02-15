import redis
import os

class RedisClient:

    HOST = os.getenv("REDIS_HOST", "redis")
    PORT = int(os.getenv("REDIS_PORT", 6379))

    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = redis.Redis(
                host=cls.HOST,
                port=cls.PORT,
                decode_responses=True
            )
        return cls._client
