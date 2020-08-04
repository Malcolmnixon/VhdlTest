.. about:

What is VHDLTest?
=================

VHDLTest is an open source unit test runner for VHDL released under the terms
of the MIT License. It allows for continuous-integration and automated-testing
of VHDL code.

Main Features
-------------

- Python test suite runner configured by a simple YAML file.
- Logging to console and optional log file.
- Optional generation of JUnit test result file.
- Runs standard testbench files without need for modification.

Requirements
------------

VHDLTest depends on a number of components listed below.

Python
******

- Python 3.5 or higher

Simulators
**********

- Aldec Active-HDL
  - Tested with Active-HDL 10.5
  
- GHDL
  - Tested with 0.37 mcode