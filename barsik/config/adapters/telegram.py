from dataclasses import dataclass
import os

from .base import BaseConfigAdapter


@dataclass
class TelegramData:
    token: str = os.getenv("BOT_TOKEN")

    redis_db: int = os.getenv("TELEGRAM_REDIS_DB")
    redis_prefix: str = "fsm"
    redis_decode_responses: bool = True


class TelegramAdapter(BaseConfigAdapter):
    data: TelegramData = TelegramData
