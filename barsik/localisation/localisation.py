import logging
import json
import pickle
from types import ModuleType
from typing import Any, cast, NotRequired, TypedDict

import aiofiles

from barsik.config.adapters import LocalisationConfig
from barsik.storage import MemoryStorage
from barsik.storage.base import BaseStorage


class OpenKwargs(TypedDict):
    mode: str
    encoding: NotRequired[str]


class Localisation:

    def __init__(
            self,
            config: LocalisationConfig,
            storage: BaseStorage | None = None,
    ):
        if not config:
            raise RuntimeError("localisation config not be initialized")

        self.config = config
        self.current: str = self.config.current_language

        self.supported: dict[str, str] = {}
        self.is_languages_loaded: bool = False

        if not storage:
            storage = MemoryStorage()
        self.storage: BaseStorage = storage

    async def load_languages(self) -> None:
        paths = (self.config.languages_file_path_dat, self.config.languages_file_path_json,)
        last_error = None

        for path in paths:
            try:
                await self.load_from_file(path)
                self.is_languages_loaded = True
                return

            except (OSError, ValueError) as error:
                last_error = error
                self.is_languages_loaded = False
                logging.error(last_error, exc_info=True)
                raise IOError("Error: open languages file...") from last_error

    async def load_from_file(self, file_path: str) -> None:
        reader: ModuleType
        kwargs: OpenKwargs

        if file_path.endswith(".dat"):
            kwargs = {"mode": "rb"}
            reader = pickle
        elif file_path.endswith(".json"):
            kwargs = {"mode": "r", "encoding": "utf-8"}
            reader = json
        else:
            raise ValueError(f"Incorrect file extenssion. Files supported (*.dat, *.json), not {file_path}")

        async with aiofiles.open(file_path, **cast(dict[str, Any], kwargs)) as lang_file:
            file_data = reader.loads(await lang_file.read())
            self.supported = file_data.pop("languages", {})
            for lang, data in file_data.items():
                await self.set_data_from_file(lang, data)

    async def set_data_from_file(self, lang: str, data: dict[str, dict[str, str]]) -> None:
        for section_name, section_data in data.items():
            new_data = {
                f"{section_name}__{key}": value
                for key, value in section_data.items()
            }
            await self.storage.set_data(new_data, lang)

    async def get_data(
            self,
            lang: str,
            variable: str,
            section: str | None = None,
    ) -> str:
        if not self.is_languages_loaded:
            await self.load_languages()
        if not self.is_languages_loaded:
            if section:
                return f"{section} {variable}"
            return variable

        if not lang or lang not in self.supported:
            lang = self.current

        if section:
            variable = f"{section}__{variable}"

        raw_data: str = await self.storage.get(variable, lang)
        return raw_data

    async def get_text(self, lang: str, variable: str, section: str | None = None, **kwargs: Any) -> str:
        text = await self.get_data(lang, variable, section)
        if text:
            return text.format(**kwargs)
        return "error localisation"

    async def f(self, variable: str, lang: str, **kwargs: Any) -> str:
        return await self.get_text(lang, variable, **kwargs)

    async def fs(self, section: str, variable: str, lang: str, **kwargs: Any) -> str:
        return await self.get_text(lang, variable, section=section, **kwargs)
