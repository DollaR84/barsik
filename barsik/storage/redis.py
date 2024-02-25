import asyncio
import typing
import json

import aioredis

from .base import BaseStorage


class AioRedisAdapterBase:

    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: typing.Optional[int] = None,
            password: typing.Optional[str] = None,
            ssl: typing.Optional[bool] = None,
            pool_size: int = 10,
            prefix: str = None,
            **kwargs,
    ):
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._ssl = ssl
        self._pool_size = pool_size
        self._kwargs = kwargs
        self._prefix = (prefix,)

        self._redis: typing.Optional["aioredis.Redis"] = None
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

    async def close(self):
        pass

    async def wait_closed(self):
        pass

    async def flushdb(self):
        return await self._redis.flushdb()


class AioRedisAdapterV2(AioRedisAdapterBase):

    async def set_data(self, data: dict, key: str | None = None):
        data = {k: json.dumps({"value": v}) for k, v in data.items()}

        if key:
            return await self._redis.hset(key, mapping=data)
        return await self._redis.mset(data)

    async def set(
            self, name: str,
            value: str | int | None,
            key: str | None = None,
    ):
        value = json.dumps({"value": value})

        if key:
            return await self._redis.hset(key, key=name, value=value)
        return await self._redis.set(name, value)

    async def get(self, name, key: str | None = None):
        if key:
            value = await self._redis.hget(key, name)
        else:
            value = await self._redis.get(name)

        return json.loads(value).get("value") if value else None

    async def get_list(self, *names: str, key: str | None = None):
        async with self._redis.pipeline(transaction=True) as pipe:
            query = pipe
            for name in names:
                if key:
                    query = query.hget(key, name)
                else:
                    query = query.get(name)
            values = await query.execute()
        return [json.loads(value).get("value") if value else None for value in values]

    async def get_data(self, key: str | None = None) -> dict | None:
        data = await self._redis.hgetall(key) if key else None

        return {k: json.loads(v).get("value") for k, v in data.items()} if data else {}

    async def delete(self, *names, key: str | None = None):
        if key:
            return await self._redis.hdel(key, *names)
        return await self._redis.delete(*names)

    async def keys(self, key: str | None = None, pattern: str = "*"):
        if key:
            return list(await self._redis.hkeys(key))
        return list(await self._redis.keys(pattern))


class RedisStorage(BaseStorage):

    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: typing.Optional[int] = None,
            password: typing.Optional[str] = None,
            ssl: typing.Optional[bool] = None,
            pool_size: int = 10,
            prefix: str = None,
            **kwargs,
    ):
        super().__init__()

        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._ssl = ssl
        self._pool_size = pool_size
        self._kwargs = kwargs
        self._prefix = (prefix,)

        self._redis: typing.Optional[AioRedisAdapterBase] = None
        self._connection_lock = asyncio.Lock()

    async def _get_adapter(self) -> AioRedisAdapterBase:
        if self._redis is None:
            redis_version = int(aioredis.__version__.split(".", maxsplit=1)[0])
            connection_data = {
                "host": self._host,
                "port": self._port,
                "db": self._db,
                "password": self._password,
                "ssl": self._ssl,
                "pool_size": self._pool_size,
            }
            connection_data.update(**self._kwargs,)
            if redis_version == 2:
                self._redis = AioRedisAdapterV2(**connection_data)
            else:
                raise RuntimeError(f"Unsupported aioredis version: {redis_version}")
            await self._redis.get_redis()
        return self._redis

    async def close(self):
        if self._redis:
            return await self._redis.close()

    async def wait_closed(self):
        if self._redis:
            await self._redis.wait_closed()
            self._redis = None

    async def get_data(self, key: str | None = None) -> dict | None:
        redis = await self._get_adapter()
        return await redis.get_data(key)

    async def get(self, name: str, key: str | None = None) -> str | None:
        redis = await self._get_adapter()
        return await redis.get(name, key)

    async def get_list(self, *names: str, key: str | None = None) -> dict[str, str]:
        redis = await self._get_adapter()
        values = await redis.get_list(*names, key=key)
        return dict(zip(names, values))

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
        redis = await self._get_adapter()
        self.data[key] = data
        await redis.set_data(data, key)

    async def set(self, name: str, value: str, key: str | None = None):
        redis = await self._get_adapter()
        await redis.set(name, value, key)
        if key and "cache" not in key:
            if key not in self.data:
                self.data[key] = {}
            self.data[key][name] = value

    async def clear(self):
        redis = await self._get_adapter()
        await redis.flushdb()
        self.data.clear()

    async def delete(self, *names: str, key: str | None = None):
        redis = await self._get_adapter()
        await redis.delete(*names, key=key)

    async def keys(self, key: str | None = None, pattern: str = "*"):
        redis = await self._get_adapter()
        return await redis.keys(key, pattern)
