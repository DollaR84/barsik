from functools import lru_cache
from typing import Type, TypeVar


T = TypeVar("T")


@lru_cache(maxsize=1)
def get_config(config_cls: Type[T]) -> T:
    return config_cls()
