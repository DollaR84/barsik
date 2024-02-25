from enum import Enum


class Main(Enum):
    CORE: str = "core"
    GEO: str = "geo"
    LOCALISATION: str = "localisation"
    SERVICES: str = "services"


class DB(Enum):
    SQLITE: str = "sqlite"
    MYSQL: str = "mysql"


class Storage(Enum):
    MEMORY: str = "memory"
    REDIS: str = "redis"


class GUI(Enum):
    TELEGRAM: str = "telegram"
    WX: str = "wx"
