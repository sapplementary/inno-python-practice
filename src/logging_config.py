"""Настройка логирования приложения.

Логирование настраивается один раз, в точке входа. Остальные модули только
получают свой логгер через ``logging.getLogger(__name__)``. Сообщения
выводятся в stderr, чтобы не смешиваться с результатом работы программы.
"""
import logging
import sys

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def setup_logging(level: str = "INFO") -> None:
    """Включает вывод логов в stderr с временем, уровнем и именем модуля.

    Повторный вызов заменяет прежние настройки.

    Args:
        level: Уровень логирования: ``DEBUG``, ``INFO``, ``WARNING`` или ``ERROR``.
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=LOG_FORMAT,
        stream=sys.stderr,
        force=True,
    )
