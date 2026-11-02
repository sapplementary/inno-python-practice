"""Соединение с PostgreSQL в виде менеджера контекста.

Модуль отвечает только за жизненный цикл соединения: открыть его, зафиксировать
или откатить транзакцию и закрыть. SQL-запросы приложения здесь не хранятся.
"""
import logging
from contextlib import contextmanager
from typing import Any, Iterator, Optional, Sequence

import psycopg2
from psycopg2.extras import RealDictCursor

from src.config import DbConfig

logger = logging.getLogger(__name__)


class DataBaseConnection:
    """Соединение с БД, управляемое оператором ``with``.

    При входе в блок соединение открывается. При нормальном выходе транзакция
    фиксируется (commit), при исключении откатывается (rollback), а соединение
    закрывается в любом случае. Методы выборки и выполнения скриптов работают
    только внутри блока ``with``.

    Example:
        with DataBaseConnection(config) as db:
            rows = db.fetch_all("SELECT 1 AS x")
    """

    def __init__(self, config: DbConfig) -> None:
        """Запоминает настройки. Само соединение пока не открывается.

        Args:
            config: Параметры подключения.
        """
        self._config = config
        self._conn = None

    def __enter__(self) -> "DataBaseConnection":
        """Открывает соединение с БД.

        Returns:
            Этот же объект, чтобы его можно было получить через ``as``.
        """
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

    def __exit__(self, exc_type, exc_value, tb) -> bool:
        """Завершает транзакцию и закрывает соединение.

        Args:
            exc_type: Тип исключения или None, если блок завершился без ошибок.
            exc_value: Экземпляр исключения или None.
            tb: Трейсбэк исключения или None.

        Returns:
            Всегда False: исключение не подавляется и передаётся дальше.
        """
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
        """Выдаёт курсор, возвращающий строки в виде словарей.

        Курсор закрывается автоматически при выходе из блока ``with``.

        Yields:
            Курсор ``RealDictCursor``.

        Raises:
            RuntimeError: Если соединение не открыто.
        """
        cur = self._require_connection().cursor(cursor_factory=RealDictCursor)
        try:
            yield cur
        finally:
            cur.close()

    def execute_script(self, path: str) -> None:
        """Выполняет SQL-скрипт из файла целиком.

        Args:
            path: Путь к ``.sql`` файлу.

        Raises:
            RuntimeError: Если соединение не открыто.
            OSError: Если файл не удалось прочитать.
        """
        with open(path, encoding="utf-8") as f:
            sql = f.read()
        with self.cursor() as cur:
            cur.execute(sql)

    def fetch_all(self, sql: str, params: Optional[Sequence[Any]] = None) -> list[dict]:
        """Выполняет запрос и возвращает все строки результата.

        Значения передаются отдельно от текста запроса (плейсхолдеры ``%s``),
        что защищает от SQL-инъекций.

        Args:
            sql: Текст запроса.
            params: Значения для плейсхолдеров или None.

        Returns:
            Список словарей вида ``{название колонки: значение}``.

        Raises:
            RuntimeError: Если соединение не открыто.
        """
        with self.cursor() as cur:
            cur.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]

    def _require_connection(self):
        """Возвращает открытое соединение или сообщает о неправильном использовании.

        Returns:
            Объект соединения psycopg2.

        Raises:
            RuntimeError: Если вызов произошёл вне блока ``with``.
        """
        if self._conn is None:
            raise RuntimeError(
                "Соединение не открыто: используйте 'with DataBaseConnection(...) as db'"
            )
        return self._conn
