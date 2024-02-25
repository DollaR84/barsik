from dataclasses import dataclass
import os

from .base import BaseConfigAdapter


@dataclass
class SqliteData:
    sqlalchemy_url: str = ":///".join(["sqlite", os.getenv("SQLITE_PATH")])
    sqlalchemy_url_async: str = ":///".join(["sqlite+aiosqlite", os.getenv("SQLITE_PATH")])

    debug_sqlalchemy: bool = False
    is_async: bool = True


class SqliteAdapter(BaseConfigAdapter):
    data: SqliteData = SqliteData
