from dataclasses import dataclass

from barsik.utils.data import Base


@dataclass(slots=True)
class BaseModel(Base):
    pass
