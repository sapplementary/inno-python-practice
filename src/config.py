"""Настройки подключения к базе данных.

Параметры читаются из переменных окружения. Значений по умолчанию нет:
если переменная не задана, программа останавливается с понятной ошибкой.
Так в код и в репозиторий не попадают логины и пароли, а забытая
настройка не приводит к тихому подключению «не туда».
"""
import os
from dataclasses import dataclass


def _require_env(name: str) -> str:
    """Возвращает значение переменной окружения или останавливает программу.

    Args:
        name: Имя переменной окружения.

    Returns:
        Непустое значение переменной.

    Raises:
        RuntimeError: Если переменная не задана или пуста.
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Не задана переменная окружения {name}")
    return value


def _require_int_env(name: str) -> int:
    """Возвращает значение переменной окружения, приведённое к целому числу.

    Args:
        name: Имя переменной окружения.

    Returns:
        Значение переменной как целое число.

    Raises:
        RuntimeError: Если переменная не задана, пуста или не является числом.
    """
    value = _require_env(name)
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(
            f"Переменная окружения {name} должна быть целым числом, получено: {value!r}"
        ) from None


@dataclass(frozen=True)
class DbConfig:
    """Неизменяемый набор параметров подключения к PostgreSQL.

    Attributes:
        host: Адрес сервера БД.
        port: Порт сервера БД.
        dbname: Имя базы данных.
        user: Имя пользователя.
        password: Пароль пользователя.
    """

    host: str
    port: int
    dbname: str
    user: str
    password: str

    @classmethod
    def from_env(cls) -> "DbConfig":
        """Создаёт конфигурацию из переменных окружения.

        Используются DB_HOST, DB_PORT, DB_NAME, DB_USER и DB_PASSWORD.

        Returns:
            Заполненный объект конфигурации.

        Raises:
            RuntimeError: Если какая-либо переменная отсутствует или некорректна.
        """
        return cls(
            host=_require_env("DB_HOST"),
            port=_require_int_env("DB_PORT"),
            dbname=_require_env("DB_NAME"),
            user=_require_env("DB_USER"),
            password=_require_env("DB_PASSWORD"),
        )
