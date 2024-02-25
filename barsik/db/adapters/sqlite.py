from barsik.config import BaseConfig
from barsik.db.adapters.base import BaseDBAdapter

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


class SqliteAdapter(BaseDBAdapter):

    @staticmethod
    def create_engine(cfg: BaseConfig):
        func_create_engine = create_async_engine if cfg.sqlite.is_async else create_engine
        sqlalchemy_url = cfg.sqlite.sqlalchemy_url_async if cfg.sqlite.is_async else cfg.sqlite.sqlalchemy_url

        return func_create_engine(
            sqlalchemy_url,
            echo=cfg.sqlite.debug_sqlalchemy,
        )
