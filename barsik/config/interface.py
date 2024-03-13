from .adapters.base import BaseConfigAdapter


class BaseConfig:

    def __init__(self, *names: list[str], **kwargs):
        BaseConfigAdapter(self, *names, **kwargs)

        self._core = None
        self._geo = None
        self._localisation = None
        self._redis = None
        self._services = None
        self._sqlite = None
        self._telegram = None

    @property
    def is_redis(self):
        return hasattr(self, "redis")

    @property
    def is_localisation(self):
        return hasattr(self, "localisation")

    @property
    def is_geo(self):
        return hasattr(self, "geo")

    @property
    def core(self):
        return self._core

    @core.setter
    def core(self, value):
        self._core = value

    @property
    def geo(self):
        return self._geo

    @geo.setter
    def geo(self, value):
        self._geo = value

    @property
    def localisation(self):
        return self._localisation

    @localisation.setter
    def localisation(self, value):
        self._localisation = value

    @property
    def redis(self):
        return self._redis

    @redis.setter
    def redis(self, value):
        self._redis = value

    @property
    def services(self):
        return self._services

    @services.setter
    def services(self, value):
        self._services = value

    @property
    def sqlite(self):
        return self._sqlite

    @sqlite.setter
    def sqlite(self, value):
        self._sqlite = value

    @property
    def telegram(self):
        return self._telegram

    @telegram.setter
    def telegram(self, value):
        self._telegram = value
