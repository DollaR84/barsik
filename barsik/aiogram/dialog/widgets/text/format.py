from typing import Dict

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Format

from barsik.localisation import Localisation


class FormatLocalisation(Format):
    def __init__(
            self,
            variable: str,
            section: str | None = None,
            when: WhenCondition = None,
            keys: list[str] | None = None,
    ):
        super().__init__(when)
        self.variable = variable
        self.section = section
        self.keys = keys or []

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        container = manager.middleware_data.get("dishka_container")
        local = await container.get(Localisation)

        start_data = data.get("start_data", {})
        lang = start_data.get("lang", local.current)
        data = {key: data.get(key) for key in self.keys}

        if self.section:
            return await local.fs(self.section, self.variable, lang, **data)
        return await local.f(self.variable, lang, **data)
