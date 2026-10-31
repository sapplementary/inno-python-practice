import pytest

from src.config import DbConfig

VARS = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]


def test_missing_env_raises_clear_error(monkeypatch):
    for name in VARS:
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(RuntimeError, match="DB_HOST"):
        DbConfig.from_env()


def test_empty_value_is_treated_as_missing(monkeypatch):
    values = {
        "DB_HOST": "h", "DB_PORT": "5432", "DB_NAME": "n",
        "DB_USER": "u", "DB_PASSWORD": "",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)

    with pytest.raises(RuntimeError, match="DB_PASSWORD"):
        DbConfig.from_env()


def test_config_reads_all_values(monkeypatch):
    values = {
        "DB_HOST": "h", "DB_PORT": "5433", "DB_NAME": "n",
        "DB_USER": "u", "DB_PASSWORD": "p",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)

    config = DbConfig.from_env()

    assert config.host == "h"
    assert config.port == 5433
    assert config.user == "u"
