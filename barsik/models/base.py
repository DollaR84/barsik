from dataclasses import asdict

from pydantic import BaseModel


class Base:

    @classmethod
    def from_schema(cls, model: BaseModel):
        return cls(**model.dict())

    def dict(self, exclude_unset: bool = False, exclude: list | None = None) -> dict:
        result = asdict(self)

        if exclude_unset:
            result = {key: value for key, value in result.items() if value is not None}

        if exclude:
            result = {key: value for key, value in result.items() if key not in exclude}

        return result
