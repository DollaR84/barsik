from typing import Type

from barsik.config import BaseConfig
from barsik.config.adapters.base import BaseConfigAdapter, T


def get_config_section(config: BaseConfig, adapter_cls: Type[BaseConfigAdapter[T]]) -> T:
    section_name = adapter_cls.get_section_name()
    if not section_name:
        raise RuntimeError(f"{adapter_cls.get_name()} must be set section_name")

    data: T = getattr(config, section_name)
    if data is not None:
        return data

    if adapter_cls.optional:
        return adapter_cls.load()

    raise ValueError(f"{adapter_cls.get_name()} must be set in env")
