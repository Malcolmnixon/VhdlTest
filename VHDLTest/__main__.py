#!/usr/bin/env python

import argparse
import sys
import yaml
from .simulator.SimulatorFactory import SimulatorFactory

def main():
    """VHDL Testbench Runner application entry point"""
    
    # Construct the argument parser
    parser = argparse.ArgumentParser(
        prog='VHDL Testbench Runner (VHDLTest)',
        description='''Runs VHDL Testbenches and generates a report of the
                     passes and failures. Reference documentation is located
                     at https://github.com/Malcolmnixon/VhdlTest''')
    parser.add_argument('-c', '--config', help='Configuration file')
    parser.add_argument('-v', '--version', default=False, action='store_true', help='Display version information')

    # If no arguments are provided then print the help information
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    # Parse the arguments
    args = parser.parse_args()
                     
    # Check for version
    if args.version:
        print('VHDL Testbench Runner (VHDLTest) version 0.0.1')
        sys.exit(0)
        
    # Ensure we have a configuration
    if args.config == None:
        parser.print_help()
        sys.exit(1)

    # Create a simulator
    simulator = SimulatorFactory.create_simulator()
    if simulator == None:
        print('No simulator installed. Please add a simulator to the path')
        sys.exit(1)
    
    # Print simulator name
    print('VHDL Testbench Runner')
    print(f'  Using {simulator.name} simulator.')

if __name__ == '__main__':
    main()
