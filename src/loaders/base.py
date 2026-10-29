from abc import ABC, abstractmethod
from typing import Iterable

from src.models import Room, Student


class DataLoader(ABC):
    @abstractmethod
    def load_rooms(self, path: str) -> Iterable[Room]: ...

    @abstractmethod
    def load_students(self, path: str) -> Iterable[Student]: ...

