from typing import Any

from .adapters.base import BaseConfigAdapter


class BaseConfig:

    def __init__(self, *names: str, **kwargs: Any):
        BaseConfigAdapter(self, *names, **kwargs)

    @property
    def is_redis(self) -> bool:
        return hasattr(self, "redis") and getattr(self, "redis").is_exist

    @property
    def is_localisation(self) -> bool:
        return hasattr(self, "localisation")

    @property
    def is_geo(self) -> bool:
        return hasattr(self, "geo")
