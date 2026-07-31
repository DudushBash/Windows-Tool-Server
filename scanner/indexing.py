"""Rebuild the persisted application index from Windows discovery sources."""

from database.repository import SystemObjectRepository
from scanner.manager import ScannerManager
from scanner.registry import RegistryScanner
from scanner.start_menu import StartMenuScanner


def refresh_system_index(repository: SystemObjectRepository) -> int:
    manager = ScannerManager([StartMenuScanner(), RegistryScanner()])
    objects = manager.scan_all()
    repository.replace_all(objects)
    return len(objects)
