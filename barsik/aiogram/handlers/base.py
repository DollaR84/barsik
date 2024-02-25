from .command_handlers import CommandHandlers


class BaseHandlers:

    @classmethod
    def register(cls, **kwargs):
        CommandHandlers.register(**kwargs)
