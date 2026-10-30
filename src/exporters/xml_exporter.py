import xml.etree.ElementTree as ET

from src.exporters.base import Exporter


class XmlExporter(Exporter):
    def export(self, data: dict[str, list[dict]]) -> str:
        root = ET.Element("result")
        for query_name, rows in data.items():
            query_el = ET.SubElement(root, query_name)
            for row in rows:
                row_el = ET.SubElement(query_el, "row")
                for column, value in row.items():
                    col_el = ET.SubElement(row_el, column)
                    col_el.text = "" if value is None else str(value)
        ET.indent(root)
        body = ET.tostring(root, encoding="unicode")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + body
