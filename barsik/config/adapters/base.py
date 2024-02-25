from __future__ import annotations

from abc import ABC
from typing import Type

from barsik.adapters import BaseAdapter


class BaseConfigAdapter(BaseAdapter, ABC):
    _adapters: dict[str, Type[BaseConfigAdapter]] = {}

    def __init__(self, config, *names: list[str], **kwargs):
        for name in names:
            adapter = self.get_adapter(name)
            if not adapter:
                continue

            adapter_data = self.get_data(adapter, **kwargs)
            setattr(config, name, adapter_data)

    def get_data(self, adapter: Type[BaseConfigAdapter], **kwargs):
        return adapter.data(**kwargs)
