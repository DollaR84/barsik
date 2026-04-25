from functools import lru_cache
from typing import Type, TypeVar

from pydantic_settings import BaseSettings


T = TypeVar("T", bound=BaseSettings)


@lru_cache(maxsize=1)
def get_config(config_cls: Type[T]) -> T:
    return config_cls()
