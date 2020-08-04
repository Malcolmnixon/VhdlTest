#!/usr/bin/env python

import argparse
import sys
from junit_xml import TestSuite, TestCase
from datetime import datetime
from typing import Dict
from .simulator.SimulatorFactory import SimulatorFactory
from .simulator.SimulatorInterface import SimulatorInterface
from .simulator.SimulatorResults import SimulatorResults
from .Configuration import Configuration
from .logger.Log import Log


def parse_arguments() -> object:
    # Construct the argument parser
    parser = argparse.ArgumentParser(
        prog='VHDL Testbench Runner (VHDLTest)',
        description='''Runs VHDL Testbenches and generates a report of the
                     passes and failures. Reference documentation is located
                     at https://github.com/Malcolmnixon/VhdlTest''')
    parser.add_argument('-c', '--config', help='Configuration file')
    parser.add_argument('-l', '--log', help='Write to log file')
    parser.add_argument('-j', '--junit', help='Generate JUnit xml file')
    parser.add_argument('-v', '--version', default=False, action='store_true', help='Display version information')

    # If no arguments are provided then print the help information
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the arguments
    args = parser.parse_args()

    # Check for version
    if args.version:
        print('VHDL Testbench Runner (VHDLTest) version 0.0.2')
        sys.exit(0)

    # Ensure we have a configuration
    if args.config is None:
        parser.print_help()
        sys.exit(1)

    # Return arguments
    return args


def compile_source(log: Log,
                   config: Configuration,
                   simulator: SimulatorInterface) -> None:
    # Compile the code
    log.write(f'Compiling files using {simulator.name}...\n')
    result = simulator.compile(config)
    if not result.passed:
        log.write(Log.error,
                  'Error: Compile of source files failed',
                  log.end,
                  '\n\n')
        result.print(log)
        sys.exit(1)

    # Report compile success
    log.write(Log.success, 'done', Log.end, '\n\n')


def run_tests(log: Log,
              config: Configuration,
              simulator: SimulatorInterface) -> Dict[str, SimulatorResults]:

    # Run the tests
    results = {}
    for test in config.tests:
        # Log starting the test
        log.write(f'Starting {test}\n')

        # Run the test and save the result
        result = simulator.test(config, test)
        results[test] = result

        # Log the result
        if result.passed:
            log.write(Log.success, 'pass ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
        else:
            log.write(Log.error, 'fail ', Log.end, f'{test} ({result.duration:.1f} seconds)\n\n')
            result.print(log)

        # Add separator after test
        log.write('\n')

    # Return dictionary of results
    return results


def emit_junit(log: Log,
               config: Configuration,
               results: Dict[str, SimulatorResults],
               junit: str) -> None:

    # Print generating message
    log.write(f'Generating JUnit output {junit}\n')

    # Create the test cases
    test_cases = []
    for test in config.tests:
        result = results[test]

        # Create the test case
        test_case = TestCase('all', classname=test, elapsed_sec=result.duration, stdout=result.output)

        # Detect error (test could not run)
        if result.error:
            test_case.add_error_info(message=result.error_message)

        # Detect failure (test ran, but did not pass)
        if result.failure:
            test_case.add_failure_info(output=result.failure_output)

        test_cases.append(test_case)

    # Create the test suite
    test_suite = TestSuite('testsuite', test_cases)

    # Write test suite to file
    with open(junit, 'w') as f:
        TestSuite.to_file(f, [test_suite])

    # Report compile success
    log.write(Log.success, 'done', Log.end, '\n\n')


def print_summary(log: Log,
                  config: Configuration,
                  results: Dict[str, SimulatorResults],
                  elapsed_duration: float) -> bool:

    # Print summary list
    log.write('==== Summary ========================================\n')
    total_count = len(config.tests)
    total_passed = 0
    total_failed = 0
    total_duration = 0.0
    for test in config.tests:
        result = results[test]
        total_duration += result.duration
        if result.passed:
            log.write(Log.success, 'pass ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
            total_passed = total_passed + 1
        else:
            log.write(Log.error, 'fail ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
            total_failed = total_failed + 1

    # Print summary statistics
    log.write('=====================================================\n')
    if total_count == 0:
        log.write(Log.warning, 'No tests were run!', Log.end, '\n')
    if total_passed != 0:
        log.write(Log.success, 'pass ', Log.end, f'{total_passed} of {total_count}\n')
    if total_failed != 0:
        log.write(Log.error, 'fail ', Log.end, f'{total_failed} of {total_count}\n')

    # Print time information
    log.write('=====================================================\n')
    log.write(f'Total time was {total_duration:.1f} seconds\n')
    log.write(f'Elapsed time was {elapsed_duration:.1f} seconds\n')
    log.write('=====================================================\n')

    # Print final warning if any failed
    if total_failed != 0:
        log.write(Log.error, 'Some failed!', Log.end, '\n')

    # Return true if none failed
    return total_failed == 0


def main() -> None:
    """VHDL Testbench Runner application entry point"""

    # Parse arguments
    args = parse_arguments()

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
    compile_source(log, config, simulator)

    # Run the tests
    results = run_tests(log, config, simulator)
    elapsed_end = datetime.now()
    elapsed_duration = (elapsed_end - elapsed_start).total_seconds()

    # Generate JUnit output
    if args.junit is not None:
        emit_junit(log, config, results, args.junit)

    # Print summary list
    passed = print_summary(log, config, results, elapsed_duration)
    if not passed:
        sys.exit(1)


if __name__ == '__main__':
    main()
