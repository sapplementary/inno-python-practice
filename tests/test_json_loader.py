import json
from datetime import date

from src.loaders.json_loader import JsonLoader


def test_load_rooms(tmp_path):
    path = tmp_path / "rooms.json"
    path.write_text(json.dumps([{"id": 7, "name": "Room #7"}]), encoding="utf-8")

    rooms = list(JsonLoader().load_rooms(str(path)))

    assert len(rooms) == 1
    assert rooms[0].id == 7
    assert rooms[0].name == "Room #7"


def test_load_students_maps_fields(tmp_path):
    path = tmp_path / "students.json"
    path.write_text(
        json.dumps([{
            "id": 1,
            "name": "Peggy Ryan",
            "birthday": "2011-08-22T00:00:00.000000",
            "sex": "M",
            "room": 473,
        }]),
        encoding="utf-8",
    )

    students = list(JsonLoader().load_students(str(path)))

    assert students[0].birthday == date(2011, 8, 22)
    assert students[0].room_id == 473
    assert students[0].sex == "M"
