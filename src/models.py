"""Модели данных: комната и студент.

Модели только хранят данные и не содержат логики. Они ничего не знают
о файлах и о базе данных, поэтому их используют и загрузчики, и репозитории.
"""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Room:
    """Комната.

    Attributes:
        id: Уникальный номер комнаты.
        name: Название комнаты, например ``Room #0``.
    """

    id: int
    name: str


@dataclass(frozen=True)
class Student:
    """Студент, живущий в одной из комнат.

    Attributes:
        id: Уникальный номер студента.
        name: Имя студента.
        birthday: Дата рождения.
        sex: Пол: ``M`` или ``F``.
        room_id: Номер комнаты, в которой живёт студент
            (во входном файле это поле называется ``room``).
    """

    id: int
    name: str
    birthday: date
    sex: str
    room_id: int
