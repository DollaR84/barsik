from abc import abstractmethod


class AuthProvider:

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        raise RuntimeError("need to define an authorization provider")


class BearerAuth(AuthProvider):

    def __init__(self, token: str):
        self.token = token

    def get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
        }
