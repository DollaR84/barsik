from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class LlmConfig:
    name: str
    base_url: str
    api_key: str
    model: str


class LlmConfigAdapter(BaseConfigAdapter[LlmConfig]):
    data: Type[LlmConfig] = LlmConfig
