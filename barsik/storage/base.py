from abc import abstractmethod
from typing import Any


class BaseStorage:
    def __init__(self) -> None:
        self.data: dict[str, dict[str, Any]] = {}

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def wait_closed(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_data(self, key: str | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, name: str, key: str | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *names: str, key: str | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def set_data(self, data: dict[str, Any], key: str | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: str, value: Any, key: str | None = None, ex: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *names: str, key: str | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_data(
            self,
            data: dict[str, Any] | None = None,
            key: str | None = None,
            **kwargs: Any,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def keys(self, key: str | None = None, pattern: str = "*") -> list[str]:
        raise NotImplementedError

    def set_local_data(self, key: str, data: dict[str, Any]) -> None:
        self.data[key] = data

    def get_local_data(self, key: str) -> dict[str, Any]:
        return self.data.get(key, {})
