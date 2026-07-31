from scanner.merge import MergeEngine
import logging

class ScannerManager:
    def __init__(self, scanners):
        self._scanners = scanners
        self._merge_engine = MergeEngine()

    def scan_all(self):
        objects = []

        for scanner in self._scanners:
            try:
                objects.extend(scanner.scan())
            except Exception as error:
                # One inaccessible source must not make all installed apps vanish.
                logging.exception("Scanner %s failed: %s", type(scanner).__name__, error)

        return self._merge_engine.merge(objects)
