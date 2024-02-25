try:
    from barsik.geo import GeoOSM
except ImportError:
    class GeoOSM:
        pass

from barsik.localisation import Localisation
from barsik.storage import MemoryStorage, RedisStorage
from barsik.config import BaseConfig

from dishka import Provider, Scope, provide


class CoreProvider(Provider):

    def __init__(self, config: BaseConfig):
        super().__init__()

        if config.is_localisation:
            if config.is_redis:
                self.storage = RedisStorage(
                    host=config.redis.host,
                    port=config.redis.port,
                    db=config.localisation.redis_db,
                    prefix=config.localisation.redis_prefix,
                    pool_size=config.redis.pool_size,
                )
            else:
                self.storage = MemoryStorage()

            self.localisation: Localisation = Localisation(config, self.storage)
        else:
            self.localisation = None

        self.geo: GeoOSM = GeoOSM(config) if config.is_geo else None

    @provide(scope=Scope.APP)
    def get_localisation(self) -> Localisation:
        return self.localisation

    @provide(scope=Scope.APP)
    def get_geo(self) -> GeoOSM:
        return self.geo
