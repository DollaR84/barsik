from pydantic import BaseModel


class User(BaseModel):
    chat_id: int
    username: str | None = None

    first_name: str | None = None
    last_name: str | None = None

    lang: str | None = None
