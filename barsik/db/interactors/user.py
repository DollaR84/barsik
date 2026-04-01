from abc import abstractmethod

from barsik.db import BaseDB
from barsik.models import User


class BaseUserInteractor:

    @abstractmethod
    async def get_user(self, user_id: int) -> User:
        raise NotImplementedError


class UserInteractor(BaseUserInteractor):

    def __init__(self, db: BaseDB):
        self.db = db

    async def get_user(self, user_id: int | None = None, chat_id: int | None = None) -> User:
        db_model = self.db.mapper.get_db_model(User)
        async with self.db.adapter() as session:
            result = await session.get(db_model, id=user_id, chat_id=chat_id)
            return self.db.mapper.from_db_model(result) if result else None
