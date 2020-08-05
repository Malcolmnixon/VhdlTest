import os
import shutil
from .SimulatorInterface import SimulatorInterface
from ..runner.RunResults import RunCategory
from ..runner.RunResults import RunResults
from ..Configuration import Configuration


class GHDL(SimulatorInterface):
    """
    GHDL Simulator class.
    """

    """Compile results parse rules."""
    compile_rules = [
        (r".*:\d+:\d+: ", RunCategory.ERROR),
        (r".*:error:", RunCategory.ERROR)
    ]

    """Test results parse rules."""
    test_rules = [
        (r".*:\(assertion note\):", RunCategory.INFO),
        (r".*:\(report note\):", RunCategory.INFO),
        (r".*:\(assertion warning\):", RunCategory.WARNING),
        (r".*:\(report warning\):", RunCategory.WARNING),
        (r".*:\(assertion error\):", RunCategory.ERROR),
        (r".*:\(report error\):", RunCategory.ERROR),
        (r".*:\(assertion failure\):", RunCategory.ERROR),
        (r".*:\(report failure\):", RunCategory.ERROR),
        (r".*:error:", RunCategory.ERROR)
    ]

    def __init__(self) -> None:
        """GHDL Simulator constructor."""
        super().__init__('GHDL')

    @classmethod
    def find_path(cls) -> str:
        # First check environment variable
        path = os.getenv('VHDLTEST_GHDL_PATH')
        if path is not None:
            return path

        # Find ghdl executable
        path = shutil.which('ghdl')
        if path is None:
            return None

        # Return directory name
        return os.path.dirname(path)

    def compile(self, config: Configuration) -> RunResults:
        # Create the directory
        if not os.path.isdir('VHDLTest.out/GHDL'):
            os.makedirs('VHDLTest.out/GHDL')

        # Write the compile response file
        with open('VHDLTest.out/GHDL/compile.rsp', 'w') as stream:
            for file in config.files:
                stream.write(f'{file}\n')

        # Run the compile
        return RunResults.run([
            f'{self._path}/ghdl',
            '-a',
            '--std=08',
            '--workdir=VHDLTest.out/GHDL',
            '@VHDLTest.out/GHDL/compile.rsp'],
            GHDL.compile_rules)

    def test(self, config: Configuration, test: str) -> RunResults:
        # Run the test
        return RunResults.run([
            f'{self._path}/ghdl',
            '-r',
            '--std=08',
            '--workdir=VHDLTest.out/GHDL',
            test],
            GHDL.test_rules)
