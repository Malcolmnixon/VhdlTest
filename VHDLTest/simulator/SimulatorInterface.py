import subprocess
from typing import List, Tuple
from ..Configuration import Configuration
from .SimulatorResults import SimulatorResults
from .SimulatorResults import ResultLineType


class SimulatorInterface(object):
    """
    Generic Simulator interface.
    """

    def __init__(self, name: str):
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
        # Create results
        results = SimulatorResults()
        try:
            # Run the process and capture the output
            out = subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            results.set_exit_code(err.returncode)
            out = err.output

        # Create simulator results and parse output lines
        results.append_output(
            out.decode('utf-8').splitlines(),
            rules)

        # Return parsed output
        return results
