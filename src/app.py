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
    def __init__(
        self,
        db: DataBaseConnection,
        loader: DataLoader,
        exporter: Exporter,
        sql_dir: Path = SQL_DIR,
    ) -> None:
        self._db = db
        self._loader = loader
        self._exporter = exporter
        self._sql_dir = sql_dir

    def run(self, rooms_path: str, students_path: str) -> str:
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

