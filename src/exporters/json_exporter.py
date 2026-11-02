"""Экспорт результата в формат JSON."""
import json

from src.exporters.base import Exporter


class JsonExporter(Exporter):
    """Сериализует результат в читаемый JSON."""

    def export(self, data: dict[str, list[dict]]) -> str:
        """Превращает результат в JSON-строку.

        Используются отступы, а кириллица и другие символы не экранируются.

        Args:
            data: Словарь «название запроса: строки результата».
                Значения должны быть сериализуемы в JSON (числа, строки).

        Returns:
            JSON-текст.
        """
        return json.dumps(data, ensure_ascii=False, indent=2)
