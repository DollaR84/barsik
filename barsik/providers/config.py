from dishka import from_context, Provider, provide, Scope

from barsik.config import BaseConfig
from barsik.config.adapters import (
    BotConfig, BotConfigAdapter,
    CoreConfig, CoreConfigAdapter,
    GeoConfig, GeoConfigAdapter,
    LLMConfig, LLMConfigAdapter,
    LocalisationConfig, LocalisationConfigAdapter,
    PostgresConfig, PostgresConfigAdapter,
    RedisConfig, RedisConfigAdapter,
    BaseServicesConfig, ServicesConfigAdapter,
    SqliteConfig, SqliteConfigAdapter,
    TelegramConfig, TelegramConfigAdapter,
)
from barsik.utils.resolvers import get_config_section


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=BaseConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_bot_config(self, config: BaseConfig) -> BotConfig:
        return get_config_section(config, BotConfigAdapter)

    @provide(scope=Scope.APP)
    def get_core_config(self, config: BaseConfig) -> CoreConfig:
        return get_config_section(config, CoreConfigAdapter)

    @provide(scope=Scope.APP)
    def get_geo_config(self, config: BaseConfig) -> GeoConfig:
        return get_config_section(config, GeoConfigAdapter)

    @provide(scope=Scope.APP)
    def get_llm_config(self, config: BaseConfig) -> LLMConfig:
        return get_config_section(config, LLMConfigAdapter)

    @provide(scope=Scope.APP)
    def get_localisation_config(self, config: BaseConfig) -> LocalisationConfig:
        return get_config_section(config, LocalisationConfigAdapter)

    @provide(scope=Scope.APP)
    def get_postgres_config(self, config: BaseConfig) -> PostgresConfig:
        return get_config_section(config, PostgresConfigAdapter)

    @provide(scope=Scope.APP)
    def get_redis_config(self, config: BaseConfig) -> RedisConfig:
        return get_config_section(config, RedisConfigAdapter)

    @provide(scope=Scope.APP)
    def get_services_config(self, config: BaseConfig) -> BaseServicesConfig:
        return get_config_section(config, ServicesConfigAdapter)

    @provide(scope=Scope.APP)
    def get_sqlite_config(self, config: BaseConfig) -> SqliteConfig:
        return get_config_section(config, SqliteConfigAdapter)

    @provide(scope=Scope.APP)
    def get_telegram_config(self, config: BaseConfig) -> TelegramConfig:
        return get_config_section(config, TelegramConfigAdapter)
