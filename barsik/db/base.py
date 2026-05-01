from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import asynccontextmanager, contextmanager
import logging
from typing import AsyncIterator, Iterator, cast, Generic, Type, TypeVar, Union

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from barsik.adapters import BaseAdapter
from barsik.config import BaseConfig


SessionType = Union[Session, AsyncSession]
ConfigT = TypeVar("ConfigT")


class BaseDBAdapter(BaseAdapter["BaseDBAdapter"], ABC, Generic[ConfigT]):
    _adapters: dict[str, Type[BaseDBAdapter]] = {}
    _async_session_factory: async_sessionmaker[AsyncSession]
    _sync_session_factory: sessionmaker[Session]
    engine: Engine | AsyncEngine
    _current_adapter: BaseDBAdapter

    @classmethod
    def init(cls, config: BaseConfig) -> BaseDBAdapter:
        if config.db is None:
            raise RuntimeError("db settings must be initialized")

        adapter_cls = cls.get_adapter(config.db.prefix)
        if not adapter_cls:
            raise RuntimeError(f"adapter {config.db.prefix} not found")

        cls._current_adapter = adapter_cls(config.db)

        if config.db.is_async:
            cls._async_session_factory = async_sessionmaker(
                bind=cast(AsyncEngine, cls._current_adapter.engine),
                class_=AsyncSession,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        else:
            cls._sync_session_factory = sessionmaker(
                bind=cast(Engine, cls._current_adapter.engine),
                class_=Session,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )

        return cls._current_adapter

    @abstractmethod
    def __init__(self, _: ConfigT):
        raise NotImplementedError

    @asynccontextmanager
    async def get_async_session(self) -> AsyncIterator[AsyncSession]:  # pylint: disable=invalid-overridden-method
        async with self._async_session_factory() as session:
            try:
                yield session

            except SQLAlchemyError as error:
                await session.rollback()
                raise OperationalError(statement=str(error), params=None, orig=error) from error

            finally:
                await session.aclose()

    @contextmanager
    def get_sync_session(self) -> Iterator[Session]:  # pylint: disable=invalid-overridden-method
        with self._sync_session_factory() as session:
            try:
                yield session

            except SQLAlchemyError as error:
                session.rollback()
                raise OperationalError(statement=str(error), params=None, orig=error) from error

            finally:
                session.close()

    async def close_async_session(self, session: AsyncSession, force: bool = False) -> None:
        try:
            await session.close()

            if force and isinstance(self._current_adapter.engine, AsyncEngine):
                await self._current_adapter.engine.dispose()

        except SQLAlchemyError as e:
            logging.error("Error closing session: %s", str(e))

    def close_sync_session(self, session: Session, force: bool = False) -> None:
        try:
            session.close()

            if force and isinstance(self._current_adapter.engine, Engine):
                self._current_adapter.engine.dispose()

        except SQLAlchemyError as e:
            session.invalidate()
            logging.error("Error closing session: %s", str(e))
