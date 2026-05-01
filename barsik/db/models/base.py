from typing import Any, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

from barsik.utils.text import paschal_case_to_snake_case


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    GET_FIELDS: Optional[list[str]] = None
    UPDATE_FIELDS: Optional[list[str]] = None
    NO_UPDATE_FIELDS: Optional[list[str]] = None

    id: so.Mapped[int] = so.mapped_column(sa.BigInteger, primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return paschal_case_to_snake_case(cls.__name__) + "s"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} #{self.id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} #{self.id}"

    def to_dict(self, exclude_unset: bool = False, exclude: set[str] | None = None) -> dict[str, Any]:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        if exclude_unset:
            data = {key: value for key, value in data.items() if value is not None}

        if exclude:
            data = {key: value for key, value in data.items() if key not in exclude}

        return data
