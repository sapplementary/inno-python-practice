from unittest.mock import MagicMock

import pytest

from src.queries import QueryService

FILES = [
    ("01_rooms_students_count.sql", "SQL-1"),
    ("02_lowest_avg_age.sql", "SQL-2"),
    ("03_largest_age_diff.sql", "SQL-3"),
    ("04_mixed_sex_rooms.sql", "SQL-4"),
]


def make_queries_dir(tmp_path):
    for name, text in FILES:
        (tmp_path / name).write_text(text, encoding="utf-8")
    return tmp_path


def test_run_all_reads_files_and_returns_four_results(tmp_path):
    db = MagicMock()
    db.fetch_all.return_value = [{"x": 1}]
    service = QueryService(db, queries_dir=make_queries_dir(tmp_path))

    result = service.run_all()

    assert list(result) == [
        "rooms_students_count",
        "lowest_avg_age_rooms",
        "largest_age_diff_rooms",
        "mixed_sex_rooms",
    ]
    assert all(rows == [{"x": 1}] for rows in result.values())
    executed = [call.args[0] for call in db.fetch_all.call_args_list]
    assert executed == ["SQL-1", "SQL-2", "SQL-3", "SQL-4"]


def test_missing_query_file_raises(tmp_path):
    service = QueryService(MagicMock(), queries_dir=tmp_path)
    with pytest.raises(FileNotFoundError):
        service.rooms_students_count()
