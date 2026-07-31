from pathlib import Path
import os
from models.object import SystemObject
from tools.result import ToolResult

class ApplicationLauncher:
    def launch(self,obj: SystemObject,) -> ToolResult:

        if not obj.path:
            return ToolResult(
                success=False,
                message="У приложения отсутствует путь запуска.",
            )

        path = Path(obj.path)

        if not path.exists():
            return ToolResult(
                success=False,
                message="Файл не найден.",
            )

        try:
            os.startfile(
                path,
                arguments=obj.metadata.get("arguments") or None,
                cwd=obj.metadata.get("working_directory") or None,
            )

            return ToolResult(
                success=True,
                message=f'"{obj.name}" успешно запущено.',
            )

        except OSError as error:
            return ToolResult(
                success=False,
                message=f"Ошибка запуска: {error}",
            )
