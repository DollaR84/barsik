from .adapters.base import BaseConfigAdapter


class BaseConfig:

    def __init__(self, *names: list[str], **kwargs):
        BaseConfigAdapter(self, *names, **kwargs)

    @property
    def is_redis(self):
        return hasattr(self, "redis")

    @property
    def is_localisation(self):
        return hasattr(self, "localisation")

    @property
    def is_geo(self):
        return hasattr(self, "geo")
