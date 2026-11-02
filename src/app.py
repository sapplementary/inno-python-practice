"""Сценарий работы приложения

Связывает остальные части в одну последовательность: схема, загрузка данных,
индексы, запросы, экспорт. Конкретные загрузчик и экспортёр передаются снаружи,
поэтому класс не зависит от форматов файлов
"""
import logging
from pathlib import Path

from src.db.connection import DataBaseConnection
from src.db.repository import RoomRepository, StudentRepository
from src.exporters.base import Exporter
from src.loaders.base import DataLoader
from src.queries import QueryService

logger = logging.getLogger(__name__)

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


class Application:
    """Выполняет полный сценарий: загрузка данных, запросы и экспорт результата."""

    def __init__(
        self,
        db: DataBaseConnection,
        loader: DataLoader,
        exporter: Exporter,
        sql_dir: Path = SQL_DIR,
    ) -> None:
        """Принимает зависимости, с которыми будет работать приложение.

        Args:
            db: Соединение с БД (ещё не открытое).
            loader: Загрузчик входных файлов.
            exporter: Экспортёр результата в нужный формат.
            sql_dir: Папка со скриптами ``schema.sql`` и ``indexes.sql``.
        """
        self._db = db
        self._loader = loader
        self._exporter = exporter
        self._sql_dir = sql_dir

    def run(self, rooms_path: str, students_path: str) -> str:
        """Загружает данные в БД, выполняет запросы и возвращает результат

        Все шаги работают в одной транзакции: если любой из них завершится
        ошибкой, изменения в БД откатываются. Порядок важен: сначала комнаты,
        затем студенты (внешний ключ), индексы создаются после загрузки

        Args:
            rooms_path: Путь к файлу с комнатами.
            students_path: Путь к файлу со студентами.

        Returns:
            Результат запросов в виде строки в формате экспортёра.
        """
        logger.info("Входные файлы: комнаты %s, студенты %s", rooms_path, students_path)
        with self._db as db:
            logger.info("Создание схемы БД")
            db.execute_script(str(self._sql_dir / "schema.sql"))

            logger.info("Загрузка комнат и студентов")
            RoomRepository(db).insert_many(self._loader.load_rooms(rooms_path))
            StudentRepository(db).insert_many(self._loader.load_students(students_path))

            logger.info("Создание индексов")
            db.execute_script(str(self._sql_dir / "indexes.sql"))

            logger.info("Выполнение запросов")
            data = QueryService(db).run_all()

        logger.info("Экспорт результата")
        return self._exporter.export(data)