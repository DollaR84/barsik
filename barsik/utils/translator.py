import re
from html import unescape
from typing import Any

from descanso import RestBuilder
from descanso.client import Loader

from barsik.utils.http import HttpSyncClient


rest = RestBuilder()


class RawTextLoader:

    def load(self, data: Any, _: Any) -> Any:
        return data


class GoogleTranslateClient(HttpSyncClient):

    def __init__(self) -> None:
        super().__init__("http://translate.google.com/")

    @property
    def headers(self) -> dict[str, str]:
        return {
            "User-Agent": "Mozilla/4.0 (\
            compatible;\
            MSIE 6.0;\
            Windows NT 5.1;\
            SV1;\
            .NET CLR 1.1.4322;\
            .NET CLR 2.0.50727;\
            .NET CLR 3.0.04506.30\
            )"
        }

    def _get_response_body_loader(self) -> Loader:
        return RawTextLoader()

    @rest.get("m")
    def _get_translation_html(self, sl: str, hl: str, tl: str, q: str) -> str:
        raise NotImplementedError

    def translate(self, text: str, to_language: str = "auto", from_language: str = "auto") -> str:
        html_content = self._get_translation_html(
            sl=from_language,
            hl=to_language,
            tl=to_language,
            q=text,
        )

        expr = r'class="result-container">(.*?)<'
        data = re.findall(expr, html_content)

        result = unescape(data[0]) if data else ""
        return result
