import logging
from datetime import timedelta
from typing import Optional

import redis.asyncio as aioredis
from pydantic import BaseModel

from src.config import settings


pool = aioredis.ConnectionPool.from_url(
    str(settings.REDIS_URL), max_connections=10, decode_responses=True
)
redis_client = aioredis.Redis(connection_pool=pool)
logger = logging.getLogger(__name__)


class RedisData(BaseModel):
    key: bytes | str
    value: bytes | str
    ttl: Optional[int | timedelta] = None


async def __set_redis_key(
    redis_data: RedisData, *, is_transaction: bool = False
) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipe:
        await pipe.set(redis_data.key, redis_data.value)
        if redis_data.ttl:
            await pipe.expire(redis_data.key, redis_data.ttl)

        await pipe.execute()


async def set_by_key(key: str, value: str, ttl: int | timedelta | None = None) -> None:
    return await __set_redis_key(RedisData(key=key, value=value, ttl=ttl))


async def get_by_key(key: str) -> str | None:
    return await redis_client.get(key)


async def set_user_language_by_id(id: int, lang: str) -> None:
    await set_by_key(f"user:language:{id}", lang)


async def get_user_language_by_id(id: int) -> str | None:
    return await get_by_key(f"user:language:{id}")


async def delete_by_key(key: str) -> None:
    return await redis_client.delete(key)
