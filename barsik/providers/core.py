from typing import Optional

from dishka import Provider, Scope, provide

from barsik.geo import GeoOSM
from barsik.localisation import Localisation
from barsik.storage import MemoryStorage, RedisStorage
from barsik.config import BaseConfig


class CoreProvider(Provider):

    def __init__(self, config: BaseConfig):
        super().__init__()

        self.localisation: Optional[Localisation]
        self.geo: Optional[GeoOSM]

        if config.is_localisation and hasattr(config, "localisation"):
            self.storage: RedisStorage | MemoryStorage

            if config.is_redis and hasattr(config, "redis"):
                self.storage = RedisStorage(
                    host=config.redis.host,
                    port=config.redis.port,
                    db=config.localisation.redis_db,
                    prefix=config.localisation.redis_prefix,
                    pool_size=config.redis.pool_size,
                )
            else:
                self.storage = MemoryStorage()

            self.localisation = Localisation(config, self.storage)
        else:
            self.localisation = None

        self.geo = GeoOSM(config) if config.is_geo else None

    @provide(scope=Scope.APP)
    def get_localisation(self) -> Localisation:
        if not self.localisation:
            raise RuntimeError("localisation is not initialized")
        return self.localisation

    @provide(scope=Scope.APP)
    def get_geo(self) -> GeoOSM:
        if not self.geo:
            raise RuntimeError("geo is not initialized")
        return self.geo
