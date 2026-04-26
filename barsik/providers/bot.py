from typing import Annotated, Union

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from aiogram_dialog import setup_dialogs

from dishka import from_context, Provider, provide, Scope

from barsik.aiogram.handlers import BaseHandlers
from barsik.config import BaseConfig
from barsik.ui import BaseUI


BotStorageType = Annotated[Union[RedisStorage, MemoryStorage], "bot"]


class BotProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=BaseConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_storage(self, config: BaseConfig) -> BotStorageType:
        storage: BotStorageType
        if config.is_redis and hasattr(config, "redis"):
            db_num = config.telegram.redis_db if hasattr(config, "telegram") else 6
            decode_responses = config.telegram.redis_decode_responses if hasattr(config, "telegram") else False
            redis_url = f"redis://{config.redis.host}:{config.redis.port}/{db_num}"

            storage = RedisStorage.from_url(
                url=redis_url,
                connection_kwargs={
                    "decode_responses": decode_responses,
                },
                key_builder=DefaultKeyBuilder(with_destiny=True) if config.redis.is_key_builder else None,
            )
        else:
            storage = MemoryStorage()

        return storage

    @provide(scope=Scope.APP)
    def get_bot(self, config: BaseConfig) -> Bot:
        if not hasattr(config, "telegram"):
            raise RuntimeError("telegram config not be initialized")

        return Bot(token=config.telegram.token)

    @provide(scope=Scope.APP)
    def get_dp(self, storage: BotStorageType, router: Router, ui: BaseUI) -> Dispatcher:
        dp = Dispatcher(storage=storage)
        dp.include_router(router)

        ui.register(dp=dp, router=router)
        setup_dialogs(dp)
        return dp

    @provide(scope=Scope.APP)
    def get_router(self) -> Router:
        router = Router()
        BaseHandlers.register(router=router)
        return router
