import winreg
import os
import re
from pathlib import Path
from scanner.base import BaseScanner
from models.object import SystemObject, ObjectType


class RegistryScanner(BaseScanner):
    _UNINSTALL_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    def scan(self) -> list[SystemObject]:
        objects = []
        registry_paths = [(winreg.HKEY_LOCAL_MACHINE, self._UNINSTALL_PATH)]
        # 64-bit Windows stores many 32-bit applications in this separate view.
        if os.environ.get("PROCESSOR_ARCHITECTURE", "").endswith("64"):
            registry_paths.append(
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
            )
        registry_paths.append((winreg.HKEY_CURRENT_USER, self._UNINSTALL_PATH))

        for root, path in registry_paths:
            objects.extend(
                self._scan_registry_path(root, path)
            )
        return objects

    def _scan_registry_path(self,root,path: str,) -> list[SystemObject]:
        objects = []
        try:
            registry_key = winreg.OpenKey(root, path)
        except OSError:
            return objects

        with registry_key:
            subkey_count = winreg.QueryInfoKey(registry_key)[0]

            for index in range(subkey_count):
                try:
                    subkey_name = winreg.EnumKey(registry_key,index,)
                    subkey_path = f"{path}\\{subkey_name}"

                    obj = self._read_application(root,subkey_path,)

                    if obj is not None:
                        objects.append(obj)

                except OSError:
                    continue

        return objects
    @staticmethod
    def _extract_executable(value: str | None) -> str:
        """Extract an executable path from DisplayIcon or command line fields."""
        if not value:
            return ""
        expanded = os.path.expandvars(value.strip().lstrip("@"))
        match = re.search(
            r'"([^\"]+?\.exe)"|([A-Za-z]:\\.*?\.exe)(?:[,\s]|$)',
            expanded,
            re.IGNORECASE,
        )
        if not match:
            return ""
        candidate = match.group(1) or match.group(2)
        path = Path(candidate)
        return str(path) if path.is_file() else ""

    @staticmethod
    def _find_executable_in_folder(install_location: str | None) -> str:
        if not install_location:
            return ""
        folder = Path(os.path.expandvars(install_location.strip().strip('"')))
        if folder.is_file() and folder.suffix.lower() == ".exe":
            return str(folder)
        if not folder.is_dir():
            return ""
        # Only accept an unambiguous executable; guessing among many is worse
        # than exposing a result that cannot be launched.
        executables = list(folder.glob("*.exe"))
        return str(executables[0]) if len(executables) == 1 else ""

    def _resolve_application_path(
        self,
        install_location: str | None,
        display_icon: str | None,
        uninstall_string: str | None,
    ) -> str:
        return (
            self._extract_executable(display_icon)
            or self._extract_executable(uninstall_string)
            or self._find_executable_in_folder(install_location)
        )

    def _read_application(self,root,subkey_path: str,) -> SystemObject | None:
        try:
            with winreg.OpenKey(root,subkey_path,) as key:
                name = self._get_value(key,"DisplayName",)
                if not name:
                    return None
                install_location = self._get_value(key,"InstallLocation",)
                display_icon = self._get_value(key,"DisplayIcon",)
                uninstall_string = self._get_value(key,"UninstallString",)
                application_path = self._resolve_application_path(
                    install_location, display_icon, uninstall_string
                )
                publisher = self._get_value(key,"Publisher",)
                version = self._get_value(key,"DisplayVersion",)
                return SystemObject(
                    id=f"registry:{root}:{subkey_path}",
                    name=name,
                    path=application_path,
                    type=ObjectType.APPLICATION,
                    description=(
                        f"Installed application by {publisher}"
                        if publisher else "Installed application"
                    ),
                    keywords=tuple(
                        word.lower()
                        for word in name.split()
                    ),
                    metadata={"publisher": publisher or "","version": version or "","registry_path": subkey_path,"display_icon": display_icon or "","uninstall_string": uninstall_string or "",},
                )

        except OSError:
            return None
    @staticmethod
    def _get_value(key,value_name: str,) -> str | None:
        try:
            value, _ = winreg.QueryValueEx(key,value_name,)
            return str(value)
        except FileNotFoundError:
            return None
