from dataclasses import dataclass
from typing import Self

from pydantic import BaseModel

from barsik.utils.data import Base


@dataclass(slots=True)
class BaseData(Base):

    @classmethod
    def from_schema(cls, model: BaseModel) -> Self:
        return cls(**model.dict())
