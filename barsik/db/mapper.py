from types import ModuleType
from typing import Optional, Type

from barsik.dto.base import BaseData

from .models.base import Base


class BaseDataMapper:

    def __init__(
        self,
        db_models: ModuleType,
        models: ModuleType,
    ):
        self.db_models = db_models
        self.models = models

    def get_db_model(self, model: BaseData) -> Type[Base]:
        db_model_cls: Optional[Type[Base]] = getattr(self.db_models, model.__class__.__name__, None)

        if not db_model_cls:
            raise TypeError(f"Database not exist {model.__class__.__name__} model")

        return db_model_cls

    def from_db_model(self, db_model: Base) -> BaseData:
        model_cls: Optional[Type[BaseData]] = getattr(self.models, db_model.__class__.__name__, None)

        if not model_cls:
            raise TypeError(f"models not exist {db_model.__class__.__name__} model")

        return model_cls(**db_model.to_dict())
