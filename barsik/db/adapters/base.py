from __future__ import annotations

from abc import ABC
from typing import Any

from barsik.db.base import BaseDBAdapter as BaseDBAdapter_

from sqlalchemy import select, update
from sqlalchemy.sql import Select


class BaseDBAdapter(BaseDBAdapter_, ABC, base=True):

    def get_statement(self, model: BaseDBAdapter.base, need_check_get_fields: bool = True, **kwargs) -> Select:
        stmt = select(model)

        for key, value in kwargs.items():
            if key not in dir(model):
                raise AttributeError(f"Unknown attribute '{key}'")
            if need_check_get_fields and model.GET_FIELDS and key not in model.GET_FIELDS:
                continue

            stmt = stmt.where(getattr(model, key) == value)

        return stmt

    async def get(self, model: BaseDBAdapter.base, id: Any = None, **kwargs):
        if id:
            kwargs["id"] = id
        elif not kwargs:
            return None

        stmt = self.get_statement(model, **kwargs)

        return await self.session.scalar(stmt)

    async def get_list(self, model: BaseDBAdapter.base, **kwargs):
        stmt = self.get_statement(model, need_check_get_fields=False, **kwargs)
        res = await self.session.execute(stmt).all()
        if res and len(res[0]) == 1:
            res = [el[0] for el in res]
        return res

    async def create(self, model: BaseDBAdapter.base, **kwargs):
        obj = model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def update(self, model: BaseDBAdapter.base, data_for_update: dict, **kwargs):
        if model.NO_UPDATE_FIELDS:
            data_for_update = {
                key: value for key, value in data_for_update.items()
                if key not in model.NO_UPDATE_FIELDS
            }
        if model.UPDATE_FIELDS:
            data_for_update = {
                key: value for key, value in data_for_update.items()
                if key in model.UPDATE_FIELDS
            }

        conditions = []
        for key, value in kwargs.items():
            if model.GET_FIELDS and (key not in model.GET_FIELDS or not value):
                continue

            conditions.append((getattr(model, key) == value))

        stmt = update(model).where(*conditions).values(data_for_update)
        await self.session.execute(stmt)

        await self.session.commit()
        return True
