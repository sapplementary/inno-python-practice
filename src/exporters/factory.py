from src.exporters.base import Exporter
from src.exporters.json_exporter import JsonExporter
from src.exporters.xml_exporter import XmlExporter


class ExporterFactory:
    _exporters: dict[str, type[Exporter]] = {
        "json": JsonExporter,
        "xml": XmlExporter,
    }

    @classmethod
    def create(cls, fmt: str) -> Exporter:
        try:
            return cls._exporters[fmt.lower()]()
        except KeyError:
            available = ", ".join(cls._exporters)
            raise ValueError(f"Неизвестный формат '{fmt}'. Доступны: {available}") from None
