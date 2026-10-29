import argparse
import sys
from pathlib import Path

import psycopg2

from src.app import Application
from src.config import DbConfig
from src.db.connection import DataBaseConnection
from src.exporters.factory import ExporterFactory
from src.loaders.json_loader import JsonLoader


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Загружает студентов и комнаты в PostgreSQL и выгружает результаты запросов."
    )
    parser.add_argument("--students", required=True, help="путь к файлу со студентами")
    parser.add_argument("--rooms", required=True, help="путь к файлу с комнатами")
    parser.add_argument("--format", required=True, choices=["json", "xml"],
                        help="формат результата")
    parser.add_argument("--output", help="файл для результата (по умолчанию вывод в консоль)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        app = Application(
            db=DataBaseConnection(DbConfig.from_env()),
            loader=JsonLoader(),
            exporter=ExporterFactory.create(args.format),
        )
        result = app.run(rooms_path=args.rooms, students_path=args.students)
    except (RuntimeError, ValueError, OSError, psycopg2.Error) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
