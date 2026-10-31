from unittest.mock import MagicMock

import pytest

from src.config import DbConfig
from src.db.connection import DataBaseConnection

CONFIG = DbConfig(host="h", port=5432, dbname="n", user="u", password="p")


@pytest.fixture
def fake_conn(monkeypatch):
    conn = MagicMock()
    monkeypatch.setattr("src.db.connection.psycopg2.connect", MagicMock(return_value=conn))
    return conn


def test_fetch_all_outside_with_raises_clear_error():
    db = DataBaseConnection(CONFIG)
    with pytest.raises(RuntimeError, match="Соединение не открыто"):
        db.fetch_all("SELECT 1")


def test_cursor_outside_with_raises_clear_error():
    db = DataBaseConnection(CONFIG)
    with pytest.raises(RuntimeError, match="Соединение не открыто"):
        with db.cursor():
            pass


def test_commit_and_close_on_success(fake_conn):
    db = DataBaseConnection(CONFIG)
    with db:
        pass

    fake_conn.commit.assert_called_once()
    fake_conn.rollback.assert_not_called()
    fake_conn.close.assert_called_once()
    assert db._conn is None


def test_rollback_and_close_on_error(fake_conn):
    db = DataBaseConnection(CONFIG)
    with pytest.raises(ValueError):
        with db:
            raise ValueError("boom")

    fake_conn.rollback.assert_called_once()
    fake_conn.commit.assert_not_called()
    fake_conn.close.assert_called_once()


def test_fetch_all_returns_dicts_and_closes_cursor(fake_conn):
    cur = fake_conn.cursor.return_value
    cur.fetchall.return_value = [{"n": 5}]

    with DataBaseConnection(CONFIG) as db:
        rows = db.fetch_all("SELECT 1 AS n")

    assert rows == [{"n": 5}]
    cur.execute.assert_called_once_with("SELECT 1 AS n", None)
    cur.close.assert_called_once()
