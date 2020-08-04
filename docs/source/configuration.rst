.. configuration:

Configuration
=============

VHDLTest is configured using a YAML configuration file. This file contains the
following information:
- List of the VHDL files to compile
- List of the test-benches to run

Example Configuration
---------------------

The following is an example configuration file:

.. code-block:: yaml

   files:
    - full_adder.vhd
    - full_adder_pass_tb.vhd
    - full_adder_fail_tb.vhd
    - half_adder.vhd
    - half_adder_pass_tb.vhd
    - half_adder_fail_tb.vhd
   
   tests:
    - full_adder_pass_tb
    - full_adder_fail_tb
    - half_adder_pass_tb
    - half_adder_fail_tb

