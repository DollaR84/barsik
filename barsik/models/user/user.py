from dataclasses import dataclass
from datetime import datetime

from ..base import Base


@dataclass
class User(Base):
    chat_id: int

    id: int | None = None
    username: str | None = None

    first_name: str | None = None
    last_name: str | None = None

    lang: str | None = None
    time_created: datetime | None = None
