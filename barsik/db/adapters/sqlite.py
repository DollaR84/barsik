from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from barsik.config.adapters import SqliteConfig
from barsik.db.base import BaseDBAdapter


class SqliteAdapter(BaseDBAdapter[SqliteConfig]):

    def __init__(self, config: SqliteConfig):
        func_create_engine = create_async_engine if config.is_async else create_engine
        sqlalchemy_url = config.async_uri if config.is_async else config.sync_uri

        self.engine = func_create_engine(
            sqlalchemy_url,
            echo=config.debug,
        )
