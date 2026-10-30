from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Room:
    id: int
    name: str


@dataclass(frozen=True)
class Student:
    id: int
    name: str
    birthday: date
    sex: str
    room_id: int

