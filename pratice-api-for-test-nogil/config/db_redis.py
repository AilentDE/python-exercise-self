import redis
import os

# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, password=os.getenv("REDIS_PASSWORD"))
pool = redis.asyncio.ConnectionPool.from_url(os.getenv("REDIS_URL"))


def get_redis() -> redis.asyncio.Redis:
    return redis.asyncio.Redis(connection_pool=pool)
