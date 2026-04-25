from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from types import TracebackType
from typing import Any, Callable, cast, Optional, Self, Type, Union

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from barsik.adapters import BaseAdapter
from barsik.config import BaseConfig


EngineType = Union[Engine, AsyncEngine]
SessionMakerType = Union["sessionmaker[Session]", "async_sessionmaker[AsyncSession]"]
SessionType = Union[Session, AsyncSession]


class BaseDBAdapter(BaseAdapter["BaseDBAdapter"], ABC):
    _adapters: dict[str, Type[BaseDBAdapter]] = {}

    base = declarative_base()

    _engine: Optional[EngineType] = None
    _session_maker: Optional[SessionMakerType] = None

    _is_async: Optional[bool] = None
    _current_adapter: Optional[Type[BaseDBAdapter]] = None

    @classmethod
    def init(cls, cfg: BaseConfig, *names: str) -> Optional[Type[BaseDBAdapter]]:
        logger = logging.getLogger()

        for name in names:
            adapter = cls.get_adapter(name)
            if not adapter:
                continue

            try:
                cls._engine = adapter.create_engine(cfg)
                config_node = getattr(cfg, name, None)
                cls._is_async = getattr(config_node, "is_async", False) if config_node else False
            except Exception as error:
                logger.error(error, exc_info=True)
                raise ValueError("Error: failed to create engine") from error

            if cls._is_async:
                cls._session_maker = async_sessionmaker(
                    binds={cls.base: cls._engine},
                    autoflush=False,
                    expire_on_commit=False,
                )
            else:
                cls._session_maker = sessionmaker(binds={cls.base: cls._engine}, autoflush=False)

            cls._current_adapter = adapter

        return cls._current_adapter

    @classmethod
    def create_session(cls) -> Any:
        if cls._session_maker is None:
            raise RuntimeError("Session maker is not initialized")

        maker: Callable[[], SessionType] = cast(Callable[[], SessionType], cls._session_maker)
        return maker()  # pylint: disable=not-callable

    @classmethod
    async def close_session(cls, session: SessionType) -> None:
        try:
            if isinstance(session, AsyncSession):
                await session.close()
            elif isinstance(session, Session):
                session.close()

            if cls._engine:
                if isinstance(cls._engine, AsyncEngine):
                    await cls._engine.dispose()
                elif isinstance(cls._engine, Engine):
                    cls._engine.dispose()

        except SQLAlchemyError as e:
            if isinstance(session, Session):
                session.invalidate()
            logging.error("Error closing session: %s", str(e))

    def __init__(self) -> None:
        self.session: Optional[Union[Session, AsyncSession]] = None

    async def __aenter__(self) -> Self:
        self.session = self.create_session()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        if self.session:
            await self.close_session(self.session)

    @staticmethod
    @abstractmethod
    def create_engine(cfg: BaseConfig) -> EngineType:
        raise NotImplementedError
