from typing import Any

from .command_handlers import CommandHandlers


class BaseHandlers:  # pylint: disable=too-few-public-methods

    @classmethod
    def register(cls, **kwargs: Any) -> None:
        CommandHandlers.register(**kwargs)
