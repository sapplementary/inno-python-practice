"""Экспорт результата в формат XML.

Структура документа: корневой элемент ``result``, внутри него элемент
на каждый запрос, внутри него элементы ``row`` (по одному на строку),
внутри них по элементу на каждую колонку.
"""
import xml.etree.ElementTree as ET

from src.exporters.base import Exporter


class XmlExporter(Exporter):
    """Сериализует результат в XML."""

    def export(self, data: dict[str, list[dict]]) -> str:
        """Превращает результат в XML-строку.

        Все значения записываются как текст, ``None`` превращается в пустой
        элемент. Названия запросов и колонок используются как имена элементов,
        поэтому они должны быть допустимыми именами XML (без пробелов).

        Args:
            data: Словарь «название запроса: строки результата».

        Returns:
            XML-текст с объявлением кодировки UTF-8 и отступами.
        """
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
