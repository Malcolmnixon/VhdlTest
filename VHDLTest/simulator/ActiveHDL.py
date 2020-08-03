import os
import shutil
from .SimulatorInterface import SimulatorInterface
from .SimulatorResults import SimulatorResults
from .SimulatorResults import ResultLineType
from ..Configuration import Configuration


class ActiveHDL(SimulatorInterface):
    """
    ActiveHDL Simulator class.
    """

    """Result parse rules."""
    rules = [
        ("Error: ", ResultLineType.error),
        ("KERNEL: Warning: ", ResultLineType.warning),
        ("EXECUTION:: NOTE", ResultLineType.execution_note),
        ("EXECUTION:: WARNING", ResultLineType.execution_warning),
        ("EXECUTION:: ERROR", ResultLineType.execution_error),
        ("EXECUTION:: FAILURE", ResultLineType.execution_failure)
    ]

    def __init__(self) -> None:
        """ActiveHDL Simulator constructor."""
        super().__init__('ActiveHDL')

    @classmethod
    def find_path(cls) -> str:
        # Find vsimsa executable
        vsimsa_path = shutil.which('vsimsa')
        if vsimsa_path is None:
            return None

        # Return directory name
        return os.path.dirname(vsimsa_path)

    def compile(self, config: Configuration) -> SimulatorResults:
        # Create the directory
        if not os.path.isdir('VHDLTest.out/ActiveHDL'):
            os.makedirs('VHDLTest.out/ActiveHDL')

        # Write the compile script
        with open('VHDLTest.out/ActiveHDL/compile.do', 'w') as stream:
            stream.write('onerror {exit -code 1}\n')
            stream.write('alib work VHDLTest.out/ActiveHDL\n')
            stream.write('set worklib work\n')
            for file in config.files:
                stream.write(f'acom -2008 -dbg {file}\n')

        # Run the compile
        return SimulatorInterface.run_process([
            'vsimsa',
            '-do',
            'VHDLTest.out/ActiveHDL/compile.do'],
            ActiveHDL.rules)

    def test(self, config: Configuration, test: str) -> SimulatorResults:
        # Write the test script
        with open('VHDLTest.out/ActiveHDL/test.do', 'w') as stream:
            stream.write('onerror {exit -code 1}\n')
            stream.write('set worklib work\n')
            stream.write(f'asim {test}\n')
            stream.write('run -all\n')
            stream.write('endsim\n')
            stream.write('exit -code 0\n')

        # Run the test
        return SimulatorInterface.run_process([
            'vsimsa',
            '-do',
            'VHDLTest.out/ActiveHDL/test.do'],
            ActiveHDL.rules)
