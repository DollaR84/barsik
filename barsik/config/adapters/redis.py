from dataclasses import dataclass
import os
from typing import Optional, Type

from .base import BaseConfigAdapter


@dataclass
class RedisData:
    host: Optional[str] = os.getenv("REDIS_HOST")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    pool_size: int = 5000

    is_key_builder: bool = True

    @property
    def is_exist(self) -> bool:
        return bool(self.host and self.port)


class RedisAdapter(BaseConfigAdapter):
    data: Type[RedisData] = RedisData
