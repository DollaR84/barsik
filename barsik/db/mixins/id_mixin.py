import sqlalchemy as sa
import sqlalchemy.orm as so


class IDMixin:

    id: so.Mapped[int] = so.mapped_column(sa.BigInteger, primary_key=True)
