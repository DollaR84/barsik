from dataclasses import dataclass
from datetime import datetime

from ..base import BaseModel


@dataclass(slots=True)
class UserModel(BaseModel):
    chat_id: int
    id: int | None = None

    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None

    lang: str | None = None
    created_at: datetime | None = None
