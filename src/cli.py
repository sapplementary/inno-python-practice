import argparse
import sys
from pathlib import Path

import psycopg2

from src.app import Application
from src.config import DbConfig
from src.db.connection import DataBaseConnection
from src.exporters.factory import ExporterFactory
from src.loaders.json_loader import JsonLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Загружает студентов и комнаты в PostgreSQL и выгружает результаты запросов."
    )
    parser.add_argument(
        "--students",
        default=str(DATA_DIR / "students.json"),
        help="путь к файлу со студентами (по умолчанию: %(default)s)",
    )
    parser.add_argument(
        "--rooms",
        default=str(DATA_DIR / "rooms.json"),
        help="путь к файлу с комнатами (по умолчанию: %(default)s)",
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=["json", "xml"],
        help="формат результата",
    )
    parser.add_argument(
        "--output",
        help="файл для результата (по умолчанию: output/result.<формат>)",
    )
    return parser


def resolve_output_path(output: str | None, fmt: str) -> Path:
    if output:
        return Path(output)
    return OUTPUT_DIR / f"result.{fmt}"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        app = Application(
            db=DataBaseConnection(DbConfig.from_env()),
            loader=JsonLoader(),
            exporter=ExporterFactory.create(args.format),
        )
        result = app.run(rooms_path=args.rooms, students_path=args.students)

        output_path = resolve_output_path(args.output, args.format)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
    except (RuntimeError, ValueError, OSError, psycopg2.Error) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    print(f"Результат записан в {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())