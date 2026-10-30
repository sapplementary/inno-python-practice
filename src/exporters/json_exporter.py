import json

from src.exporters.base import Exporter


class JsonExporter(Exporter):
    def export(self, data: dict[str, list[dict]]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)
