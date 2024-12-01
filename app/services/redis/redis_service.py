import abc
from typing import Union, Optional

from aioredis import Redis

from app.config import settings
from app.services.hasher import Hasher


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
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
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
        await self._redis.flushall(asynchronous=True)

    async def get(self, key: str) -> Optional[str]:
        key = self._hash_key(key)
        return await self._redis.get(key)

    async def set(self, key: str, val: str) -> None:
        key = self._hash_key(key)
        await self._redis.set(key, val)


class NoCache(CacheSystem):
    async def flush(self) -> None:
        pass

    async def get(self, key: str) -> Optional[str]:
        pass

    async def set(self, key: str, val: str) -> None:
        pass

