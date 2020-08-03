from ..Configuration import Configuration


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

    def compile(self, config: Configuration):
        """Compile the VHDL files into a library."""

    def test(self, config: Configuration, test: str):
        """Execute a single test."""

    def test_all(self, config: Configuration):
        """Run all configured tests."""
        return [self.test(config, test) for test in config.tests]
