from __future__ import annotations

from abc import ABC
import inspect
from typing import Type, TypeVar

from barsik.utils.text import paschal_case_to_snake_case, paschal_case_to_words


T = TypeVar("T", bound="BaseAdapter")


class BaseAdapter(ABC):
    _adapters: dict[str, Type[T]]

    def __init_subclass__(cls, is_abstract: bool = False, **kwargs):
        if is_abstract:
            return

        if not inspect.isabstract(cls):
            base = kwargs.get("base", False)
            if base:
                return

            adapter_name = cls.get_name()
            if adapter_name in cls._adapters:
                suffix = cls.get_suffix()
                raise TypeError(f"{suffix.lower()} with name {cls.__name__} has already been registered")
            cls._adapters[adapter_name] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def get_name(cls) -> str:
        suffix = cls.get_suffix()
        _name = cls.__name__.replace(suffix, "")
        return paschal_case_to_snake_case(_name)

    @classmethod
    def get_suffix(cls) -> str:
        _name_list = paschal_case_to_words(cls.__name__).split(" ")
        if _name_list:
            return _name_list[-1]
        raise ValueError(f"Error get suffix for adapter '{cls.__name__}'")

    @classmethod
    def get_adapter(cls, name: str) -> Type[T] | None:
        return cls._adapters.get(name)

    @classmethod
    def get_available_adapters_names(cls) -> list[str]:
        return list(cls._adapters.keys())
