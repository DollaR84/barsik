from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class TelegramConfig:
    token: str

    redis_db: int = 6
    redis_prefix: str = "fsm"
    redis_decode_responses: bool = True


class TelegramConfigAdapter(BaseConfigAdapter[TelegramConfig]):
    data: Type[TelegramConfig] = TelegramConfig
    prefix = "BOT"
    section_name = "bot"
