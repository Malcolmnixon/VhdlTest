import re
from datetime import datetime
from typing import List, Tuple
from enum import Enum
from ..logger.Log import Log


class ResultLineType(Enum):
    """Result Line Type enumeration."""

    text = 0
    run_warning = 1
    run_error = 2
    test_warning = 3
    test_error = 4


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
                 output: str,
                 rules: List[Tuple[str, ResultLineType]]) -> None:
        """Simulator Results constructor."""
        self._lines = []
        self._start = start
        self._duration = duration
        self._returncode = returncode
        self._output = output
        self._lines = []

        # Process all lines appending output
        for line in output.splitlines():
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
    def output(self) -> str:
        return self._output

    @property
    def lines(self) -> List[ResultLine]:
        return self._lines

    @property
    def error_lines(self) -> List[str]:
        return [line.text for line in self._lines if line.line_type == ResultLineType.run_error]

    @property
    def failure_lines(self) -> List[str]:
        return [line.text for line in self._lines if line.line_type == ResultLineType.test_error]

    @property
    def error(self) -> bool:
        return self._returncode != 0 or any(self.error_lines)

    @property
    def failure(self) -> bool:
        return self._returncode == 0 and any(self.failure_lines)

    @property
    def passed(self) -> bool:
        return not (self.error or self.failure)

    @property
    def error_message(self) -> str:
        # If we have run errors then return them
        run_errors = self.error_lines
        if run_errors:
            return '\n'.join(run_errors)

        # If we have a non-zero return code then describe it
        if self._returncode != 0:
            return f'Program terminated with returncode {self._returncode}'

        # Could not build a suitable error description
        return None

    @property
    def failure_output(self) -> str:
        # If we have test errors then return them
        test_errors = self.failure_lines
        if test_errors:
            return '\n'.join(test_errors)

        # Could not build a suitable failure output
        return None

    def print(self, log: Log) -> None:
        """
        Print results.
        """

        for line in self._lines:
            if line.line_type == ResultLineType.run_warning:
                log.write(Log.warning, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.run_error:
                log.write(Log.error, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.test_warning:
                log.write(Log.warning, line.text, Log.end, '\n')
            elif line.line_type == ResultLineType.test_error:
                log.write(Log.error, line.text, Log.end, '\n')
            else:
                log.write(line.text, '\n')
