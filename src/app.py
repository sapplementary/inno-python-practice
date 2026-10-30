from pathlib import Path

from src.db.connection import DataBaseConnection
from src.db.repository import RoomRepository, StudentRepository
from src.exporters.base import Exporter
from src.loaders.base import DataLoader
from src.queries import QueryService

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
        with self._db as db:
            db.execute_script(str(self._sql_dir / "schema.sql"))
            RoomRepository(db).insert_many(self._loader.load_rooms(rooms_path))
            StudentRepository(db).insert_many(self._loader.load_students(students_path))
            db.execute_script(str(self._sql_dir / "indexes.sql"))
            data = QueryService(db).run_all()
        return self._exporter.export(data)
