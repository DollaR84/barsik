from enum import Enum


class Main(Enum):
    CORE = "core"
    GEO = "geo"
    LOCALISATION = "localisation"
    SERVICES = "services"


class DB(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"


class Storage(Enum):
    MEMORY = "memory"
    REDIS = "redis"


class GUI(Enum):
    TELEGRAM = "telegram"
    WX = "wx"
