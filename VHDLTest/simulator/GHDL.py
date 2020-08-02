import os
import shutil
from .SimulatorInterface import SimulatorInterface

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
