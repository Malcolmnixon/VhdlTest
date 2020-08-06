"""Module for VHDLTest Configuration class."""

from typing import List
import os
import yaml


class Configuration(object):
    """YAML configuration class."""

    def __init__(self, filename: str) -> None:
        """
        Initialize a new Configuration instance.

        Args:
            filename (str): YAML configuration file name.
        """
        # Fail if file doesn't exist
        if not os.path.isfile(filename):
            raise RuntimeError(f'Configuration file {filename} not found.')

        # Load the configuration file contents
        with open(filename, 'r') as stream:
            contents = stream.read()

        # Parse the configuration file contents
        self._doc = yaml.load(contents, Loader=yaml.SafeLoader)

    @property
    def doc(self) -> object:
        """Get the YAML document."""
        return self._doc or {}

    @property
    def files(self) -> List[str]:
        """Get the files mentioned in the configuration."""
        return self.doc.get('files') or []

    @property
    def tests(self) -> List[str]:
        """Get the tests mentioned in the configuration."""
        return self.doc.get('tests') or []
