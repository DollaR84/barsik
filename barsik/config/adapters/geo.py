from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class GeoConfig:
    location_timeout: int = 5


class GeoConfigAdapter(BaseConfigAdapter[GeoConfig]):
    data: Type[GeoConfig] = GeoConfig
    optional = True
