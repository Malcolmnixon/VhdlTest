"""Tests for Active-HDL output parsing."""

from VHDLTest.simulator.ActiveHDL import ActiveHDL
from VHDLTest.runner.RunResults import RunResults
from VHDLTest.runner.RunResults import RunCategory


activehdl_compile_patterns = [
    (RunCategory.TEXT, 'some simple text'),
    (RunCategory.ERROR, "Error: COMP96_0015: xxx.vhd : (46, 14): ';' expected.")
]

activehdl_test_patterns = [
    (RunCategory.TEXT, 'some simple text'),
    (RunCategory.TEXT, 'KERNEL: Warning: You are using the Active-HDL Lattice Edition. The performance of simulation'),
    (RunCategory.TEXT, 'KERNEL: Warning: Contact Aldec for available upgrade options - sales@aldec.com.'),
    (RunCategory.INFO, 'EXECUTION:: NOTE   : Report note'),
    (RunCategory.WARNING, 'EXECUTION:: WARNING: Report warning'),
    (RunCategory.ERROR, 'EXECUTION:: ERROR  : Report error'),
    (RunCategory.ERROR, 'EXECUTION:: FAILURE: Report failure'),
    (RunCategory.INFO, 'EXECUTION:: NOTE   : Assert note'),
    (RunCategory.WARNING, 'EXECUTION:: WARNING: Assert warning'),
    (RunCategory.ERROR, 'EXECUTION:: ERROR  : Assert error'),
    (RunCategory.ERROR, 'EXECUTION:: FAILURE: Assert failure'),
    (RunCategory.WARNING, 'KERNEL: WARNING: NUMERIC_STD."=": metavalue detected, returning FALSE'),
    (RunCategory.ERROR, 'RUNTIME: Fatal Error: RUNTIME_0048 xxx.vhd (49): Cannot open file "missing_file.txt"'),
    (RunCategory.ERROR, 'VSIM: Error: Fatal error occurred during simulation.')
]


def test_activehdl_compile_rules() -> None:
    """Test parsing ActiveHDL compile output."""
    # Get the count, categories, and lines of the test input
    count = len(activehdl_compile_patterns)
    categories, lines = zip(*activehdl_compile_patterns)

    # Get lines as single string
    text = '\n'.join(lines)

    # Parse the text using the Active-HDL compile rules
    results = RunResults(None, 1.0, 0, text, ActiveHDL.compile_rules)

    assert len(results.lines) == count
    for i in range(count):
        assert results.lines[i].category == categories[i]
        assert results.lines[i].text == lines[i]


def test_activehdl_test_rules() -> None:
    """Test parsing ActiveHDL test output."""
    # Get the count, categories, and lines of the test input
    count = len(activehdl_test_patterns)
    categories, lines = zip(*activehdl_test_patterns)

    # Get lines as single string
    text = '\n'.join(lines)

    # Parse the text using the Active-HDL test rules
    results = RunResults(None, 1.0, 0, text, ActiveHDL.test_rules)

    assert len(results.lines) == count
    for i in range(count):
        assert results.lines[i].category == categories[i]
        assert results.lines[i].text == lines[i]
