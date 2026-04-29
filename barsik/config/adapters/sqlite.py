from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class SqliteConfig:
    path: str = "data.db"
    debug_sqlalchemy: bool = False
    is_async: bool = True

    @property
    def uri(self) -> str:
        return f"sqlite:///{self.path}"

    @property
    def async_uri(self) -> str:
        return f"sqlite+aiosqlite:///{self.path}"


class SqliteConfigAdapter(BaseConfigAdapter[SqliteConfig]):
    data: Type[SqliteConfig] = SqliteConfig
    section_name = "db"
    optional = True
