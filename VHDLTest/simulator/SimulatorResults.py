import re
from datetime import datetime
from typing import List, Tuple
from enum import Enum
from ..logger.Log import Log


class ResultLineType(Enum):
    """Result Line Type enumeration."""

    text = 0
    warning = 10
    error = 11
    execution_note = 20
    execution_warning = 21
    execution_error = 22
    execution_failure = 23

    @property
    def is_warning(self) -> bool:
        """Test if result type is warning."""
        return (self == ResultLineType.warning
                or self == ResultLineType.execution_warning)

    @property
    def is_error(self) -> bool:
        """Test if result type is error."""
        return (self == ResultLineType.error
                or self == ResultLineType.execution_error
                or self == ResultLineType.execution_failure)


class ResultLine(object):
    """Result Line class."""

    def __init__(self, line_type: ResultLineType, text: str) -> None:
        """
        Results Line constructor.

        Args:
            line_type (ResultLineType): Type of result line
            text (str): Text of result line
        """

        self._type = line_type
        self._text = text

    @property
    def line_type(self) -> ResultLineType:
        return self._type

    @property
    def text(self) -> str:
        return self._text


class SimulatorResults(object):
    """Simulator Results class."""

    def __init__(self,
                 start: datetime,
                 duration: float,
                 returncode: int,
                 lines: List[str],
                 rules: List[Tuple[str, ResultLineType]]) -> None:
        """Simulator Results constructor."""
        self._lines = []
        self._start = start
        self._duration = duration
        self._returncode = returncode
        self._lines = []

        # Process all lines appending output
        for line in lines:
            # Look for matching rule
            line_type = None
            for rule in rules:
                if re.match(rule[0], line):
                    line_type = rule[1]
                    break

            # Append the line
            self._lines.append(ResultLine(line_type or ResultLineType.text, line))

    @property
    def returncode(self) -> int:
        return self._returncode

    @property
    def start(self) -> datetime:
        return self._start

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def lines(self) -> List[ResultLine]:
        return self._lines

    @property
    def any_errors(self) -> bool:
        return self._returncode != 0 or any(line.line_type.is_error for line in self._lines)

    def print(self, log: Log) -> None:
        """
        Print results.
        """

        for line in self._lines:
            if line.line_type == ResultLineType.warning:
                log.write(Log.warning, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.error:
                log.write(Log.error, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.execution_note:
                log.write(Log.success, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.execution_warning:
                log.write(Log.warning, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.execution_error:
                log.write(Log.error, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.execution_failure:
                log.write(Log.error, line.text, Log.end, '\n')
            else:
                log.write(line.text, '\n')
