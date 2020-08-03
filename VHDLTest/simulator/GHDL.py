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
        if ghdl_path is None:
            return None

        # Return directory name
        return os.path.dirname(ghdl_path)

    def compile(self, config: Configuration):
        # Create the directory
        if not os.path.isdir('VHDLTest.out/GHDL'):
            os.makedirs('VHDLTest.out/GHDL')

        # Write the compile response file
        with open('VHDLTest.out/GHDL/compile.rsp', 'w') as stream:
            for file in config.files:
                stream.write(f'{file}\n')

        # Run the compile (analysis)
        subprocess.run([
            'ghdl',
            '-a',
            '--std=08',
            '--work work',
            '--workdir=VHDLTest.out/GHDL',
            '@VHDLTest.out/GHDL/compile.rsp'
        ])

    def test(self, config: Configuration, test: str):
        # Run the test
        subprocess.run([
            'ghdl',
            '-r',
            '--std=08',
            '--work work',
            '--workdir=VHDLTest.out/GHDL',
            test
        ])
