from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.app import Application


def make_app(monkeypatch, fail_on_students=False):
    calls = []

    db = MagicMock()
    db.__enter__.return_value = db
    db.__exit__.return_value = False
    db.execute_script.side_effect = lambda path: calls.append(("script", Path(path).name))

    class FakeRoomRepository:
        def __init__(self, db):
            pass

        def insert_many(self, rooms):
            calls.append(("rooms", list(rooms)))

    class FakeStudentRepository:
        def __init__(self, db):
            pass

        def insert_many(self, students):
            if fail_on_students:
                raise ValueError("boom")
            calls.append(("students", list(students)))

    class FakeQueryService:
        def __init__(self, db):
            pass

        def run_all(self):
            calls.append(("queries",))
            return {"q": []}

    monkeypatch.setattr("src.app.RoomRepository", FakeRoomRepository)
    monkeypatch.setattr("src.app.StudentRepository", FakeStudentRepository)
    monkeypatch.setattr("src.app.QueryService", FakeQueryService)

    loader = MagicMock()
    loader.load_rooms.return_value = ["room"]
    loader.load_students.return_value = ["student"]
    exporter = MagicMock()
    exporter.export.return_value = "RESULT"

    app = Application(db, loader, exporter, sql_dir=Path("sql"))
    return app, db, loader, exporter, calls


def test_run_executes_steps_in_order(monkeypatch):
    app, db, loader, exporter, calls = make_app(monkeypatch)

    result = app.run("rooms.json", "students.json")

    assert result == "RESULT"
    assert calls == [
        ("script", "schema.sql"),
        ("rooms", ["room"]),
        ("students", ["student"]),
        ("script", "indexes.sql"),
        ("queries",),
    ]
    loader.load_rooms.assert_called_once_with("rooms.json")
    loader.load_students.assert_called_once_with("students.json")
    exporter.export.assert_called_once_with({"q": []})


def test_error_during_load_stops_run_and_skips_export(monkeypatch):
    app, db, loader, exporter, calls = make_app(monkeypatch, fail_on_students=True)

    with pytest.raises(ValueError, match="boom"):
        app.run("rooms.json", "students.json")

    assert calls == [("script", "schema.sql"), ("rooms", ["room"])]
    assert db.__exit__.call_args.args[0] is ValueError
    exporter.export.assert_not_called()
