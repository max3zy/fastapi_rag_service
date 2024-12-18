from typing import AsyncIterator

from aioredis import Redis, from_url


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
    yield session
    session.close()
    await session.wait_closed()
