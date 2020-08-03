import os
import shutil
import subprocess
from .SimulatorInterface import SimulatorInterface
from ..Configuration import Configuration


class ActiveHDL(SimulatorInterface):
    """
    ActiveHDL Simulator class.
    """

    def __init__(self):
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

    def run(self, config: Configuration):
        # Create the directory
        if not os.path.isdir('VHDLTest.out/ActiveHDL'):
            os.makedirs('VHDLTest.out/ActiveHDL')

        # Write the 'do' file
        with open('VHDLTest.out/ActiveHDL/work.do', 'w') as stream:
            stream.write('onerror {exit -code 1}\n')
            stream.write('alib work VHDLTest.out/ActiveHDL\n')
            stream.write('set worklib work\n')
            for file in config.files:
                stream.write(f'acom -2008 -dbg {file}\n')
            for test in config.tests:
                stream.write(f'asim {test}\n')
                stream.write('run -all\n')
                stream.write('endsim\n')
            stream.write('exit -code 0\n')

        # Run the script
        subprocess.run(['vsimsa', '-do', 'VHDLTest.out/ActiveHDL/work.do'])
