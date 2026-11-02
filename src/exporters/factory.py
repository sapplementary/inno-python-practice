"""Фабрика экспортёров: выбор формата вывода по его названию."""
from src.exporters.base import Exporter
from src.exporters.json_exporter import JsonExporter
from src.exporters.xml_exporter import XmlExporter


class ExporterFactory:
    """Создаёт экспортёр по названию формата.

    Чтобы добавить формат, нужно написать подкласс ``Exporter`` и добавить
    его в словарь ``_exporters``.
    """

    _exporters: dict[str, type[Exporter]] = {
        "json": JsonExporter,
        "xml": XmlExporter,
    }

    @classmethod
    def create(cls, fmt: str) -> Exporter:
        """Возвращает экспортёр для указанного формата.

        Args:
            fmt: Название формата (``json`` или ``xml``), регистр не важен.

        Returns:
            Новый экземпляр подходящего экспортёра.

        Raises:
            ValueError: Если такого формата нет.
        """
        try:
            return cls._exporters[fmt.lower()]()
        except KeyError:
            available = ", ".join(cls._exporters)
            raise ValueError(f"Неизвестный формат '{fmt}'. Доступны: {available}") from None
