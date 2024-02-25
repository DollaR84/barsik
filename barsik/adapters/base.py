from __future__ import annotations

from abc import ABC
import inspect
from typing import Type

from barsik.utils.text import paschal_case_to_snake_case


class BaseAdapter(ABC):

    def __init_subclass__(cls, **kwargs):
        if not inspect.isabstract(cls):
            base = kwargs.get("base", False)
            if base:
                return

            adapter_name = paschal_case_to_snake_case(cls.__name__.replace("Adapter", ""))
            if adapter_name in cls._adapters:
                raise TypeError(f"adapter with name {cls.__name__} has already been registered")
            cls._adapters[adapter_name] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def get_adapter(cls, name: str) -> Type[BaseAdapter] | None:
        return cls._adapters.get(name)

    @classmethod
    def get_available_adapters_names(cls) -> list[str]:
        return list(cls._adapters.keys())
