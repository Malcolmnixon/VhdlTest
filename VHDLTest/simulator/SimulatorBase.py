"""Module for SimulatorBase class."""

from ..Configuration import Configuration
from ..runner.RunResults import RunResults


class SimulatorBase(object):
    """Generic Simulator interface."""

    def __init__(self, name: str) -> None:
        """
        Initialize new SimulatorBase instance.

        Args:
            name (str): Name of the simulator
        """
        self._name = name
        self._path = self.__class__.find_path()

    @property
    def name(self) -> str:
        """Get the simulator name."""
        return self._name

    @property
    def path(self) -> str:
        """Get the simulator install path."""
        return self._path

    @classmethod
    def is_available(cls) -> bool:
        """Test if the simulator is available."""
        return cls.find_path() is not None

    @classmethod
    def find_path(cls) -> str:
        """Find the path to the simulator."""
        raise NotImplementedError

    def compile(self, config: Configuration) -> RunResults:
        """
        Compile the VHDL files into a library.

        Args:
            config (Configuration): Configuration data for compile.
        """
        raise NotImplementedError

    def test(self, config: Configuration, test: str) -> RunResults:
        """
        Execute a test-bench.

        Args:
            config (Configuration): Configuration data for test.
            test (str): Name of test-bench.
        """
        raise NotImplementedError
