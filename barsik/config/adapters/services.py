from dataclasses import dataclass
from typing import Any, Type

from .base import BaseConfigAdapter


@dataclass
class ServicesData:
    data: Any = None


class ServicesAdapter(BaseConfigAdapter):
    data: Type[ServicesData] = ServicesData
