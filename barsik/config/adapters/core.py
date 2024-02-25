from dataclasses import dataclass

from .base import BaseConfigAdapter


@dataclass
class CoreData:
    app_name: str = "barsik"


class CoreAdapter(BaseConfigAdapter):
    data: CoreData = CoreData
