import os
import shutil
from .SimulatorInterface import SimulatorInterface

class ActiveHDL(SimulatorInterface):
    """
    ActiveHDL Simulator class.
    """

    def __init__(self):
        """ActiveHDL Simulator constructor."""
        super().__init__('ActiveHDL')

    @classmethod
    def find_path(cls) -> str:
        # Find vcom executable
        vcom_path = shutil.which('vcom')
        if vcom_path == None:
            return None
        
        # Return directory name
        return os.path.dirname(vcom_path)
