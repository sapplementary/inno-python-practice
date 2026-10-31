import logging
from typing import Iterable

from psycopg2.extras import execute_values

from src.db.connection import DataBaseConnection
from src.models import Room, Student

logger = logging.getLogger(__name__)

class RoomRepository:
    def __init__(self, db: DataBaseConnection) -> None:
        self._db = db

    def insert_many(self, rooms: Iterable[Room]) -> None:
        rows = [(room.id, room.name) for room in rooms]
        sql = """
            INSERT INTO rooms (id, name)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
        """
        with self._db.cursor() as cur:
            execute_values(cur, sql, rows)
            logger.info("Загружено комнат: %d", len(rows))
            logger.info("Загружено студентов: %d", len(rows))


class StudentRepository:
    def __init__(self, db: DataBaseConnection) -> None:
        self._db = db

    def insert_many(self, students: Iterable[Student]) -> None:
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
            execute_values(cur, sql, rows)
            logger.info("Загружено комнат: %d", len(rows))
            logger.info("Загружено студентов: %d", len(rows))
