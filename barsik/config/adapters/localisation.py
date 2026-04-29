from dataclasses import dataclass
from typing import Type

from .base import BaseConfigAdapter


@dataclass(frozen=True, slots=True)
class LocalisationConfig:
    current_language: str = "uk"

    languages_file_path_json: str = "languages.json"
    languages_file_path_dat: str = "languages.dat"

    redis_db: int = 7
    redis_prefix: str = "langs"


class LocalisationConfigAdapter(BaseConfigAdapter[LocalisationConfig]):
    data: Type[LocalisationConfig] = LocalisationConfig
    optional = True
