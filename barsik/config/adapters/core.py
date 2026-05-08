from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class CoreConfig:
    app_name: str = "barsik"


class CoreConfigAdapter(BaseConfigAdapter[CoreConfig]):
    data: Type[CoreConfig] = CoreConfig
    optional = True
