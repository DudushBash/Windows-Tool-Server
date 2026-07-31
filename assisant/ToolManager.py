from tools.base import BaseTool
from tools.result import ToolResult

class ToolManager:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
    def register(self,name: str,tool: BaseTool,) -> None:
        if name in self._tools:
            raise ValueError(f'Tool "{name}" уже зарегистрирован.')
        self._tools[name] = tool

    def execute(self,name: str,**kwargs,) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(success=False,message=f'Tool "{name}" не найден.',)
        return tool.execute(**kwargs)

    def has_tool(self,name: str,) -> bool:
        return name in self._tools

    def list_tools(self,) -> list[str]:
        return sorted(self._tools.keys())