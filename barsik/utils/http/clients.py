import aiohttp
from aiohttp import ClientSession

from dataclass_rest.http.aiohttp import AiohttpClient
from dataclass_rest.http.requests import RequestsClient

from adaptix import Retort, NameStyle, name_mapping

from .auth import AuthProvider


class BaseHttpClient:

    def get_retort_recipe(self) -> list:
        return [
            name_mapping(name_style=NameStyle.CAMEL),
        ]

    def _init_request_body_factory(self) -> Retort:
        return Retort(recipe=self.get_retort_recipe())


class HttpSyncClient(RequestsClient, BaseHttpClient):

    def __init__(self, url: str, auth: AuthProvider | None = None):
        super().__init__(base_url=url)

        self.session.headers.update({"Content-Type": "application/json"
        if auth:
            self.session.headers.update(auth.get_headers())


class HttpAsyncClient(AiohttpClient, BaseHttpClient):

    def __init__(self, url: str, auth: AuthProvider | None = None, session: ClientSession | None = None):
        self.base_url = url
        self._auth: AuthProvider | None = auth
        self._session: ClientSession | None = session
        self._owns_session = session is None

        if self._session is not None:
            super().__init__(base_url=self.base_url, session=self._session)
            self.update_headers()

    def update_headers(self) -> None:
        self._session.headers.update({"Content-Type": "application/json"
        if self._auth:
            self._session.headers.update(self._auth.get_headers())

    async def _ensure_session(self) -> None:
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self.update_headers()
            super().__init__(base_url=self.base_url, session=self._session)

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._owns_session and self._session:
            await self._session.close()
