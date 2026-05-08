from __future__ import annotations

from abc import ABC
from dataclasses import fields, MISSING
import logging
from typing import Any, Generic, Optional, Type, TypeVar

import dature
from dature.protocols import DataclassInstance
from dature.sources.base import Source

from barsik.adapters import BaseAdapter
from barsik.utils.cache.env import EnvFieldsCache
from barsik.utils.text import paschal_case_to_words


T = TypeVar("T", bound=DataclassInstance)


class BaseConfigAdapter(BaseAdapter["BaseConfigAdapter"], ABC, Generic[T], is_abstract=True):
    _adapters: dict[str, Type[BaseConfigAdapter]] = {}
    data: Type[T]
    prefix: Optional[str] = None
    section_name: Optional[str] = None
    optional: bool = False
    secret_field_names: Optional[tuple[str, ...]] = None

    @classmethod
    def get_prefix(cls) -> str:
        prefix = paschal_case_to_words(cls.__name__).split()[0].upper()
        return cls.prefix or prefix

    @classmethod
    def get_section_name(cls) -> str:
        section_name = paschal_case_to_words(cls.__name__).split()[0].lower()
        return cls.section_name or section_name

    @classmethod
    def load(cls) -> T:
        prefix = cls.get_prefix()
        sources: list[Source] = [
            dature.EnvSource(prefix=f"{prefix}_"),
        ]

        data = dature.load(
            *sources,
            secret_field_names=cls.secret_field_names,
            mask_secrets=True,
            schema=cls.data,
        )

        return data

    @classmethod
    def get_mandatory_fields(cls) -> list[str]:
        return [
            field.name for field in fields(cls.data)
            if field.default is MISSING and field.default_factory is MISSING
        ]

    def __init__(self, config: Any):
        logger = logging.getLogger()
        env_cache = EnvFieldsCache()

        for adapter_cls in self._adapters.values():
            prefix = adapter_cls.get_prefix()
            section_name = adapter_cls.get_section_name()

            if not env_cache.is_section(prefix):
                continue

            unset_fields = env_cache.check_fields(prefix, adapter_cls.get_mandatory_fields())
            if unset_fields:
                logger.error("unset fields: %s", str(["_".join([prefix, field.upper()]) for field in unset_fields]))
                continue

            data = adapter_cls.load()
            if not data:
                continue

            if getattr(config, section_name) is not None:
                continue
            setattr(config, section_name, data)
