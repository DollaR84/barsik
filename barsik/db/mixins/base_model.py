from typing import Any, Type

import sqlalchemy.orm as so
from sqlalchemy.sql.schema import Table

from barsik.utils.text import paschal_case_to_snake_case


class BaseDBModel:

    __table__: Table

    GET_FIELDS: list | None = None
    UPDATE_FIELDS: list | None = None
    NO_UPDATE_FIELDS: list | None = None

    @so.declared_attr.directive
    def __tablename__(cls: Type["BaseDBModel"]) -> str:  # pylint: disable=no-self-argument
        return paschal_case_to_snake_case(cls.__name__) + "s"  # pylint: disable=no-member

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} #{self.id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} #{self.id}"

    def dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
