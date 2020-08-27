"""Module for the Vivado simulator class."""

import os
import shutil
from .SimulatorBase import SimulatorBase
from ..Configuration import Configuration
from ..runner.RunResults import RunCategory
from ..runner.RunResults import RunResults


class Vivado(SimulatorBase):
    """Vivado Simulator class."""

    """Compile parse rules."""
    compile_rules = [
        (r"Error: ", RunCategory.ERROR)
    ]

    """Test results parse rules."""
    test_rules = [
        (r"Note: ", RunCategory.INFO),
        (r"Warning: ", RunCategory.WARNING),
        (r"Error: ", RunCategory.ERROR),
        (r"Failure: ", RunCategory.ERROR)
    ]

    def __init__(self) -> None:
        """Initialize a new Vivado instance."""
        super().__init__('Vivado')

    @classmethod
    def find_path(cls) -> str:
        """Find the path to Vivado binaries."""
        # First check environment variable
        path = os.getenv('VHDLTEST_VIVADO_PATH')
        if path:
            return path

        # Find vivado executable
        path = shutil.which('vivado')
        if not path:
            return ''

        # Return directory name
        return os.path.dirname(path)

    @classmethod
    def create(cls) -> SimulatorBase:
        """Create an instance of the Vivado simulator."""
        return Vivado()

    def compile(self, config: Configuration) -> RunResults:
        """
        Compile VHDL source using Vivado compiler.

        Args:
            config (Configuration): Configuration data for compile.
        """
        # Create the directory
        if not os.path.isdir('VHDLTest.out/Vivado'):
            os.makedirs('VHDLTest.out/Vivado')

        # Write the compile script
        with open('VHDLTest.out/Vivado/compile.do', 'w') as stream:
            stream.write('-2008\n')
            stream.write('-nolog\n')
            stream.write('-work work\n')
            for file in config.files:
                stream.write(f'{os.path.join("../..", file)}\n')

        # Run the compile
        return RunResults.run([
            f'{self._path}/xvhdl',
            '-file',
            'compile.do'],
            Vivado.compile_rules,
            shell=True,
            cwd='VHDLTest.out/Vivado')

    def test(self, config: Configuration, test: str) -> RunResults:
        """
        Execute a test-bench using Vivado simulator.

        Args:
            config (Configuration): Configuration data for test.
            test (str): Name of test-bench.
        """
        # Write the test script
        with open('VHDLTest.out/Vivado/test.do', 'w') as stream:
            stream.write('-nolog\n')
            stream.write('-standalone\n')
            stream.write('-runall\n')
            stream.write(f'{test}\n')

        # Run the test
        return RunResults.run([
            f'{self._path}/xelab',
            '-file',
            'test.do'],
            Vivado.test_rules,
            shell=True,
            cwd='VHDLTest.out/Vivado')
