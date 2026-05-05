from dataclasses import dataclass
from typing import Optional, Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class BotConfig:
    token: str
    id: Optional[int] = None

    redis_db: int = 6
    redis_prefix: str = "fsm"
    redis_decode_responses: bool = True


class BotConfigAdapter(BaseConfigAdapter[BotConfig]):
    data: Type[BotConfig] = BotConfig
    prefix = "BOT"
    section_name = "bot"
