from ..mixins import TimeCreatedMixin

import sqlalchemy as sa
import sqlalchemy.orm as so


class BaseUser(TimeCreatedMixin):

    chat_id: so.Mapped[int] = so.mapped_column(nullable=False, unique=True)
    username: so.Mapped[str | None] = so.mapped_column(sa.String(256), nullable=True)

    first_name: so.Mapped[str | None] = so.mapped_column(sa.String(256), nullable=True)
    last_name: so.Mapped[str | None] = so.mapped_column(sa.String(256), nullable=True)

    lang: so.Mapped[str | None] = so.mapped_column(sa.String(2), nullable=True)

    GET_FIELDS = ["id", "chat_id"]
    NO_UPDATE_FIELDS = ["id", "chat_id", "time_created"]
