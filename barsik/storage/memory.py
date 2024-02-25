from .base import BaseStorage


class MemoryStorage(BaseStorage):

    async def wait_closed(self):
        pass

    async def close(self):
        self.data.clear()

    async def get_data(self, key: str | None = None) -> dict:
        return self.get_local_data(key) if key else self.data

    async def get(self, name: str, key: str | None = None) -> str | None:
        data = await self.get_data(key)
        if not data:
            return None
        return data.get(name)

    async def get_list(self, *names: str, key: str | None = None) -> dict[str, str]:
        data = await self.get_data(key)
        if not data:
            return {}

        return {
            name: data.get(name)
            for name in names
        }

    async def update_data(
            self,
            data: dict | None = None,
            key: str | None = None,
            **kwargs
    ):
        if data is None:
            data = {}
        data.update(**kwargs)
        await self.set_data(data, key)

    async def set_data(self, data: dict, key: str | None = None):
        if key and not self.data.get(key):
            self.data[key] = {}
        (await self.get_data(key)).update(data)

    async def set(self, name: str, value: str, key: str | None = None):
        if key and not self.data.get(key):
            self.data[key] = {}
        (await self.get_data(key)).update({name: value})

    async def delete(self, *names: str, key: str | None = None):
        if key is None:
            obj = await self.get_data(key)
            for name in names:
                obj.pop(name, None)

    async def reset_data(self, key: str | None = None):
        await self._cleanup(key)

    async def _cleanup(self, key: str | None = None):
        (await self.get_data(key)).clear()

    async def clear(self):
        self.data.clear()

    async def keys(self, key: str | None = None, pattern: str = "*") -> list[str]:
        return list(self.data.get(key).keys()) if key else list(self.data.keys())
