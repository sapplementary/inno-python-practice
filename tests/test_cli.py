import logging
from pathlib import Path

import pytest

from src.cli import OUTPUT_DIR, build_parser, main, resolve_output_path


@pytest.fixture(autouse=True)
def reset_logging():
    yield
    logging.getLogger().handlers.clear()


def test_explicit_output_path_wins():
    assert resolve_output_path("custom/out.json", "json") == Path("custom/out.json")


@pytest.mark.parametrize("fmt", ["json", "xml"])
def test_default_output_path_depends_on_format(fmt):
    assert resolve_output_path(None, fmt) == OUTPUT_DIR / f"result.{fmt}"


def test_format_is_required():
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args([])
    assert exc.value.code == 2


def test_unknown_format_is_rejected():
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["--format", "csv"])
    assert exc.value.code == 2


def test_defaults_for_paths_and_log_level():
    args = build_parser().parse_args(["--format", "json"])

    assert Path(args.rooms).name == "rooms.json"
    assert Path(args.rooms).parent.name == "data"
    assert Path(args.students).name == "students.json"
    assert args.output is None
    assert args.log_level == "INFO"


def test_main_returns_1_when_env_is_missing(monkeypatch):
    for name in ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]:
        monkeypatch.delenv(name, raising=False)

    assert main(["--format", "json"]) == 1
