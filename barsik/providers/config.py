from typing import Type

from dishka import from_context, Provider, provide, Scope

from barsik.config import BaseConfig
from barsik.config.adapters import (
    CoreConfig, CoreConfigAdapter,
    GeoConfig, GeoConfigAdapter,
    LocalisationConfig, LocalisationConfigAdapter,
    RedisConfig, RedisConfigAdapter,
    BaseServicesConfig, ServicesConfigAdapter,
    SqliteConfig, SqliteConfigAdapter,
    TelegramConfig, TelegramConfigAdapter,
)
from barsik.config.adapters.base import BaseConfigAdapter, T


def resolve_config(config: BaseConfig, adapter_cls: Type[BaseConfigAdapter[T]]) -> T:
    section_name = adapter_cls.get_section_name()
    if not section_name:
        raise RuntimeError(f"{adapter_cls.get_name()} must be set section_name")

    data: T = getattr(config, section_name)
    if data is not None:
        return data

    if adapter_cls.optional:
        return adapter_cls.load()

    raise ValueError(f"{adapter_cls.get_name()} must be set in env")


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=BaseConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_core_config(self, config: BaseConfig) -> CoreConfig:
        return resolve_config(config, CoreConfigAdapter)

    @provide(scope=Scope.APP)
    def get_geo_config(self, config: BaseConfig) -> GeoConfig:
        return resolve_config(config, GeoConfigAdapter)

    @provide(scope=Scope.APP)
    def get_localisation_config(self, config: BaseConfig) -> LocalisationConfig:
        return resolve_config(config, LocalisationConfigAdapter)

    @provide(scope=Scope.APP)
    def get_redis_config(self, config: BaseConfig) -> RedisConfig:
        return resolve_config(config, RedisConfigAdapter)

    @provide(scope=Scope.APP)
    def get_services_config(self, config: BaseConfig) -> BaseServicesConfig:
        return resolve_config(config, ServicesConfigAdapter)

    @provide(scope=Scope.APP)
    def get_sqlite_config(self, config: BaseConfig) -> SqliteConfig:
        return resolve_config(config, SqliteConfigAdapter)

    @provide(scope=Scope.APP)
    def get_telegram_config(self, config: BaseConfig) -> TelegramConfig:
        return resolve_config(config, TelegramConfigAdapter)
