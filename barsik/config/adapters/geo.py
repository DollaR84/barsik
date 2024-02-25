from dataclasses import dataclass

from .base import BaseConfigAdapter


@dataclass
class GeoData:
    location_timeout: int = 5


class GeoAdapter(BaseConfigAdapter):
    data: GeoData = GeoData
