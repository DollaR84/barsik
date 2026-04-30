from typing import Optional

from barsik.config.adapters import (
    CoreConfig,
    GeoConfig,
    LocalisationConfig,
    RedisConfig,
    BaseServicesConfig,
    SqliteConfig,
    TelegramConfig,
)
from .adapters.base import BaseConfigAdapter


class BaseConfig:
    core: CoreConfig
    geo: Optional[GeoConfig] = None
    localisation: Optional[LocalisationConfig] = None
    redis: Optional[RedisConfig] = None
    services: Optional[BaseServicesConfig] = None
    db: Optional[SqliteConfig] = None
    bot: Optional[TelegramConfig] = None

    def __init__(self) -> None:
        BaseConfigAdapter(self)

    @property
    def is_redis(self) -> bool:
        return self.redis is not None and self.redis.is_exist

    @property
    def is_localisation(self) -> bool:
        return self.localisation is not None

    @property
    def is_geo(self) -> bool:
        return self.geo is not None
