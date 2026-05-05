from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class LLMConfig:
    name: str
    base_url: str
    api_key: str
    model: str


class LLMConfigAdapter(BaseConfigAdapter[LLMConfig]):
    data: Type[LLMConfig] = LLMConfig
