import logging
from contextlib import contextmanager
from typing import Any, Iterator, Optional, Sequence

import psycopg2
from psycopg2.extras import RealDictCursor

from src.config import DbConfig

logger = logging.getLogger(__name__)

class DataBaseConnection:
    def __init__(self, config: DbConfig) -> None:
        self._config = config
        self._conn = None

    def __enter__(self) -> "DataBaseConnection":
        logger.debug(
            "Подключение к БД %s:%s/%s",
            self._config.host, self._config.port, self._config.dbname,
        )
        self._conn = psycopg2.connect(
            host=self._config.host,
            port=self._config.port,
            dbname=self._config.dbname,
            user=self._config.user,
            password=self._config.password,
        )
        logger.info("Соединение с БД установлено")
        return self
    
    def __exit__(self, exc_type, exc, tb) -> bool:
        try:
            if exc_type is None:
                self._conn.commit()
                logger.info("Транзакция зафиксирована (commit)")
            else:
                self._conn.rollback()
                logger.warning("Транзакция откатена (rollback)")
        finally:
            self._conn.close()
            self._conn = None
            logger.debug("Соединение закрыто")
        return False

    @contextmanager
    def cursor(self) -> Iterator[RealDictCursor]:
        cur = self._require_connection().cursor(cursor_factory=RealDictCursor)
        try:
            yield cur
        finally:
            cur.close()

    def execute_script(self, path: str) -> None:
        with open(path, encoding="utf-8") as f:
            sql = f.read()
        with self.cursor() as cur:
            cur.execute(sql)

    def fetch_all(self, sql: str, params: Optional[Sequence[Any]] = None) -> list[dict]:
        with self.cursor() as cur:
            cur.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]

    def _require_connection(self):
        if self._conn is None:
            raise RuntimeError(
                "Соединение не открыто: используйте 'with DataBaseConnection(...) as db'"
            )
        return self._conn
