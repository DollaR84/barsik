from dataclasses import dataclass

from .base import BaseConfigAdapter


@dataclass
class ServicesData:
    data: None = None


class ServicesAdapter(BaseConfigAdapter):
    data: ServicesData = ServicesData
