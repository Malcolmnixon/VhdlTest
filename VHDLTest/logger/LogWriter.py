from typing import Any


class LogWriter(object):

    def close(self) -> None:
        """Close the writer."""

    def write(self, *items: Any) -> None:
        """Write items to the log."""
