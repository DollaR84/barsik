from dataclasses import dataclass
import os

from .base import BaseConfigAdapter


@dataclass
class LocalisationData:
    current_language: str = "uk"

    languages_file_path_json: str = "languages.json"
    languages_file_path_dat: str = "languages.dat"

    redis_db: int = os.getenv("LOCALISATION_REDIS_DB")
    redis_prefix: str = "langs"


class LocalisationAdapter(BaseConfigAdapter):
    data: LocalisationData = LocalisationData
