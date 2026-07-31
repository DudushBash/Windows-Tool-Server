from abc import ABC, abstractmethod
from models.object import SystemObject

class BaseScanner(ABC):
    @abstractmethod
    def scan(self) -> list[SystemObject]:
        pass