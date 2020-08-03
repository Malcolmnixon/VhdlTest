import re
from typing import List, Tuple
from enum import Enum


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
    def is_warning(self):
        """Test if result type is warning."""
        return (self == ResultLineType.warning or
                self == ResultLineType.execution_warning)

    @property
    def is_error(self):
        """Test if result type is error."""
        return (self == ResultLineType.error or
                self == ResultLineType.execution_error or
                self == ResultLineType.execution_failure)


class ResultLine(object):
    """Result Line class."""

    def __init__(self, line_type: ResultLineType, text: str):
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

    def __init__(self):
        """Simulator Results constructor."""
        self._lines = []
        self._exit_code = 0

    def append_output(self, output: List[str], rules: List[Tuple[str, ResultLineType]]):
        """
        Append console output to simulator results.

        Args:
            output (List[str]): Output lines to append
            rules (List[Tuple[str, ResultLineType]]): List of parse rules
        """

        # Process all lines appending output
        for line in output:
            # Look for matching rule
            line_type = None
            for rule in rules:
                if re.match(rule[0], line):
                    line_type = rule[1]
                    break

            # Append the line
            self._lines.append(ResultLine(line_type or ResultLineType.text, line))

    def set_exit_code(self, code: int):
        """Set the exit code of the process creating results."""
        self._exit_code = code

    @property
    def lines(self) -> List[ResultLine]:
        return self._lines

    @property
    def any_errors(self) -> bool:
        return self._exit_code != 0 or any(line.line_type.is_error for line in self._lines)

    def print(self):
        """
        Print results.
        """

        for line in self._lines:
            print(line.text)
