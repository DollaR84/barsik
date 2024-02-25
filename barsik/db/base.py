from __future__ import annotations

from abc import ABC
import logging
from typing import Type

from barsik.adapters import BaseAdapter
from barsik.config import BaseConfig

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class BaseDBAdapter(BaseAdapter, ABC):
    _adapters: dict[str, Type[BaseDBAdapter]] = {}

    _base = declarative_base()
    _engine = None
    _session_maker = None

    _is_async = None
    _current_adapter = None

    @classmethod
    @property
    def base(cls):
        return cls._base

    @classmethod
    @property
    def engine(cls):
        return cls._engine

    @classmethod
    @property
    def session_maker(cls):
        return cls._session_maker

    @classmethod
    @property
    def current_adapter(cls):
        return cls._current_adapter

    @classmethod
    @property
    def is_async(cls):
        return cls._is_async

    @classmethod
    def init(cls, cfg: BaseConfig, *names: list[str]):
        logger = logging.getLogger()
        for name in names:
            adapter = cls.get_adapter(name)
            if not adapter:
                continue

            try:
                cls._engine = adapter.create_engine(cfg)
                cls._is_async = getattr(cfg, name).is_async
            except Exception as error:
                logger.error(error, exc_info=True)
                raise ValueError("Error: failed to create engine") from error

            if cls.is_async:
                cls._session_maker = async_sessionmaker(
                    binds={cls.base: cls.engine},
                    autoflush=False,
                    expire_on_commit=False,
                )
            else:
                cls._session_maker = sessionmaker(binds={cls.base: cls.engine}, autoflush=False)

            cls._current_adapter = adapter

        return cls.current_adapter

    @classmethod
    def create_session(cls) -> sessionmaker | AsyncSession:
        return cls.session_maker()

    @classmethod
    async def close_session(cls, session):
        try:
            await session.close()
            await cls.engine.dispose()
        except Exception:
            await session.invalidate()

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = self.create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session(self.session)
