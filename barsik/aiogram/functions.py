from aiogram import types

from barsik.models import User

from barsik import schemas


def get_user(message_or_callback_query: types.Message | types.CallbackQuery) -> schemas.User:
    user = message_or_callback_query.from_user
    if user is None:
        raise RuntimeError("Event must have a from_user")

    if isinstance(message_or_callback_query, types.Message):
        chat_id = message_or_callback_query.chat.id
    else:
        if message_or_callback_query.message is None:
            raise RuntimeError("callback_query.message must be set")
        chat_id = message_or_callback_query.message.chat.id

    return schemas.User(
        chat_id=chat_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        lang=user.language_code,
    )


def get_name(user: User) -> str:
    name = user.first_name
    if user.last_name:
        name = " ".join([name, user.last_name]) if name else user.last_name
    if not name:
        name = user.username
    if not name:
        name = str(user.chat_id)
    return name
