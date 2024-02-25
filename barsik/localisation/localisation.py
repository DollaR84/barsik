import logging
import json
import pickle

import aiofiles

from barsik.config import BaseConfig
from barsik.storage import MemoryStorage
from barsik.storage.base import BaseStorage


class Localisation:

    def __init__(
            self,
            config: BaseConfig,
            storage: BaseStorage | None = None,
    ):
        self.config = config.localisation
        self.current: str = self.config.current_language

        self.supported: dict[str, str] = {}
        self.is_languages_loaded: bool = False

        if not storage:
            storage = MemoryStorage()
        self.storage: BaseStorage = storage

    async def load_languages(self):
        try:
            await self.load_from_file(self.config.languages_file_path_dat)
        except Exception:
            try:
                await self.load_from_file(self.config.languages_file_path_json)
            except Exception as error:
                self.is_languages_loaded = False
                logging.error(error, exc_info=True)
                raise IOError("Error: open languages file...") from error

        self.is_languages_loaded = True

    async def load_from_file(self, file_path: str):
        if file_path.endswith(".dat"):
            kwargs = {"mode": "rb"}
            reader = pickle
        elif file_path.endswith(".json"):
            kwargs = {"mode": "r", "encoding": "utf-8"}
            reader = json
        else:
            raise ValueError(f"Incorrect file extenssion. Files supported (*.dat, *.json), not {file_path}")

        try:
            async with aiofiles.open(file_path, **kwargs) as lang_file:
                file_data = reader.loads(await lang_file.read())
                self.supported = file_data.pop("languages", {})
                for lang, data in file_data.items():
                    await self.set_data_from_file(lang, data)
        except IOError:
            raise

    async def set_data_from_file(self, lang: str, data: dict):
        for section_name, section_data in data.items():
            new_data = {
                f"{section_name}__{key}": value
                for key, value in section_data.items()
            }
            await self.storage.set_data(new_data, lang)

    async def get_data(self, lang: str, variable: str, section: str | None = None) -> str | list | dict | None:
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
        return await self.storage.get(variable, lang)

    async def get_text(self, lang: str, variable: str, section: str | None = None, **kwargs) -> str:
        text = await self.get_data(lang, variable, section)
        if text:
            return text.format(**kwargs)
        return "error localisation"

    async def f(self, variable: str, lang: str, **kwargs) -> str:
        return await self.get_text(lang, variable, **kwargs)

    async def fs(self, section: str, variable: str, lang: str, **kwargs) -> str:
        return await self.get_text(lang, variable, section=section, **kwargs)
