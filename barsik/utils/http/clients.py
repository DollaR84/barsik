from functools import cached_property
from types import TracebackType
from typing import Optional, Self, Type

import aiohttp
from aiohttp import ClientSession
from requests import Session

from adaptix import NameStyle, name_mapping, Provider, Retort
from descanso.client import Dumper, Loader
from descanso.http.aiohttp import AiohttpClient
from descanso.http.requests import RequestsClient

from .auth import AuthProvider


class BaseHttpClient:

    @property
    def headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    def get_retort_recipe(self) -> list[Provider]:
        return [
            name_mapping(name_style=NameStyle.CAMEL),
        ]

    @cached_property
    def _retort(self) -> Retort:
        return Retort(recipe=self.get_retort_recipe())

    def _get_request_body_dumper(self) -> Dumper:
        return self._retort

    def _get_response_body_loader(self) -> Loader:
        return self._retort


class HttpSyncClient(RequestsClient, BaseHttpClient):

    def __init__(self, url: str, auth: AuthProvider | None = None):
        session = Session()
        session.headers.update(self.headers)
        if auth:
            session.headers.update(auth.get_headers())

        super().__init__(base_url=url, session=session)


class HttpAsyncClient(AiohttpClient, BaseHttpClient):

    def __init__(self, url: str, auth: AuthProvider | None = None, session: ClientSession | None = None):
        self.base_url = url
        self._auth: AuthProvider | None = auth
        self.session: ClientSession | None = session
        self._owns_session = session is None

        if self.session is not None:
            self.update_headers()
            super().__init__(base_url=self.base_url, session=self.session)

    def update_headers(self) -> None:
        if self.session is None:
            raise RuntimeError("session not be initialized")

        self.session.headers.update(self.headers)
        if self._auth:
            self.session.headers.update(self._auth.get_headers())

    async def _ensure_session(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self.update_headers()
            super().__init__(base_url=self.base_url, session=self.session)

    async def __aenter__(self) -> Self:
        await self._ensure_session()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        if self._owns_session and self.session:
            await self.session.close()
