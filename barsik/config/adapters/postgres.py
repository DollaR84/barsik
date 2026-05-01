from dataclasses import dataclass, field
from typing import Optional, Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class PGBouncerConfig:
    host: Optional[str] = None
    port: int = 6432
    use: bool = False


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    username: str
    password: str
    db_name: str
    host: str
    port: int = 5432
    debug: bool = False
    is_async: bool = True

    ssl: bool = False
    url: Optional[str] = None

    bouncer: PGBouncerConfig = field(default_factory=PGBouncerConfig)

    @property
    def prefix(self) -> str:
        return "postgres"

    @property
    def connection_target(self) -> tuple[str, int]:
        if self.bouncer.use and self.bouncer.host:
            return self.bouncer.host, self.bouncer.port
        return self.host, self.port

    @property
    def sync_uri(self) -> str:
        host, port = self.connection_target
        uri = f"postgresql://{self.username}:{self.password}@{host}:{port}/{self.db_name}"
        return self.url if self.url else uri

    @property
    def async_uri(self) -> str:
        host, port = self.connection_target
        uri = f"postgresql+asyncpg://{self.username}:{self.password}@{host}:{port}/{self.db_name}"
        return self.url if self.url else uri


class PostgresConfigAdapter(BaseConfigAdapter[PostgresConfig]):
    data: Type[PostgresConfig] = PostgresConfig
    section_name = "db"
    optional = False
