import asyncio
from abc import ABC, abstractmethod
import sys
import json
from typing import Any, Optional

from .base import BaseStorage

if sys.version_info >= (3, 11):
    from redis import asyncio as aioredis
else:
    import aioredis


class AioRedisAdapterBase(ABC):

    def __init__(
            self, *,
            host: str = "localhost",
            port: int = 6379,
            db: Optional[int] = None,
            password: Optional[str] = None,
            ssl: Optional[bool] = None,
            pool_size: int = 10,
            prefix: Optional[str] = None,
            **kwargs: Any,
    ):
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._ssl = ssl
        self._pool_size = pool_size
        self._kwargs = kwargs
        self._prefix = (prefix,)

        self._redis: Optional["aioredis.Redis"] = None
        self._connection_lock = asyncio.Lock()

    async def get_redis(self) -> aioredis.Redis:
        async with self._connection_lock:
            if self._redis is None:
                self._redis = aioredis.Redis(
                    host=self._host,
                    port=self._port,
                    db=self._db,
                    password=self._password,
                    ssl=self._ssl,
                    max_connections=self._pool_size,
                    decode_responses=True,
                    **self._kwargs,
                )
        return self._redis

    async def close(self) -> None:
        pass

    async def wait_closed(self) -> None:
        pass

    async def flushdb(self) -> None:
        if self._redis:
            await self._redis.flushdb()

    @abstractmethod
    async def get_data(self, key: str | None = None) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get(self, name: str, key: str | None = None) -> Any:
        ...

    @abstractmethod
    async def get_list(self, *names: str, key: str | None = None) -> list[Any]:
        ...

    @abstractmethod
    async def set_data(self, data: dict[str, Any], key: str | None = None) -> None:
        ...

    @abstractmethod
    async def set(
            self, name: str,
            value: Any,
            key: str | None = None,
            ex: int | None = None,
    ) -> None:
        ...

    @abstractmethod
    async def delete(self, *names: str, key: str | None = None) -> None:
        ...

    @abstractmethod
    async def keys(self, key: str | None = None, pattern: str = "*") -> list[str]:
        ...


class AioRedisAdapterV2(AioRedisAdapterBase):

    async def set_data(self, data: dict[str, Any], key: str | None = None) -> None:
        if self._redis is None:
            return

        data = {k: json.dumps({"value": v}) for k, v in data.items()}

        if key:
            await self._redis.hset(key, mapping=data)
        else:
            await self._redis.mset(data)

    async def set(
            self, name: str,
            value: Any,
            key: str | None = None,
            ex: int | None = None,
    ) -> None:
        if self._redis is None:
            return

        value = json.dumps({"value": value})

        if key:
            await self._redis.hset(key, key=name, value=value)
            if ex:
                await self._redis.expire(key, ex)

        else:
            await self._redis.set(name, value, ex=ex)

    async def get(self, name: str, key: str | None = None) -> Any:
        if self._redis is None:
            return None

        if key:
            value = await self._redis.hget(key, name)
        else:
            value = await self._redis.get(name)

        return json.loads(value).get("value") if value else None

    async def get_list(self, *names: str, key: str | None = None) -> list[Any]:
        if self._redis is None:
            return []

        async with self._redis.pipeline(transaction=True) as pipe:
            query = pipe
            for name in names:
                if key:
                    query = query.hget(key, name)
                else:
                    query = query.get(name)
            values = await query.execute()
        return [json.loads(value).get("value") if value else None for value in values]

    async def get_data(self, key: str | None = None) -> dict[str, Any]:
        if not key or not self._redis:
            return {}

        data = await self._redis.hgetall(key)

        return {k: json.loads(v).get("value") for k, v in data.items()}

    async def delete(self, *names: str, key: str | None = None) -> None:
        if self._redis is None:
            return

        if key:
            await self._redis.hdel(key, *names)
        else:
            await self._redis.delete(*names)

    async def keys(self, key: str | None = None, pattern: str = "*") -> list[str]:
        if self._redis is None:
            return []

        if key:
            return list(await self._redis.hkeys(key))
        return list(await self._redis.keys(pattern))


class RedisStorage(BaseStorage):

    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: Optional[int] = None,
            password: Optional[str] = None,
            ssl: Optional[bool] = None,
            pool_size: int = 10,
            prefix: Optional[str] = None,
            **kwargs: Any,
    ):
        super().__init__()

        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._ssl = ssl
        self._pool_size = pool_size
        self._kwargs = kwargs
        self._prefix = prefix

        self._redis: Optional[AioRedisAdapterBase] = None
        self._connection_lock = asyncio.Lock()

    async def _get_adapter(self) -> AioRedisAdapterBase:
        if self._redis is None:
            version = getattr(aioredis, "__version__", "2")
            major = version.split(".", maxsplit=1)[0]
            redis_version = int(major) if major.isdigit() else 2

            connection_data: dict[str, Any] = {
                "host": self._host,
                "port": self._port,
                "db": self._db,
                "password": self._password,
                "ssl": self._ssl,
                "pool_size": self._pool_size,
            }
            connection_data.update(self._kwargs)
            if redis_version == 2:
                self._redis = AioRedisAdapterV2(**connection_data)
            else:
                raise RuntimeError(f"Unsupported aioredis version: {redis_version}")
            await self._redis.get_redis()
        return self._redis

    async def close(self) -> None:
        if self._redis:
            return await self._redis.close()

    async def wait_closed(self) -> None:
        if self._redis:
            await self._redis.wait_closed()
            self._redis = None

    async def get_data(self, key: str | None = None) -> dict[str, Any]:
        redis = await self._get_adapter()
        result: dict[str, Any] = await redis.get_data(key)
        return result

    async def get(self, name: str, key: str | None = None) -> Any:
        redis = await self._get_adapter()
        return await redis.get(name, key)

    async def get_list(self, *names: str, key: str | None = None) -> dict[str, Any]:
        redis = await self._get_adapter()
        values = await redis.get_list(*names, key=key)
        return dict(zip(names, values))

    async def update_data(
            self,
            data: dict[str, Any] | None = None,
            key: str | None = None,
            **kwargs: Any,
    ) -> None:
        if data is None:
            data = {}
        data.update(**kwargs)
        await self.set_data(data, key)

    async def set_data(self, data: dict[str, Any], key: str | None = None) -> None:
        redis = await self._get_adapter()
        if key:
            self.data[key] = data
        await redis.set_data(data, key)

    async def set(self, name: str, value: Any, key: str | None = None, ex: int | None = None) -> None:
        redis = await self._get_adapter()
        await redis.set(name, value, key, ex=ex)
        if not ex:
            if key and "cache" not in key:
                if key not in self.data:
                    self.data[key] = {}
                self.data[key][name] = value

    async def clear(self) -> None:
        redis = await self._get_adapter()
        await redis.flushdb()
        self.data.clear()

    async def delete(self, *names: str, key: str | None = None) -> None:
        redis = await self._get_adapter()
        await redis.delete(*names, key=key)

    async def keys(self, key: str | None = None, pattern: str = "*") -> list[str]:
        redis = await self._get_adapter()
        return await redis.keys(key, pattern)
