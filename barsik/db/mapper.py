from barsik.models.base import Base

from .base import BaseDBAdapter


class BaseDataMapper:

    def __init__(
        self,
        adapter: BaseDBAdapter,
        db_models, models,
    ):
        self.adapter = adapter
        self.db_models = db_models
        self.models = models

    def get_db_model(self, model: Base) -> BaseDBAdapter.base:
        db_model = getattr(self.db_models, model.__class__.__name__, None)

        if not db_model:
            raise TypeError(f"Database not exist {model.__class__.__name__} model")

        return db_model

    def from_db_model(self, db_model: BaseDBAdapter.base) -> Base:
        model = getattr(self.models, db_model.__class__.__name__, None)

        if not model:
            raise TypeError(f"models not exist {db_model.__class__.__name__} model")

        return model(**db_model.dict())

    async def create(self, model: Base):
        db_model = self.get_db_model(model)

        async with self.adapter() as session:
            result = await session.create(db_model, **model.dict(exclude=["id"]))
            return self.from_db_model(result) if result else None

    async def get(self, model: Base):
        db_model = self.get_db_model(model)

        async with self.adapter() as session:
            result = await session.get(db_model, **model.dict())
            return self.from_db_model(result) if result else None

    async def get_list(self, model: Base):
        db_model = self.get_db_model(model)

        async with self.adapter() as session:
            results = await session.get_list(db_model, **model.dict())
            return [self.from_db_model(res) for res in results if res]

    async def update(self, model: Base, **kwargs) -> bool:
        db_model = self.get_db_model(model)

        async with self.adapter() as session:
            return await session.update(db_model, kwargs, **model.dict())

    async def get_or_create(self, model: Base):
        result = await self.get(model)
        if not result:
            result = await self.create(model)
        return result

    async def create_or_update(self, model: Base):
        result = await self.get_or_create(model)
        await self.update(model, **model.dict())
        return await  self.get(model)
