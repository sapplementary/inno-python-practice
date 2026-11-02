"""Контракт загрузчиков входных данных.

Определяет абстрактный класс ``DataLoader``. Остальной код зависит только от него,
поэтому новый формат входных файлов добавляется новым подклассом, а приложение
менять не нужно.
"""
from abc import ABC, abstractmethod
from typing import Iterable

from src.models import Room, Student


class DataLoader(ABC):
    """Абстрактный загрузчик данных о комнатах и студентах."""

    @abstractmethod
    def load_rooms(self, path: str) -> Iterable[Room]:
        """Читает файл с комнатами.

        Args:
            path: Путь к файлу.

        Returns:
            Комнаты в виде объектов ``Room``.
        """

    @abstractmethod
    def load_students(self, path: str) -> Iterable[Student]:
        """Читает файл со студентами.

        Args:
            path: Путь к файлу.

        Returns:
            Студенты в виде объектов ``Student``.
        """
