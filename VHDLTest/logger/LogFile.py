from typing import Any
from .LogWriter import LogWriter
from .LogItem import LogItem


class LogFile(LogWriter):

    def __init__(self, filename: str) -> None:
        self._stream = open(filename, 'w')

    def close(self) -> None:
        self._stream.close()

    def write(self, *items: Any) -> None:
        for item in items:
            if type(item) is not LogItem:
                self._stream.write(item)
