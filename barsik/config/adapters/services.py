from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class BaseServicesConfig:
    pass


class ServicesConfigAdapter(BaseConfigAdapter[BaseServicesConfig]):
    data: Type[BaseServicesConfig] = BaseServicesConfig
