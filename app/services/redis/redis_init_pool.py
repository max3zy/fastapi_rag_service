from abc import ABC
from logging import exception
from typing import AsyncIterator

from aioredis import Redis, from_url

from app.config import settings


# from app.da_log.logger import logger_factory

# logger = logger_factory(__name__)


def create_redis_url(host, port) -> str:
    try:
        return f"redis://{host}:{port}"
    except Exception as e:
        # logger.exception(e)
        raise e


async def init_redis_pool(host: str, port: str) -> AsyncIterator[Redis]:
    session = from_url(
        url=create_redis_url(host=host, port=port),
        encoding="utf-8",
        decode_responses=True,
    )
    # logger.info("redis_session created successfuly")
    yield session
    session.close()
    await session.wait_closed()


class RedisConnection(ABC):
    REDIS_FROM_URL = "redis://{host}:{port}"

    def __init__(self, host: str, port: int, timeout: str):
        self.redis_port = port
        self.redis_host = host
        self.connect_timeout = timeout
        self.redis = None

    async def _create_connection(self) -> Redis:
        self.redis = from_url(
            url=self.create_redis_url(
                host=self.redis_host,
                port=self.redis_port,
            ),
            socket_connect_timeout=self.connect_timeout,
            encoding="utf-8",
            decode_responses=True,
        )
        return self.redis

    async def _close_connection(self):
        if self.redis:
            await self.redis.close()

    def create_redis_url(self, host: str, port: int) -> str:
        return self.REDIS_FROM_URL.format(host=host, port=port)

    async def __aenter__(self) -> Redis:
        return await self._create_connection()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close_connection()

    async def __call__(self, *args, **kwargs) -> Redis:
        return await self._create_connection()


def get_redis_pool() -> RedisConnection:
    return RedisConnection(
        host=settings.CACHE_HOST_REDIS,
        port=settings.CACHE_PORT_REDIS,
        timeout=settings.CACHE_REDIS_TIMEOUT,
    )