from typing import AsyncGenerator, Generator

from dishka import from_context, Provider, Scope, provide

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from barsik.config import BaseConfig
from barsik.db.base import BaseDBAdapter


class DBProvider(Provider):

    config = from_context(provides=BaseConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_db(self, config: BaseConfig) -> BaseDBAdapter:
        return BaseDBAdapter.init(config)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, db: BaseDBAdapter) -> AsyncGenerator[AsyncSession, None]:
        async with db.get_async_session() as session:
            yield session
            await db.close_async_session(session)

    @provide(scope=Scope.REQUEST)
    def get_sync_session(self, db: BaseDBAdapter) -> Generator[Session, None, None]:
        with db.get_sync_session() as session:
            yield session
            db.close_sync_session(session)
