from __future__ import annotations

from abc import ABC
from typing import Type

from barsik.adapters import BaseAdapter
from barsik.config import BaseConfig


class BaseUIAdapter(BaseAdapter, ABC):
    _adapters: dict[str, Type[BaseUIAdapter]] = {}

    def __init__(self, cfg: BaseConfig, *names: list[str]):
        self.cfg = cfg
        self.adapter = None

        for name in names:
            adapter = self.get_adapter(name)
            if not adapter:
                continue

            self.adapter = adapter

    def register(self, **kwargs):
        self.adapter.register(**kwargs)
