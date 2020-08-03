import os
import shutil
import subprocess
from .SimulatorInterface import SimulatorInterface
from ..Configuration import Configuration

class GHDL(SimulatorInterface):
    """
    GHDL Simulator class.
    """

    def __init__(self):
        """GHDL Simulator constructor."""
        super().__init__('GHDL')

    @classmethod
    def find_path(cls) -> str:
        # Find ghdl executable
        ghdl_path = shutil.which('ghdl')
        if ghdl_path == None:
            return None
        
        # Return directory name
        return os.path.dirname(ghdl_path)

    def run(self, config: Configuration):
        # Create the directory
        if not os.path.isdir('VHDLTest.out/GHDL'):
            os.makedirs('VHDLTest.out/GHDL')

        # Write the analysis response file
        with open('VHDLTest.out/GHDL/analysis.rsp', 'w') as stream:
            for file in config.files:
                stream.write(f'{file}\n')

        # Run the analysis
        subprocess.run(['ghdl', '-a', '--std=08', '--workdir=VHDLTest.out/GHDL', '@VHDLTest.out/GHDL/analysis.rsp'])
        
        # Run the tests
        for test in config.tests:
            subprocess.run(['ghdl', '-r', '--std=08', '--workdir=VHDLTest.out/GHDL', test])
