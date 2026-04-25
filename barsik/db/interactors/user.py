from abc import abstractmethod
from typing import Optional

from barsik.db import BaseDB
from barsik.models import User


class BaseUserInteractor:

    def __init__(self, db: BaseDB):
        self.db = db

    @abstractmethod
    async def get_user(self, user_id: int | None = None, chat_id: int | None = None) -> Optional[User]:
        raise NotImplementedError


class UserInteractor(BaseUserInteractor):

    async def get_user(self, user_id: int | None = None, chat_id: int | None = None) -> Optional[User]:
        if not self.db.mapper:
            return None

        db_model = self.db.mapper.get_db_model(User)
        async with self.db.adapter() as session:
            result = await session.get(db_model, id=user_id, chat_id=chat_id)
            return self.db.mapper.from_db_model(result) if result else None
