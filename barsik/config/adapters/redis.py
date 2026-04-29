from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str
    port: int = 6379
    pool_size: int = 5000

    is_key_builder: bool = True

    @property
    def is_exist(self) -> bool:
        return bool(self.host and self.port)


class RedisConfigAdapter(BaseConfigAdapter[RedisConfig]):
    data: Type[RedisConfig] = RedisConfig
