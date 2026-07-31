from models.object import SystemObject
import os


class MergeEngine:
    def merge(
        self,
        objects: list[SystemObject],
    ) -> list[SystemObject]:

        merged: dict[str, SystemObject] = {}

        for obj in objects:
            key = self._create_key(obj)

            if key not in merged:
                merged[key] = obj
                continue

            merged[key] = self._merge_objects(
                merged[key],
                obj,
            )

        return list(merged.values())

    @staticmethod
    def _create_key(obj: SystemObject) -> str:
        if obj.path:
            return os.path.normcase(os.path.normpath(obj.path))

        return obj.name.lower()

    @staticmethod
    def _merge_objects(
        first: SystemObject,
        second: SystemObject,
    ) -> SystemObject:

        description = (
            first.description
            if first.description
            else second.description
        )

        path = (
            first.path
            if first.path
            else second.path
        )

        keywords = tuple(
            sorted(
                set(first.keywords) | set(second.keywords)
            )
        )

        metadata = {**first.metadata, **second.metadata}

        return SystemObject(
            id=first.id,
            name=first.name,
            path=path,
            type=first.type,
            description=description,
            keywords=keywords,
            metadata=metadata,
        )
