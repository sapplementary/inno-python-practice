from pathlib import Path

from src.db.connection import DataBaseConnection

QUERIES_DIR = Path(__file__).resolve().parent.parent / "sql" / "queries"


class QueryService:
    def __init__(self, db: DataBaseConnection, queries_dir: Path = QUERIES_DIR) -> None:
        self._db = db
        self._queries_dir = queries_dir

    def rooms_students_count(self) -> list[dict]:
        return self._run("01_rooms_students_count.sql")

    def lowest_avg_age_rooms(self) -> list[dict]:
        return self._run("02_lowest_avg_age.sql")

    def largest_age_diff_rooms(self) -> list[dict]:
        return self._run("03_largest_age_diff.sql")

    def mixed_sex_rooms(self) -> list[dict]:
        return self._run("04_mixed_sex_rooms.sql")

    def run_all(self) -> dict[str, list[dict]]:
        return {
            "rooms_students_count": self.rooms_students_count(),
            "lowest_avg_age_rooms": self.lowest_avg_age_rooms(),
            "largest_age_diff_rooms": self.largest_age_diff_rooms(),
            "mixed_sex_rooms": self.mixed_sex_rooms(),
        }

    def _run(self, filename: str) -> list[dict]:
        sql = (self._queries_dir / filename).read_text(encoding="utf-8")
        return self._db.fetch_all(sql)

