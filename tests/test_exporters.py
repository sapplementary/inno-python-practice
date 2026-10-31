import json
import xml.etree.ElementTree as ET

import pytest

from src.exporters.factory import ExporterFactory

DATA = {
    "rooms_students_count": [
        {"id": 0, "name": "Room #0", "count_students": 2},
        {"id": 1, "name": "Room #1", "count_students": 0},
    ],
    "lowest_avg_age_rooms": [
        {"id": 0, "name": "Room #0", "avg_age_years": 12.5},
    ],
}


def test_json_export_can_be_parsed_back():
    text = ExporterFactory.create("json").export(DATA)
    assert json.loads(text) == DATA


def test_xml_export_structure():
    text = ExporterFactory.create("xml").export(DATA)
    root = ET.fromstring(text)
    rows = root.find("rooms_students_count").findall("row")
    assert len(rows) == 2
    assert rows[0].find("name").text == "Room #0"
    assert rows[0].find("count_students").text == "2"


def test_factory_is_case_insensitive():
    assert type(ExporterFactory.create("JSON")) is type(ExporterFactory.create("json"))


def test_factory_rejects_unknown_format():
    with pytest.raises(ValueError, match="csv"):
        ExporterFactory.create("csv")
