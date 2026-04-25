from __future__ import annotations

from abc import ABC
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from barsik.db.base import BaseDBAdapter as BaseDBAdapter_


class BaseDBAdapter(BaseDBAdapter_, ABC, base=True):

    def get_statement(self, model: BaseDBAdapter.base, need_check_get_fields: bool = True, **kwargs: Any) -> Select:
        stmt = select(model)

        for key, value in kwargs.items():
            if key not in dir(model):
                raise AttributeError(f"Unknown attribute '{key}'")
            if need_check_get_fields and model.GET_FIELDS and key not in model.GET_FIELDS:
                continue

            stmt = stmt.where(getattr(model, key) == value)

        return stmt

    async def get(  # pylint: disable=redefined-builtin
            self,
            model: BaseDBAdapter.base,
            id: Any = None,
            **kwargs: Any,
    ) -> BaseDBAdapter.base:
        if not self.session:
            raise RuntimeError("session not initialized")

        if id:
            kwargs["id"] = id
        elif not kwargs:
            return None

        stmt = self.get_statement(model, **kwargs)

        if isinstance(self.session, AsyncSession):
            return await self.session.scalar(stmt)
        return self.session.scalar(stmt)

    async def get_list(self, model: BaseDBAdapter.base, **kwargs: Any) -> list[BaseDBAdapter.base]:
        if not self.session:
            raise RuntimeError("session not initialized")

        stmt = self.get_statement(model, need_check_get_fields=False, **kwargs)

        if isinstance(self.session, AsyncSession):
            res = await self.session.execute(stmt)
        else:
            res = self.session.execute(stmt)

        results = list(res.all())
        if results and len(results[0]) == 1:
            results = [el[0] for el in results]
        return results

    async def create(self, model: BaseDBAdapter.base, **kwargs: Any) -> BaseDBAdapter.base:
        if not self.session:
            raise RuntimeError("session not initialized")

        obj = model(**kwargs)
        self.session.add(obj)

        if isinstance(self.session, AsyncSession):
            await self.session.commit()
        else:
            self.session.commit()
        return obj

    async def update(self, model: BaseDBAdapter.base, data_for_update: dict[str, Any], **kwargs: Any) -> bool:
        if not self.session:
            raise RuntimeError("session not initialized")

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
        if isinstance(self.session, AsyncSession):
            await self.session.execute(stmt)
            await self.session.commit()
        else:
            self.session.execute(stmt)
            self.session.commit()

        return True
