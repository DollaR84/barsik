from functools import lru_cache
from typing import Type, TypeVar

from pydantic_settings import BaseSettings

from barsik.config import BaseConfig


T = TypeVar("T", bound=BaseConfig)
P = TypeVar("P", bound=BaseSettings)


@lru_cache(maxsize=1)
def get_config(config_cls: Type[T | P]) -> T | P:
    return config_cls()
