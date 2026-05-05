from dataclasses import fields
from types import ModuleType
from typing import Literal, Optional, Type, TypeVar

from pydantic import BaseModel as PydanticBaseModel

from barsik.dto.base import BaseData
from barsik.db.domain.base import BaseModel as DomainBaseModel

from .models.base import Base


DomainT = TypeVar("DomainT", bound=DomainBaseModel)
DtoT = TypeVar("DtoT", bound=PydanticBaseModel)


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


class Mapper:

    @staticmethod
    def to_domain(
            dto: PydanticBaseModel,
            domain_cls: Type[DomainT],
            *,
            exclude: set[str] | None = None,
            exclude_unset: bool = False,
            mode: Literal["json", "python"] = "python",
    ) -> DomainT:
        data = dto.model_dump(mode=mode, by_alias=True, exclude_unset=exclude_unset)
        domain_fields = {f.name for f in fields(domain_cls)}

        if exclude:
            domain_fields -= exclude

        return domain_cls(**{
            k: v for k, v in data.items() if k in domain_fields
        })

    @staticmethod
    def to_dto(
            dto_cls: Type[DtoT],
            data: DomainBaseModel,
            *,
            exclude: set | None = None,
            exclude_unset: bool = False,
    ) -> DtoT:
        dto_fields = set(dto_cls.model_fields.keys())

        return dto_cls(**{
            k: v for k, v in data.dict(exclude=exclude, exclude_unset=exclude_unset).items() if k in dto_fields
        })
