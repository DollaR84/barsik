from dataclasses import dataclass
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


@dataclass(slots=True, init=False)
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
        return bool(self.redis and self.redis.is_exist)

    @property
    def is_localisation(self) -> bool:
        return bool(self.localisation)

    @property
    def is_geo(self) -> bool:
        return bool(self.geo)
