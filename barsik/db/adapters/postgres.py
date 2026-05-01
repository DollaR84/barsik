import logging
import ssl

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError

from barsik.config.adapters import PostgresConfig
from barsik.db.base import BaseDBAdapter


class PostgresAdapter(BaseDBAdapter[PostgresConfig]):

    def __init__(self, config: PostgresConfig):
        connect_args = {}
        if config.ssl:
            ssl_context = ssl.create_default_context()
            connect_args["ssl"] = ssl_context

        func_create_engine = create_async_engine if config.is_async else create_engine
        sqlalchemy_url = config.async_uri if config.is_async else config.sync_uri

        try:
            self.engine = func_create_engine(
                sqlalchemy_url,
                echo=config.debug,
                pool_size=15,
                max_overflow=15,
                connect_args=connect_args,
            )
        except OperationalError as error:
            logger = logging.getLogger()
            logger.error(error, exc_info=True)
            raise ValueError("Error: failed to create engine") from error
