from models.object import SystemObject
from database.database import SQLiteDatabase
from serializers.object_serializer import SystemObjectMapper

class SystemObjectRepository:
    _INSERT_QUERY = """
    INSERT OR REPLACE INTO system_objects (
        id,
        name,
        path,
        type,
        description,
        keywords,
        metadata,
        search_text
    )
    VALUES (
        :id,
        :name,
        :path,
        :type,
        :description,
        :keywords,
        :metadata,
        :search_text
    )
    """
    def __init__(self, database: SQLiteDatabase):
        self._database = database

    def save(self, obj: SystemObject) -> None:
        record = SystemObjectMapper.to_record(obj)
        cursor = self._database.connection.cursor()
        cursor.execute(self._INSERT_QUERY, record)
        self._database.connection.commit()
        cursor.close()

    def save_all(self, objects: list[SystemObject]) -> None:
        records = [SystemObjectMapper.to_record(obj) for obj in objects]
        cursor = self._database.connection.cursor()
        cursor.executemany(self._INSERT_QUERY, records)
        self._database.connection.commit()
        cursor.close()

    def replace_all(self, objects: list[SystemObject]) -> None:
        """Atomically replace stale scan results with a complete new scan."""
        records = [SystemObjectMapper.to_record(obj) for obj in objects]
        with self._database.connection:
            self._database.connection.execute("DELETE FROM system_objects")
            self._database.connection.executemany(self._INSERT_QUERY, records)

    def get_all(self) -> list[SystemObject]:
        cursor = self._database.connection.cursor()
        cursor.execute("""
            SELECT *
            FROM system_objects
        """)
        rows = cursor.fetchall()
        cursor.close()
        return [SystemObjectMapper.from_record(dict(row)) for row in rows]
    
    def get_by_id(self, object_id: str) -> SystemObject | None:
        cursor = self._database.connection.cursor()
        try:
            cursor.execute("SELECT * FROM system_objects WHERE id = ?", (object_id,))
            row = cursor.fetchone()
            return SystemObjectMapper.from_record(dict(row)) if row else None
        finally:
            cursor.close()

    def delete(self, object_id: str) -> None:
        cursor = self._database.connection.cursor()
        try:
            cursor.execute("DELETE FROM system_objects WHERE id = ?", (object_id,))
            self._database.connection.commit()
        finally:
            cursor.close()
