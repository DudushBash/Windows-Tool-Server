from search.semantic import HybridSearchEngine
from tools.result import ToolResult
from tools.base import BaseTool
from tools.launcher import ApplicationLauncher


class OpenApplicationTool(BaseTool):

    def __init__(self,search_engine: HybridSearchEngine,launcher: ApplicationLauncher,):
        self._search_engine = search_engine
        self._launcher = launcher

    def execute(self,query: str,) -> ToolResult:
        result = self._search_engine.search_one(query)
        if result is None:
            return ToolResult(
                success=False,
                message="Приложение не найдено.",
            )
        return self._launcher.launch(result.object)
