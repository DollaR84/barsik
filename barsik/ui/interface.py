from typing import Any

from barsik.config import BaseConfig

from .base import BaseUIAdapter


class BaseUI:

    def __init__(self, cfg: BaseConfig, *names: str):
        self.adapter = BaseUIAdapter(cfg, *names)

    def register(self, **kwargs: Any) -> None:
        self.adapter.register(**kwargs)
