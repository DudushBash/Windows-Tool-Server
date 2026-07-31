from datetime import datetime
from fastapi import FastAPI
from api.model import IndexRefreshResponse, SearchHit, SearchResponse, ToolRequest, ToolResponse
from api.bootstrap import DATABASE_PATH, create_services
from database.database import SQLiteDatabase
from database.repository import SystemObjectRepository
from scanner.indexing import refresh_system_index

app = FastAPI(title="Delorian Tool Server",)
tool_manager, search_engine = create_services()

@app.post("/tools/execute")
def execute_tool(request: ToolRequest):
    result = tool_manager.execute(request.tool,**request.arguments,)
    return ToolResponse(success=result.success,message=result.message,)

@app.get("/tools")
def get_tools():
    return tool_manager.list_tools()


@app.get("/search", response_model=SearchResponse)
def search(query: str, limit: int = 5):
    """Find applications by exact terms and semantic similarity."""
    limit = max(1, min(limit, 20))
    results = search_engine.search(query, limit=limit)
    return SearchResponse(
        semantic_enabled=search_engine.capabilities.semantic_enabled,
        results=[
            SearchHit(
                id=result.object.id,
                name=result.object.name,
                path=result.object.path,
                type=result.object.type.value,
                description=result.object.description,
                score=round(result.score, 4),
            )
            for result in results
        ],
    )


@app.post("/index/refresh", response_model=IndexRefreshResponse)
def refresh_index():
    """Scan Start Menu and Windows registry, then rebuild the search index."""
    global tool_manager, search_engine

    repository = SystemObjectRepository(SQLiteDatabase(str(DATABASE_PATH)))
    count = refresh_system_index(repository)
    tool_manager, search_engine = create_services()
    return IndexRefreshResponse(indexed_objects=count)
