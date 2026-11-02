"""Точка входа: командная строка приложения.

Запуск из корня проекта: ``python3 -m src.cli --format json``.
Здесь разбираются параметры, создаются конкретные объекты (соединение,
загрузчик, экспортёр) и передаются в ``Application``. Код возврата:
0 при успехе, 1 при известной ошибке, 2 при неверных параметрах.
"""
import argparse
import logging
import sys
from pathlib import Path

import psycopg2

from src.app import Application
from src.config import DbConfig
from src.db.connection import DataBaseConnection
from src.exporters.factory import ExporterFactory
from src.loaders.json_loader import JsonLoader
from src.logging_config import setup_logging

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"


def build_parser() -> argparse.ArgumentParser:
    """Создаёт разборщик параметров командной строки.

    Returns:
        Разборщик с параметрами ``--format`` (обязательный), ``--rooms``,
        ``--students``, ``--output`` и ``--log-level``.
    """
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
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="уровень логирования (по умолчанию: %(default)s)",
    )
    return parser


def resolve_output_path(output: str | None, fmt: str) -> Path:
    """Определяет, куда записать результат.

    Args:
        output: Путь, заданный пользователем, или None.
        fmt: Формат результата (``json`` или ``xml``).

    Returns:
        Путь пользователя, если он задан, иначе ``output/result.<формат>``.
    """
    if output:
        return Path(output)
    return OUTPUT_DIR / f"result.{fmt}"


def main(argv: list[str] | None = None) -> int:
    """Запускает приложение.

    Известные ошибки (нет переменной окружения, нет файла, неверный формат,
    ошибка БД) логируются одной строкой и не показываются трейсбэком,
    кроме режима ``--log-level DEBUG``. При неверных параметрах argparse
    сам завершает программу с кодом 2.

    Args:
        argv: Список параметров; если None, берутся параметры командной строки.

    Returns:
        Код возврата: 0 при успехе, 1 при ошибке.
    """
    args = build_parser().parse_args(argv)
    setup_logging(args.log_level)
    logger.info("Запуск: формат результата %s", args.format)
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
        logger.error("Ошибка: %s", e, exc_info=args.log_level == "DEBUG")
        return 1

    logger.info("Результат записан в %s", output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
