from typing import Any
from .LogConsole import LogConsole
from .LogFile import LogFile
from .LogItem import LogItem


class Log(object):
    # Simple access to LogItem types
    end = LogItem.END
    success = LogItem.SUCCESS
    info = LogItem.INFO
    warning = LogItem.WARNING
    error = LogItem.ERROR

    def __init__(self) -> None:
        # Start with only console logger
        self._loggers = [LogConsole()]

    def add_log_file(self, filename: str) -> None:
        # Append new LogFile to loggers
        self._loggers.append(LogFile(filename))

    def close(self) -> None:
        # Close all loggers
        for logger in self._loggers:
            logger.close()

        # Dispose of all extra loggers
        self._loggers = self._loggers[0:1]

    def write(self, *args: Any) -> None:
        # Send to all loggers
        for logger in self._loggers:
            logger.write(*args)
