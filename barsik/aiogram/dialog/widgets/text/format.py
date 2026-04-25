from typing import Any

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

from barsik.localisation import Localisation


class FormatLocalisation(Text):
    def __init__(
            self,
            variable: str,
            section: str | None = None,
            when: WhenCondition = None,
            keys: list[str] | None = None,
    ):
        super().__init__(when=when)
        self.variable = variable
        self.section = section
        self.keys = keys or []

    async def _render_text(self, data: dict[str, Any], manager: DialogManager) -> str:
        container = manager.middleware_data.get("dishka_container")
        if not container:
            return f"Error: No container for {manager.__class__.__name__}"

        result: str
        local = await container.get(Localisation)

        start_data = data.get("start_data", {})
        lang = start_data.get("lang", local.current)
        data_ = {key: data.get(key) for key in self.keys}

        if self.section:
            result = await local.fs(self.section, self.variable, lang, **data_)
        else:
            result = await local.f(self.variable, lang, **data_)

        return result
