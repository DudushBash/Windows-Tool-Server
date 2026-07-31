from dataclasses import dataclass
from enum import Enum
from typing import Any

class ObjectType(Enum):
    APPLICATION = "application"
    DOCUMENT = "document"
    DEVICE = "device"
    FOLDER = "folder"

@dataclass(frozen=True)
class SystemObject:
    id:str
    name:str
    path:str
    type:ObjectType
    description:str
    keywords: tuple[str, ...]
    metadata:dict[str,Any]

