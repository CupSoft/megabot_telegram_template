import logging
from datetime import timedelta
from typing import Optional

import redis.asyncio as aioredis
from pydantic import BaseModel

from src.config import settings

logger = logging.getLogger(__name__)

pool = aioredis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD.get_secret_value(),
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    decode_responses=True,
)
redis_client = aioredis.Redis(connection_pool=pool)


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
