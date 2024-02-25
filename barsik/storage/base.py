from abc import abstractmethod
from typing import Any


class BaseStorage:
    def __init__(self):
        self.data: dict[str, dict[str, Any]] = {}

    @abstractmethod
    async def close(self):
        raise NotImplementedError

    @abstractmethod
    async def wait_closed(self):
        raise NotImplementedError

    @abstractmethod
    async def get_data(self, key: str | None = None) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, name: str, key: str | None = None) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *names: str, key: str | None = None) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    async def set_data(self, data: dict, key: str | None = None):
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: str, value: str, key: str | None = None):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *names: str, key: str | None = None):
        raise NotImplementedError

    @abstractmethod
    async def update_data(
            self,
            data: dict | None = None,
            key: str | None = None,
            **kwargs
    ):
        raise NotImplementedError

    @abstractmethod
    async def clear(self):
        raise NotImplementedError

    @abstractmethod
    async def keys(self, key: str | None = None, pattern: str = "*") -> list[str]:
        raise NotImplementedError

    def set_local_data(self, key: str, data: dict):
        self.data[key] = data

    def get_local_data(self, key: str) -> dict[str, Any]:
        return self.data.get(key, {})
