from ..Configuration import Configuration
from ..runner.RunResults import RunResults


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

    def compile(self, config: Configuration) -> RunResults:
        """Compile the VHDL files into a library."""

    def test(self, config: Configuration, test: str) -> RunResults:
        """Execute a single test."""
