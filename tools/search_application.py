from search.semantic import HybridSearchEngine
from tools.base import BaseTool
from tools.result import ToolResult


class SearchApplicationTool(BaseTool):

    def __init__(self,search_engine: HybridSearchEngine,):
        self._search_engine = search_engine

    def execute(self,query: str,) -> ToolResult:
        results = self._search_engine.search(query)
        if not results:
            return ToolResult(success=False,message="Приложение не найдено.",)
        result = results[0]
        obj = result.object
        return ToolResult(
            success=True,
            message=(
                f"Найдено:\n"
                f"{obj.name}\n"
                f"Path: {obj.path}\n"
                f"Score: {result.score:.3f}"
            ),
            data=results,
        )
