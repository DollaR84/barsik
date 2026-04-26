from typing import Annotated, Union

from dishka import from_context, Provider, provide, Scope

from barsik.geo import GeoOSM
from barsik.localisation import Localisation
from barsik.storage import MemoryStorage, RedisStorage
from barsik.config import BaseConfig


BarsikStorageType = Annotated[Union[MemoryStorage, RedisStorage], "barsik"]


class CoreProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=BaseConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_storage(self, config: BaseConfig) -> BarsikStorageType:
        storage: BarsikStorageType
        if config.is_redis and hasattr(config, "redis"):
            storage = RedisStorage(
                host=config.redis.host,
                port=config.redis.port,
                db=config.localisation.redis_db if hasattr(config, "localisation") else 7,
                prefix=config.localisation.redis_prefix if hasattr(config, "localisation") else "lang",
                pool_size=config.redis.pool_size,
            )
        else:
            storage = MemoryStorage()

        return storage

    @provide(scope=Scope.APP)
    def get_localisation(self, config: BaseConfig, storage: BarsikStorageType) -> Localisation:
        if not config.is_localisation or not hasattr(config, "localisation"):
            raise RuntimeError("localisation config not be initialized")

        return Localisation(config, storage)

    @provide(scope=Scope.APP)
    def get_geo(self, config: BaseConfig) -> GeoOSM:
        if not config.is_geo or not hasattr(config, "geo"):
            raise RuntimeError("geo is not initialized")

        return GeoOSM(config)
