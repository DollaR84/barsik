import sqlalchemy as sa
import sqlalchemy.orm as so


class IDMixin:  # pylint: disable=too-few-public-methods

    id: so.Mapped[int] = so.mapped_column(sa.BigInteger, primary_key=True)
