from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass
class GeoData:
    location_timeout: int = 5


class GeoAdapter(BaseConfigAdapter):
    data: Type[GeoData] = GeoData
