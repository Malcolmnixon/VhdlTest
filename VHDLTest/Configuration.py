import sys
import os
import yaml

class Configuration(object):
    """YAML configuration class."""
    
    def __init__(self, filename: str):
        """
        Configuration constructor.
        
        Args:
            filename (str): YAML configuration file name.
        """
        
        # Fail if file doesn't exist
        if not os.path.isfile(filename):
            print('VHDL Testbench Runner (VHDLTest)')
            print(f'  Error: Configuration file {filename} not found.')
            sys.exit(1)
        
        # Load the configuration file contents
        with open(filename, 'r') as stream:
            contents = stream.read()
            
        # Parse the configuration file contents
        self._doc = yaml.load(contents, Loader=yaml.SafeLoader)

    @property
    def files(self):
        """
        Gets the files mentioned in the configuration.
        """
        return self._doc['files']

    @property
    def tests(self):
        """
        Gets the tests mentioned in the configuration.
        """
        return self._doc['tests']
