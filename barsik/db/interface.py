from barsik.config import BaseConfig
from barsik.models import User

from .base import BaseDBAdapter


class BaseDB:

    def __init__(self, cfg: BaseConfig, *names: list[str]):
        self.adapter = BaseDBAdapter.init(cfg, *names)
        self.mapper = None

    async def get_user(self, user: User):
        return await self.mapper.get(user)

    async def get_or_create_user(self, user: User):
        return await self.mapper.get_or_create(user)

    async def update_user(
            self, user: User,
            first_name: str | None = None,
            last_name: str | None = None,
            username: str | None = None,
            lang: str | None = None,
    ):
        return await self.mapper.update(user, first_name=first_name, last_name=last_name, username=username, lang=lang)

    async def get_and_update_user(self, user: User):
        await self.get_or_create_user(user)
        await self.update_user(
            user,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            lang=user.lang,
        )
        return await self.get_user(user)
