from .SimulatorInterface import SimulatorInterface
from .ActiveHDL import ActiveHDL
from .GHDL import GHDL

class SimulatorFactory(object):
    """
    Factory for VHDL simulators
    """
    
    @staticmethod
    def simulator_list():
        """Returns the list of supported simulators."""
        return [
            ActiveHDL,
            GHDL
        ]
        
    @staticmethod
    def available_simulators():
        """Returns the list of available simulators."""
        return [sim for sim in SimulatorFactory.simulator_list() if sim.is_available()]
        
    @staticmethod
    def create_simulator() -> SimulatorInterface:
        """Creates a simulator if available."""
        
        # Get the list of available simulators and return None if none available
        available = SimulatorFactory.available_simulators()
        if not available:
            return None
            
        # Create an instance of the first available simulator
        return available[0]()
        