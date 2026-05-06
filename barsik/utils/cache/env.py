import os


class EnvFieldsCache:

    def __init__(self) -> None:
        self._cache: dict[str, list[str]] = {}
        for key in os.environ:
            if "_" not in key:
                continue

            prefix, field = key.split("_", 1)
            if prefix not in self._cache:
                self._cache[prefix] = []

            self._cache[prefix].append(field)

    def is_section(self, prefix: str) -> bool:
        return prefix in self._cache

    def is_field(self, prefix: str, field: str) -> bool:
        section = self._cache[prefix]
        return field in section

    def check_fields(self, prefix: str, fields: list[str]) -> list[str]:
        section = self._cache[prefix]
        unset_fields = []

        for field in fields:
            if field not in section:
                unset_fields.append(field)
        return unset_fields
