from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass
class CoreData:
    app_name: str = "barsik"


class CoreAdapter(BaseConfigAdapter):
    data: Type[CoreData] = CoreData
