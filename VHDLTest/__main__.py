#!/usr/bin/env python

import argparse
import sys
from datetime import datetime
from .simulator.SimulatorFactory import SimulatorFactory
from .Configuration import Configuration
from .logger.Log import Log


def main() -> None:
    """VHDL Testbench Runner application entry point"""

    # Construct the argument parser
    parser = argparse.ArgumentParser(
        prog='VHDL Testbench Runner (VHDLTest)',
        description='''Runs VHDL Testbenches and generates a report of the
                     passes and failures. Reference documentation is located
                     at https://github.com/Malcolmnixon/VhdlTest''')
    parser.add_argument('-c', '--config', help='Configuration file')
    parser.add_argument('-l', '--log', help='Log file')
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

    # Construct the logger
    log = Log()
    if args.log is not None:
        log.add_log_file(args.log)

    # Print the banner and capture the start time
    log.write('VHDL Testbench Runner (VHDLTest)\n\n')
    elapsed_start = datetime.now()

    # Read the configuration
    config = Configuration(args.config)

    # Create a simulator
    simulator = SimulatorFactory.create_simulator()
    if simulator is None:
        log.write(Log.error,
                  'Error: No simulator installed. Please add a simulator to the path',
                  Log.end,
                  '\n')
        sys.exit(1)

    # Compile the code
    log.write(f'Compiling files using {simulator.name}...\n')
    compile_result = simulator.compile(config)
    if compile_result.any_errors:
        log.write(Log.error,
                  'Error: Compile of VHDL code failed',
                  log.end,
                  '\n\n')
        compile_result.print(log)
        sys.exit(1)

    # Report compile success
    log.write(Log.success, 'done', Log.end, '\n\n')

    # Run the tests
    results = {}
    for test in config.tests:
        # Log starting the test
        log.write(f'Starting {test}\n')

        # Run the test and save the result
        result = simulator.test(config, test)
        results[test] = result

        # Log the result
        if result.any_errors:
            log.write(Log.error, 'fail ', Log.end, f'{test} ({result.duration:.1f} seconds)\n\n')
            result.print(log)
        else:
            log.write(Log.success, 'pass ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')

        # Add separator after test
        log.write('\n')

    # Print summary list
    log.write('==== Summary ========================================\n')
    total_count = len(config.tests)
    total_passed = 0
    total_failed = 0
    total_duration = 0.0
    for test in config.tests:
        result = results[test]
        total_duration += result.duration
        if result.any_errors:
            log.write(Log.error, 'fail ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
            total_failed = total_failed + 1
        else:
            log.write(Log.success, 'pass ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
            total_passed = total_passed + 1

    # Print summary statistics
    log.write('=====================================================\n')
    if total_count == 0:
        log.write(Log.warning, 'No tests were run!', Log.end, '\n')
    if total_passed != 0:
        log.write(Log.success, 'pass ', Log.end, f'{total_passed} of {total_count}\n')
    if total_failed != 0:
        log.write(Log.error, 'fail ', Log.end, f'{total_failed} of {total_count}\n')

    # Print time information
    elapsed_end = datetime.now()
    elapsed_duration = (elapsed_end - elapsed_start).total_seconds()
    log.write('=====================================================\n')
    log.write(f'Total time was {total_duration:.1f} seconds\n')
    log.write(f'Elapsed time was {elapsed_duration:.1f} seconds\n')
    log.write('=====================================================\n')

    # Print final warning if any failed
    if total_failed != 0:
        log.write(Log.error, 'Some failed!', Log.end, '\n')


if __name__ == '__main__':
    main()
