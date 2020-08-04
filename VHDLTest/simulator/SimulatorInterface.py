import subprocess
from datetime import datetime
from typing import List, Tuple
from ..Configuration import Configuration
from .SimulatorResults import SimulatorResults
from .SimulatorResults import ResultLineType


class SimulatorInterface(object):
    """
    Generic Simulator interface.
    """

    def __init__(self, name: str) -> None:
        """
        Simulator Interface constructor.

        Args:
            name (str): Name of the simulator
        """
        self._name = name
        self._path = self.__class__.find_path()

    @property
    def name(self) -> str:
        """Gets the simulator name."""
        return self._name

    @property
    def path(self) -> str:
        """Gets the simulator install path."""
        return self._path

    @classmethod
    def is_available(cls) -> bool:
        """Test if the simulator is available."""
        return cls.find_path() is not None

    @classmethod
    def find_path(cls) -> str:
        """Find the path to the simulator."""

    def compile(self, config: Configuration) -> SimulatorResults:
        """Compile the VHDL files into a library."""

    def test(self, config: Configuration, test: str) -> SimulatorResults:
        """Execute a single test."""

    def test_all(self, config: Configuration) -> List[SimulatorResults]:
        """Run all configured tests."""
        return [(test, self.test(config, test)) for test in config.tests]

    @staticmethod
    def run_process(args: List[str], rules: List[Tuple[str, ResultLineType]]) -> SimulatorResults:
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
        return SimulatorResults(
            start,
            duration,
            returncode,
            out.decode('utf-8'),
            rules)
