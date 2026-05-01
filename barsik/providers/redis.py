from typing import AsyncGenerator

from dishka import from_context, Provider, Scope, provide

from barsik.config import BaseConfig
from barsik.storage import BaseStorage, MemoryStorage, RedisStorage


class RedisProvider(Provider):

    config = from_context(provides=BaseConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_storage(self, config: BaseConfig) -> AsyncGenerator[BaseStorage, None]:
        storage: BaseStorage

        if config.redis and config.redis.host:
            storage = RedisStorage(
                host=config.redis.host,
                port=config.redis.port,
                db=config.redis.db_num,
                pool_size=config.redis.pool_size,
            )
        else:
            storage = MemoryStorage()

        yield storage
        await storage.close()
