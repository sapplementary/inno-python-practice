import json
from datetime import datetime
from typing import Iterable

from src.loaders.base import DataLoader
from src.models import Room, Student


class JsonLoader(DataLoader):
    def load_rooms(self, path: str) -> Iterable[Room]:
        for item in self._read(path):
            yield Room(id=item["id"], name=item["name"])

    def load_students(self, path: str) -> Iterable[Student]:
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
        with open(path, encoding="utf-8") as f:
            return json.load(f)
