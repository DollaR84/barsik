from dataclasses import dataclass
import os

from .base import BaseConfigAdapter


@dataclass
class RedisData:
    host: str = os.getenv("REDIS_HOST")
    port: int = os.getenv("REDIS_PORT")
    pool_size: int = 5000

    is_key_builder: bool = True


class RedisAdapter(BaseConfigAdapter):
    data: RedisData = RedisData
