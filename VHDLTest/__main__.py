#!/usr/bin/env python

import argparse
import sys
from .simulator.SimulatorFactory import SimulatorFactory
from .Configuration import Configuration


def main() -> None:
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
    if args.config is None:
        parser.print_help()
        sys.exit(1)

    # Print the banner
    print('VHDL Testbench Runner (VHDLTest)')

    # Read the configuration
    config = Configuration(args.config)

    # Create a simulator
    simulator = SimulatorFactory.create_simulator()
    if simulator is None:
        print('  Error: No simulator installed. Please add a simulator to the path')
        sys.exit(1)

    # Print simulator name
    print(f'  Using {simulator.name} simulator.')

    # Compile the code
    compile_result = simulator.compile(config)
    if compile_result.any_errors:
        print('  Error: Compile of VHDL code failed')
        compile_result.print()
        sys.exit(1)

    # Run all tests
    test_results = simulator.test_all(config)
    print('  Test results:')
    passed = 0
    for (name, result) in test_results:
        if result.any_errors:
            print(f'    fail: {name}')
        else:
            print(f'    pass: {name}')
            passed = passed + 1

    # Print summary
    print(f'  Passed {passed} of {len(test_results)} tests')


if __name__ == '__main__':
    main()
