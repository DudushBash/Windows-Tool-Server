from pathlib import Path
from dataclasses import dataclass
import win32com.client
import os
import logging
from scanner.base import BaseScanner
from models.object import SystemObject, ObjectType


@dataclass(frozen=True)
class ShortcutInfo:
    target_path: str
    description: str
    icon_location: str
    arguments: str
    working_directory: str

class StartMenuScanner(BaseScanner):
    def __init__(self):
        self._shell = win32com.client.Dispatch("WScript.Shell")

    def _get_start_menu_folders(self) -> list[Path]:
        appdata = os.environ.get("APPDATA")
        programdata = os.environ.get("ProgramData")
        folders = []

        if appdata:
            folders.append(
                Path(appdata) / "Microsoft" / "Windows" / "Start Menu"
            )

        if programdata:
            folders.append(
                Path(programdata) / "Microsoft" / "Windows" / "Start Menu"
            )
        return [folder for folder in folders if folder.is_dir()]

    def _find_shortcuts(self, folders: list[Path]) -> list[Path]:
        shortcuts = []
        for folder in folders:
            try:
                shortcuts.extend(path for path in folder.rglob("*.lnk") if path.is_file())
            except OSError as error:
                logging.warning("Cannot scan Start Menu folder %s: %s", folder, error)
        return shortcuts
    
    def _load_shortcut(self, shortcut: Path) -> ShortcutInfo | None:
        try:
            lnk = self._shell.CreateShortCut(str(shortcut))

            return ShortcutInfo(
                target_path=lnk.TargetPath,
                description=lnk.Description or "",
                icon_location=lnk.IconLocation or "",
                arguments=lnk.Arguments or "",
                working_directory=lnk.WorkingDirectory or "",
            )
        except Exception as error:
            logging.warning("Cannot read shortcut %s: %s", shortcut, error)
            return None
    
    def _create_keywords(self, name: str) -> tuple[str, ...]:
        return tuple(part.lower() for part in name.replace("-", " ").split())
    
    def _create_object(self,shortcut: Path,) -> SystemObject | None:
        info = self._load_shortcut(shortcut)
        if info is None or not info.target_path:
            return None
        target_path = os.path.expandvars(info.target_path)
        return SystemObject(
            id=f"start-menu:{shortcut.resolve()}",
            name=shortcut.stem,
            path=target_path,
            type=ObjectType.APPLICATION,
            description=info.description,
            keywords=self._create_keywords(shortcut.stem),
            metadata={
                "icon": info.icon_location,
                "arguments": info.arguments,
                "working_directory": info.working_directory,
                "shortcut_path": str(shortcut),
            },
        )
    def scan(self) -> list[SystemObject]:
        folders = self._get_start_menu_folders()
        shortcuts = self._find_shortcuts(folders)

        objects = []

        for shortcut in shortcuts:
            obj = self._create_object(shortcut)

            if obj is not None:
                objects.append(obj)

        return objects


if __name__ == "__main__":
    scanner = StartMenuScanner()
    objects = scanner.scan()
    print(f"Найдено приложений: {len(objects)}\n")
    for obj in objects:
        print(f"{obj.name}")
        print(f"  Path: {obj.path}")
        print(f"  Keywords: {obj.keywords}")
        print()
