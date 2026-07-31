from dataclasses import dataclass
from models.object import SystemObject

@dataclass(frozen=True)
class SearchResult:
    object: SystemObject
    score: float