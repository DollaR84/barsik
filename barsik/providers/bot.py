from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from aiogram_dialog import setup_dialogs

from barsik.aiogram.handlers import BaseHandlers
from barsik.config import BaseConfig
from barsik.ui import BaseUI

from dishka import Provider, Scope, provide


class BotProvider(Provider):

    def __init__(self, config: BaseConfig, ui: BaseUI):
        super().__init__()

        if config.is_redis:
            redis_url = f"redis://{config.redis.host}:{config.redis.port}/{config.telegram.redis_db}"
            self.storage = RedisStorage.from_url(
                url=redis_url,
                connection_kwargs={
                    "decode_responses": config.telegram.redis_decode_responses,
                },
                key_builder=DefaultKeyBuilder(with_destiny=True) if config.redis.is_key_builder else None,
            )
        else:
            self.storage = MemoryStorage()

        self.bot: Bot = Bot(token=config.telegram.token)
        self.dp: Dispatcher = Dispatcher(storage=self.storage)
        self.router: Router = Router()

        BaseHandlers.register(router=self.router)
        self.dp.include_router(self.router)

        ui.register(dp=self.dp, router=self.router)
        setup_dialogs(self.dp)

    @provide(scope=Scope.APP)
    def get_bot(self) -> Bot:
        return self.bot

    @provide(scope=Scope.APP)
    def get_dp(self) -> Dispatcher:
        return self.dp

    @provide(scope=Scope.APP)
    def get_router(self) -> Router:
        return self.router
