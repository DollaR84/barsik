from __future__ import annotations

from abc import ABC
from typing import Any, Type

from barsik.adapters import BaseAdapter
from barsik.config import BaseConfig


class BaseUIAdapter(BaseAdapter["BaseUIAdapter"], ABC):
    _adapters: dict[str, Type[BaseUIAdapter]] = {}

    def __init__(self, cfg: BaseConfig, *names: str):
        self.cfg = cfg
        self.adapter = None

        for name in names:
            adapter = self.get_adapter(name)
            if not adapter:
                continue

            self.adapter = adapter

    def register(self, **kwargs: Any) -> None:
        if self.adapter:
            self.adapter.register(**kwargs)
