import abc
from typing import Optional, Union

from aioredis import Redis

from app.config import settings
from app.services.hasher import Hasher
from app.services.redis.redis_init_pool import RedisConnection, get_redis_pool


class CacheSystem(abc.ABC):
    @abc.abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abc.abstractmethod
    async def set(self, key: str, val: str) -> None:
        pass

    @abc.abstractmethod
    async def flush(self):
        pass


class CacheRedis(CacheSystem):
    def __init__(self) -> None:
        self._redis: RedisConnection = get_redis_pool()
        self._hasher = Hasher(hasher=settings.REDIS_HASHER).hash_data
        self._min_key_length_to_hash = settings.SIZE_CHARS

    def _hash_key(self, data: Union[str, bytes]) -> str:
        if (
            self._min_key_length_to_hash
            and isinstance(data, (str, bytes))
            and len(data) > self._min_key_length_to_hash
        ):
            try:
                return self._hasher(data)
            except TypeError:
                pass
        return data

    async def flush(self) -> None:
        try:
            async with self._redis as session:
                await session.flushall(asynchronous=True)
        except Exception as e:
            raise e

    async def get(self, key: str) -> Optional[str]:
        key = self._hash_key(key)
        try:
            async with self._redis as session:
                return await session.get(key)
        except Exception as e:
            # logger.error(str(e))
            return None

    async def set(self, key: str, val: str) -> None:
        key = self._hash_key(key)
        try:
            async with self._redis as session:
                await session.set(key, val)
        except Exception as e:
            # logger.error(str(e))
            pass

class NoCache(CacheSystem):
    async def flush(self) -> None:
        pass

    async def get(self, key: str) -> Optional[str]:
        pass

    async def set(self, key: str, val: str) -> None:
        pass
