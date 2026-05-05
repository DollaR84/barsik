from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class TelegramConfig:
    api_id: int
    api_hash: str

    workdir: str = "/app/sessions/"


class TelegramConfigAdapter(BaseConfigAdapter[TelegramConfig]):
    data: Type[TelegramConfig] = TelegramConfig
    prefix = "TELEGRAM"
    section_name = "telegram"
