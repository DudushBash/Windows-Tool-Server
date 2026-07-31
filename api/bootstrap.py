from pathlib import Path

from database.database import SQLiteDatabase
from database.repository import SystemObjectRepository

from search.indexer import SearchIndexBuilder
from search.semantic import HybridSearchEngine

from tools.launcher import ApplicationLauncher
from tools.open_app import OpenApplicationTool
from tools.search_application import SearchApplicationTool
from assisant.ToolManager import ToolManager


DATABASE_PATH = Path(__file__).resolve().parent.parent / "delorean.db"


def create_services() -> tuple[ToolManager, HybridSearchEngine]:
    db = SQLiteDatabase(str(DATABASE_PATH))
    repo = SystemObjectRepository(db)
    builder = SearchIndexBuilder(repo)
    index = builder.build()
    search_engine = HybridSearchEngine(index)
    launcher = ApplicationLauncher()
    manager = ToolManager()
    manager.register("open_application",OpenApplicationTool(search_engine, launcher),)
    manager.register("search_application",SearchApplicationTool(search_engine),)

    return manager, search_engine


def create_tool_manager() -> ToolManager:
    """Backward-compatible factory for consumers that only need tools."""
    return create_services()[0]
