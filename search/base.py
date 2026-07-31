from abc import ABC, abstractmethod
from models.object import SystemObject

class BaseSearchEngine(ABC):
    @abstractmethod
    def search(self, query: str, limit: int = 5) -> list[SystemObject]:
        pass