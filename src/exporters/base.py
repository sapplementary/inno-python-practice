from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def export(self, data: dict[str, list[dict]]) -> str: ...

