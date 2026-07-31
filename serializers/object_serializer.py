import json
from typing import Any
from models.object import SystemObject, ObjectType

class SystemObjectMapper:
    @staticmethod
    def _build_search_text(obj: SystemObject) -> str:
        parts = [obj.name,obj.description,*obj.keywords,]
        return " ".join(part for part in parts if part)

    @staticmethod
    def to_record(obj: SystemObject) -> dict[str, Any]:
        return {
            "id": obj.id,
            "name": obj.name,
            "path": obj.path,
            "type": obj.type.value,
            "description": obj.description,
            "keywords":json.dumps(obj.keywords, ensure_ascii=False),
            "metadata":json.dumps(obj.metadata, ensure_ascii=False),
            "search_text": SystemObjectMapper._build_search_text(obj),
        }
    @staticmethod
    def from_record(record: dict[str, Any]) -> SystemObject:
        return SystemObject(
            id=record["id"],
            name=record["name"],
            path=record["path"],
            type=ObjectType(record["type"]),
            description=record["description"],
            keywords=tuple(json.loads(record["keywords"])),
            metadata=json.loads(record["metadata"]),
        )