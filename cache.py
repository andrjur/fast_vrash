from redis import asyncio as aioredis
from typing import Optional
import json
from config import settings

redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

class CacheManager:
    @staticmethod
    async def get_cache(key: str) -> Optional[str]:
        return await redis.get(key)

    @staticmethod
    async def set_cache(key: str, value: str, expire: int = 3600):
        await redis.set(key, value, ex=expire)

    @staticmethod
    async def delete_cache(key: str):
        await redis.delete(key) 