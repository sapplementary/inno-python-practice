import os
from dataclasses import dataclass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Не задана переменная окружения {name}")
    return value


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    dbname: str
    user: str
    password: str

    @classmethod
    def from_env(cls) -> "DbConfig":
        return cls(
            host=_require_env("DB_HOST"),
            port=int(_require_env("DB_PORT")),
            dbname=_require_env("DB_NAME"),
            user=_require_env("DB_USER"),
            password=_require_env("DB_PASSWORD"),
        )
