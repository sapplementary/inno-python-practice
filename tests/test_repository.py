from datetime import date
from unittest.mock import MagicMock

import pytest

from src.db.repository import RoomRepository, StudentRepository
from src.models import Room, Student


@pytest.fixture
def db_and_cursor():
    db = MagicMock()
    cur = MagicMock()
    db.cursor.return_value.__enter__.return_value = cur
    return db, cur


@pytest.fixture
def execute_values_mock(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("src.db.repository.execute_values", mock)
    return mock


def test_room_insert_many_builds_rows_and_upsert(db_and_cursor, execute_values_mock):
    db, cur = db_and_cursor

    RoomRepository(db).insert_many([Room(0, "Room #0"), Room(1, "Room #1")])

    used_cur, sql, rows = execute_values_mock.call_args.args
    assert used_cur is cur
    assert "INSERT INTO rooms" in sql
    assert "ON CONFLICT (id)" in sql
    assert rows == [(0, "Room #0"), (1, "Room #1")]


def test_student_insert_many_builds_rows_and_upsert(db_and_cursor, execute_values_mock):
    db, _ = db_and_cursor
    student = Student(1, "Peggy Ryan", date(2011, 8, 22), "M", 473)

    StudentRepository(db).insert_many([student])

    _, sql, rows = execute_values_mock.call_args.args
    assert "INSERT INTO students" in sql
    assert "ON CONFLICT (id)" in sql
    assert rows == [(1, "Peggy Ryan", date(2011, 8, 22), "M", 473)]


def test_insert_many_accepts_generator(db_and_cursor, execute_values_mock):
    db, _ = db_and_cursor
    rooms = (Room(i, f"Room #{i}") for i in range(3))

    RoomRepository(db).insert_many(rooms)

    rows = execute_values_mock.call_args.args[2]
    assert len(rows) == 3
