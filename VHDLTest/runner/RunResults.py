import subprocess
import re
from datetime import datetime
from enum import Enum
from typing import TypeVar, List, Tuple
from ..logger.Log import Log


class RunCategory(Enum):
    TEXT = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    @property
    def is_info(self) -> bool:
        return self.value >= RunCategory.INFO.value

    @property
    def is_warning(self) -> bool:
        return self.value >= RunCategory.WARNING.value

    @property
    def is_error(self) -> bool:
        return self.value >= RunCategory.WARNING.value


class RunLine(object):
    def __init__(self,
                 text: str,
                 category: RunCategory) -> None:
        self.text = text
        self.category = category


T = TypeVar('T', bound='RunResults')


class RunResults(object):
    def __init__(self,
                 start: datetime,
                 duration: float,
                 returncode: int,
                 output: str,
                 rules: List[Tuple[str, RunCategory]]) -> None:
        self.start = start
        self.duration = duration
        self.returncode = returncode
        self.output = output
        self.lines = []

        # Process all lines appending output
        for line in output.splitlines():
            # Look for matching rule
            category = RunCategory.TEXT
            for rule in rules:
                if re.match(rule[0], line):
                    category = rule[1]
                    break

            # Append the line
            self.lines.append(RunLine(line, category))

    @property
    def category(self) -> RunCategory:
        # If no lines then just return text
        if not self.lines:
            return RunCategory.TEXT

        # Return the maximum value
        return RunCategory(max([line.category.value for line in self.lines]))

    @property
    def info(self) -> bool:
        return self.returncode != 0 or self.category.value >= RunCategory.INFO.value

    @property
    def warning(self) -> bool:
        return self.returncode != 0 or self.category.value >= RunCategory.WARNING.value

    @property
    def error(self) -> bool:
        return self.returncode != 0 or self.category.value >= RunCategory.ERROR.value

    @property
    def failure(self) -> bool:
        return self.returncode != 0

    @property
    def error_info(self) -> str:
        # Get the error lines
        errors = [line.text for line in self.lines if line.category.is_error]

        # Add any returncode info
        if self.returncode != 0:
            errors.append(f'Program terminated with returncode {self.returncode}')

        # Join into single line
        return '\n'.join(errors)

    def print(self, log: Log) -> None:
        """
        Print results.
        """

        for line in self.lines:
            if line.category == RunCategory.INFO:
                log.write(Log.info, line.text, Log.end, '\n')
            elif line.category == RunCategory.WARNING:
                log.write(Log.warning, line.text, Log.end, '\n')
            elif line.category == RunCategory.ERROR:
                log.write(Log.error, line.text, Log.end, '\n')
            else:
                log.write(line.text, '\n')

    @staticmethod
    def run(args: List[str],
            rules: List[Tuple[str, RunCategory]]) -> T:
        # Capture the start time
        start = datetime.now()

        # Create results
        try:
            # Run the process and capture the output
            out = subprocess.check_output(args, stderr=subprocess.STDOUT)
            returncode = 0
        except subprocess.CalledProcessError as err:
            out = err.output
            returncode = err.returncode

        # Calculate the duration
        end = datetime.now()
        duration = (end - start).total_seconds()

        # Return the results
        return RunResults(
            start,
            duration,
            returncode,
            out.decode('utf-8'),
            rules)
