"""Загрузчик входных данных из JSON-файлов.

Файл должен содержать список объектов. Для комнат это поля ``id`` и ``name``,
для студентов ``id``, ``name``, ``birthday`` (строка в формате ISO), ``sex``
и ``room`` (номер комнаты). Файл читается в память целиком, а объекты моделей
создаются по одному.
"""
import json
from datetime import datetime
from typing import Iterable

from src.loaders.base import DataLoader
from src.models import Room, Student


class JsonLoader(DataLoader):
    """Читает комнаты и студентов из JSON-файлов."""

    def load_rooms(self, path: str) -> Iterable[Room]:
        """Читает комнаты из JSON-файла.

        Метод является генератором: файл открывается, когда по результату
        начинают итерацию, а не в момент вызова.

        Args:
            path: Путь к JSON-файлу с комнатами.

        Yields:
            Объекты ``Room``.

        Raises:
            OSError: Если файл не удалось открыть.
            ValueError: Если файл не является корректным JSON.
            KeyError: Если в записи нет обязательного поля.
        """
        for item in self._read(path):
            yield Room(id=item["id"], name=item["name"])

    def load_students(self, path: str) -> Iterable[Student]:
        """Читает студентов из JSON-файла.

        Дата рождения превращается в ``date`` (время отбрасывается),
        поле ``room`` сохраняется как ``room_id``.

        Args:
            path: Путь к JSON-файлу со студентами.

        Yields:
            Объекты ``Student``.

        Raises:
            OSError: Если файл не удалось открыть.
            ValueError: Если файл не является корректным JSON
                или дата рождения записана в неверном формате.
            KeyError: Если в записи нет обязательного поля.
        """
        for item in self._read(path):
            yield Student(
                id=item["id"],
                name=item["name"],
                birthday=datetime.fromisoformat(item["birthday"]).date(),
                sex=item["sex"],
                room_id=item["room"],
            )

    @staticmethod
    def _read(path: str) -> list[dict]:
        """Читает JSON-файл целиком.

        Args:
            path: Путь к файлу.

        Returns:
            Список записей из файла.
        """
        with open(path, encoding="utf-8") as f:
            return json.load(f)
