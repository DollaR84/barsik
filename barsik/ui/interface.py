from barsik.config import BaseConfig

from .base import BaseUIAdapter


class BaseUI:

    def __init__(self, cfg: BaseConfig, *names: list[str]):
        self.adapter = BaseUIAdapter(cfg, *names)

    def register(self, **kwargs):
        self.adapter.register(**kwargs)
