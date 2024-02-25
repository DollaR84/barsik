from aiogram import types

from barsik.models import User

from barsik import schemas


def get_user(message_or_callback_query: types.Message | types.CallbackQuery) -> schemas.User:
    if isinstance(message_or_callback_query, types.Message):
        message = message_or_callback_query
    else:
        message = message_or_callback_query.message

    return schemas.User(
        chat_id=message.chat.id,
        username=message_or_callback_query.from_user.username,
        first_name=message_or_callback_query.from_user.first_name,
        last_name=message_or_callback_query.from_user.last_name,
        lang=message_or_callback_query.from_user.language_code,
    )


def get_name(user: User) -> str:
    name = user.first_name
    if user.last_name:
        name = " ".join([name, user.last_name]) if name else user.last_name
    if not name:
        name = user.username
    if not name:
        name = user.chat_id
    return name
