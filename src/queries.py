"""Выполнение четырёх SQL-запросов по заданию.

Тексты запросов лежат в файлах ``sql/queries/``, а здесь они читаются
и выполняются. Все вычисления (подсчёт студентов, средний возраст, разница
в возрасте, поиск комнат с разным полом) делаются на стороне БД, Python
получает готовые строки. Возраст считается в целых годах относительно
даты запуска.
"""
import logging
import time
from pathlib import Path

from src.db.connection import DataBaseConnection

logger = logging.getLogger(__name__)

QUERIES_DIR = Path(__file__).resolve().parent.parent / "sql" / "queries"


class QueryService:
    """Выполняет запросы из папки ``sql/queries/`` и возвращает списки словарей.

    Названия полей в результате совпадают с названиями колонок в SQL-файлах.
    """

    def __init__(self, db: DataBaseConnection, queries_dir: Path = QUERIES_DIR) -> None:
        """Запоминает соединение и папку с запросами.

        Args:
            db: Соединение с БД (внутри блока ``with``).
            queries_dir: Папка с ``.sql`` файлами запросов.
        """
        self._db = db
        self._queries_dir = queries_dir

    def rooms_students_count(self) -> list[dict]:
        """Запрос 1: комнаты и количество студентов в каждой.

        Пустые комнаты тоже попадают в результат, с нулём студентов.

        Returns:
            Строки с полями ``id``, ``name``, ``count_students``.
        """
        return self._run("01_rooms_students_count.sql")

    def lowest_avg_age_rooms(self) -> list[dict]:
        """Запрос 2: пять комнат с наименьшим средним возрастом студентов.

        Сортировка идёт по точному среднему, при равенстве по номеру комнаты.

        Returns:
            Пять строк с полями ``id``, ``name``, ``avg_age_years``.
        """
        return self._run("02_lowest_avg_age.sql")

    def largest_age_diff_rooms(self) -> list[dict]:
        """Запрос 3: пять комнат с наибольшей разницей в возрасте студентов.

        Разница это максимальный возраст минус минимальный в целых годах.
        При равной разнице выше стоит комната с большим разрывом между датами
        рождения (в днях), при равенстве и этого меньший номер комнаты.

        Returns:
            Пять строк с полями ``id``, ``name``, ``age_diff_years``.
        """
        return self._run("03_largest_age_diff.sql")

    def mixed_sex_rooms(self) -> list[dict]:
        """Запрос 4: комнаты, в которых живут студенты разного пола.

        Returns:
            Строки с полями ``id`` и ``name``.
        """
        return self._run("04_mixed_sex_rooms.sql")

    def run_all(self) -> dict[str, list[dict]]:
        """Выполняет все четыре запроса.

        Returns:
            Словарь «название запроса: строки результата». Порядок ключей
            соответствует порядку запросов в задании.
        """
        return {
            "rooms_students_count": self.rooms_students_count(),
            "lowest_avg_age_rooms": self.lowest_avg_age_rooms(),
            "largest_age_diff_rooms": self.largest_age_diff_rooms(),
            "mixed_sex_rooms": self.mixed_sex_rooms(),
        }

    def _run(self, filename: str) -> list[dict]:
        """Читает SQL-файл, выполняет запрос и записывает в лог время выполнения.

        Args:
            filename: Имя файла в папке запросов.

        Returns:
            Строки результата в виде словарей.

        Raises:
            FileNotFoundError: Если файла запроса нет.
        """
        sql = (self._queries_dir / filename).read_text(encoding="utf-8")
        start = time.perf_counter()
        rows = self._db.fetch_all(sql)
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("Запрос %s: %d строк за %.1f мс", filename, len(rows), elapsed_ms)
        return rows
