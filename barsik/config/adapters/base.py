from __future__ import annotations

from abc import ABC
from typing import Any, Type

from barsik.adapters import BaseAdapter


class BaseConfigAdapter(BaseAdapter["BaseConfigAdapter"], ABC):
    _adapters: dict[str, Type[BaseConfigAdapter]] = {}
    data: Any

    def __init__(self, config: Any, *names: str, **kwargs: Any):
        for name in names:
            adapter = self.get_adapter(name)
            if not adapter:
                continue

            adapter_data = self.get_data(adapter, **kwargs)
            setattr(config, name, adapter_data)

    def get_data(self, adapter: Type[BaseConfigAdapter], **kwargs: Any) -> Any:
        return adapter.data(**kwargs)
