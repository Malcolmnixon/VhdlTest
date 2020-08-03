import os
import shutil
from .SimulatorInterface import SimulatorInterface
from .SimulatorResults import SimulatorResults
from .SimulatorResults import ResultLineType
from ..Configuration import Configuration


class GHDL(SimulatorInterface):
    """
    GHDL Simulator class.
    """

    """Result parse rules."""
    rules = [
        (r".*:\d+:\d+: ", ResultLineType.error),
        (r".*:\(assertion note\):", ResultLineType.execution_note),
        (r".*:\(report note\):", ResultLineType.execution_note),
        (r".*:\(assertion warning\):", ResultLineType.execution_warning),
        (r".*:\(report warning\):", ResultLineType.execution_warning),
        (r".*:\(assertion error\):", ResultLineType.execution_error),
        (r".*:\(report error\):", ResultLineType.execution_error),
        (r".*:\(assertion failure\):", ResultLineType.execution_failure),
        (r".*:\(report failure\):", ResultLineType.execution_failure)
    ]

    def __init__(self):
        """GHDL Simulator constructor."""
        super().__init__('GHDL')

    @classmethod
    def find_path(cls) -> str:
        # Find ghdl executable
        ghdl_path = shutil.which('ghdl')
        if ghdl_path is None:
            return None

        # Return directory name
        return os.path.dirname(ghdl_path)

    def compile(self, config: Configuration) -> SimulatorResults:
        # Create the directory
        if not os.path.isdir('VHDLTest.out/GHDL'):
            os.makedirs('VHDLTest.out/GHDL')

        # Write the compile response file
        with open('VHDLTest.out/GHDL/compile.rsp', 'w') as stream:
            for file in config.files:
                stream.write(f'{file}\n')

        # Run the compile
        return SimulatorInterface.run_process([
            'ghdl',
            '-a',
            '--std=08',
            '--workdir=VHDLTest.out/GHDL',
            '@VHDLTest.out/GHDL/compile.rsp'
            ],
            GHDL.rules)

    def test(self, config: Configuration, test: str) -> SimulatorResults:
        # Run the test
        return SimulatorInterface.run_process([
            'ghdl',
            '-r',
            '--std=08',
            '--workdir=VHDLTest.out/GHDL',
            test],
            GHDL.rules)
