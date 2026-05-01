import logging
from typing import Generic, Literal, Optional, overload, TypeVar
import uuid

from sqlalchemy.exc import SQLAlchemyError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import Delete, Insert, Select, Update


T = TypeVar("T", int, uuid.UUID)
M = TypeVar("M")


class BaseGateway(Generic[T, M]):

    def __init__(self, session: AsyncSession):
        self.session = session

    @overload
    async def create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> T:
        ...

    @overload
    async def create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[T]:
        ...

    async def create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: bool = False,
    ) -> T | list[T]:
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            return list(result.scalars().all()) if is_multiple else result.scalar_one()

        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    async def delete(self, stmt: Delete, error_message: str) -> None:
        try:
            await self.session.execute(stmt)
            await self.session.commit()

        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    @overload
    async def get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> Optional[M]:
        ...

    @overload
    async def get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[M]:
        ...

    async def get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: bool = False,
    ) -> Optional[M] | list[M]:
        try:
            result = await self.session.execute(stmt)

            return list(result.scalars().all()) if is_multiple else result.scalar_one_or_none()
        except MultipleResultsFound as error:
            logging.error(error, exc_info=True)
            raise ValueError(f"Multiple records found: {error_message}") from error

        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    @overload
    async def update(
            self,
            stmt: Update,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> T:
        ...

    @overload
    async def update(
            self,
            stmt: Update,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[T]:
        ...

    async def update(
            self,
            stmt: Update,
            error_message: str,
            is_multiple: bool = False,
    ) -> T | list[T]:
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            return list(result.scalars().all()) if is_multiple else result.scalar_one()

        except NoResultFound as error:
            logging.error(error, exc_info=True)
            raise NoResultFound(f"no records updated: {error_message}") from error
        except MultipleResultsFound as error:
            logging.error(error, exc_info=True)
            raise MultipleResultsFound(f"multiple records updated: {error_message}") from error
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    async def get_count(self, stmt: Select, error_message: str) -> int:
        try:
            result = await self.session.scalar(stmt)
            return result or 0
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    async def get_exists(self, stmt: Select, error_message: str) -> bool:
        try:
            result = await self.session.execute(stmt)
            return bool(result.scalar_one())
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error


class BaseSyncGateway(Generic[T, M]):

    def __init__(self, session: Session):
        self.session = session

    @overload
    def create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> T:
        ...

    @overload
    def create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[T]:
        ...

    def create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: bool = False,
    ) -> T | list[T]:
        try:
            result = self.session.execute(stmt)
            self.session.commit()
            return list(result.scalars().all()) if is_multiple else result.scalar_one()

        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    def delete(self, stmt: Delete, error_message: str) -> None:
        try:
            self.session.execute(stmt)
            self.session.commit()

        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    @overload
    def get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> Optional[M]:
        ...

    @overload
    def get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[M]:
        ...

    def get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: bool = False,
    ) -> Optional[M] | list[M]:
        try:
            result = self.session.execute(stmt)

            return list(result.scalars().all()) if is_multiple else result.scalar_one_or_none()
        except MultipleResultsFound as error:
            logging.error(error, exc_info=True)
            raise ValueError(f"Multiple records found: {error_message}") from error

        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    @overload
    def update(
            self,
            stmt: Update,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> T:
        ...

    @overload
    def update(
            self,
            stmt: Update,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[T]:
        ...

    def update(
            self,
            stmt: Update,
            error_message: str,
            is_multiple: bool = False,
    ) -> T | list[T]:
        try:
            result = self.session.execute(stmt)
            self.session.commit()
            return list(result.scalars().all()) if is_multiple else result.scalar_one()

        except NoResultFound as error:
            logging.error(error, exc_info=True)
            raise NoResultFound(f"no records updated: {error_message}") from error
        except MultipleResultsFound as error:
            logging.error(error, exc_info=True)
            raise MultipleResultsFound(f"multiple records updated: {error_message}") from error
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    def get_count(self, stmt: Select, error_message: str) -> int:
        try:
            result = self.session.scalar(stmt)
            return result or 0
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    def get_exists(self, stmt: Select, error_message: str) -> bool:
        try:
            result = self.session.execute(stmt)
            return bool(result.scalar_one())
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error
