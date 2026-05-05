from __future__ import annotations

from abc import ABC
from dataclasses import fields, MISSING
from typing import Any, Generic, Optional, Type, TypeVar

import dature
from dature.protocols import DataclassInstance

from barsik.adapters import BaseAdapter


T = TypeVar("T", bound=DataclassInstance)


class BaseConfigAdapter(BaseAdapter["BaseConfigAdapter"], ABC, Generic[T], is_abstract=True):
    _adapters: dict[str, Type[BaseConfigAdapter]] = {}
    data: Type[T]
    prefix: Optional[str] = None
    section_name: Optional[str] = None
    optional: bool = False

    @classmethod
    def get_prefix(cls) -> str:
        return cls.prefix or cls.get_name().upper()

    @classmethod
    def get_section_name(cls) -> str:
        return cls.section_name or cls.get_name().lower()

    @classmethod
    def load(cls) -> T:
        prefix = cls.get_prefix()

        data = dature.load(
            dature.EnvSource(prefix=f"{prefix}_"),
            secret_field_names=("token", "password",),
            mask_secrets=True,
            schema=cls.data,
        )
        setattr(data, "__loaded__", not cls.is_empty(data))
        return data

    @classmethod
    def is_empty(cls, data: T) -> bool:
        for f in fields(data):
            value = getattr(data, f.name)
            if f.default is not MISSING:
                if value != f.default:
                    return False

            elif f.default_factory is not MISSING:
                if value != f.default_factory():
                    return False

            else:
                if value is not None:
                    return False

        return True

    def __init__(self, config: Any):
        for adapter_cls in self._adapters.values():
            data = adapter_cls.load()
            if not getattr(data, "__loaded__", False):
                continue

            name = adapter_cls.get_section_name()
            setattr(config, name, data)
