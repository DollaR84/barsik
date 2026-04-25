from dataclasses import dataclass
import os
from typing import Type

from .base import BaseConfigAdapter


@dataclass
class TelegramData:
    token: str = os.getenv("BOT_TOKEN", "")

    redis_db: int = int(os.getenv("TELEGRAM_REDIS_DB", "6"))
    redis_prefix: str = "fsm"
    redis_decode_responses: bool = True


class TelegramAdapter(BaseConfigAdapter):
    data: Type[TelegramData] = TelegramData
