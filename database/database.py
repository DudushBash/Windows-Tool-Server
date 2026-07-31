import sqlite3

class SQLiteDatabase:
    def __init__(self, db_path: str):
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_objects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            type TEXT,
            description TEXT,
            keywords TEXT,
            metadata TEXT,
            search_text TEXT
        )
        """)
        self._connection.commit()
        cursor.close()
    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection