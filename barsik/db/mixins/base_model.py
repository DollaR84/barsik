import sqlalchemy.orm as so

from barsik.utils.text import paschal_case_to_snake_case


class BaseDBModel:

    GET_FIELDS: list | None = None
    UPDATE_FIELDS: list | None = None
    NO_UPDATE_FIELDS: list | None = None

    @so.declared_attr
    def __tablename__(self):
        return paschal_case_to_snake_case(self.__name__) + "s"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    def __str__(self):
        return f"{self.__class__.__name__} #{self.id}"

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.id}"

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
