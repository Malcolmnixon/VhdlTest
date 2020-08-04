![CI/Test](https://github.com/Malcolmnixon/VhdlTest/workflows/CI/Test/badge.svg) [![Documentation Status](https://readthedocs.org/projects/vhdltest/badge/?version=latest)](https://vhdltest.readthedocs.io/en/latest/?badge=latest)

# VHDL Testbench Runner
This python module runs VHDL testbenches and generates a report of the results.

It requires a VHDL Simulator be installed on the system. Supported simulators are:
- [GHDL](http://ghdl.free.fr/)
- [Aldec Active-HDL](https://www.aldec.com/en/products/fpga_simulation/active-hdl)

# Installation
VHDL Testbench Runner can be installed by running:
```
python -m pip install VHDLTest
```

# Configuring
VHDL Testbench Runner requires a yaml configuration file to specify the project.

# Running
VHDL Testbench Runner can be run by;
```
python -m VHDLTest -c config.yaml
```
