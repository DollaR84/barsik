from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so


class TimeCreatedMixin:

    time_created: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )
