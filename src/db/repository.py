"""Репозитории: запись комнат и студентов в базу данных.

Каждый репозиторий отвечает за SQL одной таблицы. Соединение передаётся снаружи,
а commit или rollback выполняет код, открывший это соединение. Поэтому загрузка
нескольких таблиц проходит в одной транзакции.
"""
import logging
from typing import Iterable

from psycopg2.extras import execute_values

from src.db.connection import DataBaseConnection
from src.models import Room, Student

logger = logging.getLogger(__name__)


class RoomRepository:
    """Записывает комнаты в таблицу ``rooms``."""

    def __init__(self, db: DataBaseConnection) -> None:
        """Запоминает открытое соединение.

        Args:
            db: Соединение с БД (внутри блока ``with``).
        """
        self._db = db

    def insert_many(self, rooms: Iterable[Room]) -> None:
        """Вставляет комнаты пачками.

        Если комната с таким ``id`` уже есть, её название обновляется
        (``ON CONFLICT DO UPDATE``), поэтому метод можно вызывать повторно.

        Args:
            rooms: Комнаты; подойдёт и список, и генератор.
        """
        rows = [(room.id, room.name) for room in rooms]
        sql = """
            INSERT INTO rooms (id, name)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
        """
        with self._db.cursor() as cur:
            execute_values(cur, sql, rows, page_size=1000)
        logger.info("Загружено комнат: %d", len(rows))


class StudentRepository:
    """Записывает студентов в таблицу ``students``."""

    def __init__(self, db: DataBaseConnection) -> None:
        """Запоминает открытое соединение.

        Args:
            db: Соединение с БД (внутри блока ``with``).
        """
        self._db = db

    def insert_many(self, students: Iterable[Student]) -> None:
        """Вставляет студентов пачками.

        Если студент с таким ``id`` уже есть, его данные обновляются. Комнаты
        студентов должны быть загружены заранее: иначе внешний ключ
        ``room_id`` не позволит выполнить вставку.

        Args:
            students: Студенты; подойдёт и список, и генератор.
        """
        rows = [
            (s.id, s.name, s.birthday, s.sex, s.room_id)
            for s in students
        ]
        sql = """
            INSERT INTO students (id, name, birthday, sex, room_id)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                birthday = EXCLUDED.birthday,
                sex = EXCLUDED.sex,
                room_id = EXCLUDED.room_id
        """
        with self._db.cursor() as cur:
            execute_values(cur, sql, rows, page_size=1000)
        logger.info("Загружено студентов: %d", len(rows))
