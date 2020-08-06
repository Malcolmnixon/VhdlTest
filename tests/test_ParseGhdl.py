"""Tests for GHDL output parsing."""

from VHDLTest.simulator.GHDL import GHDL
from VHDLTest.runner.RunResults import RunResults
from VHDLTest.runner.RunResults import RunCategory


ghdl_compile_patterns = [
    (RunCategory.TEXT, "some simple text"),
    (RunCategory.WARNING, "some_file.vhd:12:34:warning: comparing non-numeric vector is unexpected"),
    (RunCategory.ERROR, "some_file.vhd:23:45:error: unhandled function: "),
    (RunCategory.ERROR, "full_adder.vhd:25:18: ';' expected at end of signal assignment"),
    (RunCategory.ERROR, "ghdl\\bin\\ghdl.exe: cannot open missing_file.vhd")
]

ghdl_test_patterns = [
    (RunCategory.TEXT, "some simple text"),
    (RunCategory.INFO, "full_adder_pass_tb.vhd:47:9:@10ns:(report note): Report note"),
    (RunCategory.WARNING, "full_adder_pass_tb.vhd:47:9:@10ns:(report warning): Report warning"),
    (RunCategory.ERROR, "full_adder_pass_tb.vhd:47:9:@10ns:(report error): Report error"),
    (RunCategory.ERROR, "full_adder_pass_tb.vhd:47:9:@10ns:(report failure): Report failure"),
    (RunCategory.INFO, "full_adder_pass_tb.vhd:47:9:@10ns:(assertion note): Assert note"),
    (RunCategory.WARNING, "full_adder_pass_tb.vhd:47:9:@10ns:(assertion warning): Assert warning"),
    (RunCategory.ERROR, "full_adder_pass_tb.vhd:47:9:@10ns:(assertion error): Assert error"),
    (RunCategory.ERROR, "full_adder_pass_tb.vhd:47:9:@10ns:(assertion failure): Assert failure"),
    (RunCategory.ERROR, "ghdl\\bin\\ghdl.exe:error: report failed"),
    (RunCategory.ERROR, "ghdl\\bin\\ghdl.exe:error: assertion failed"),
    (RunCategory.ERROR, "ghdl\\bin\\ghdl.exe:error: simulation failed")
]


def test_ghdl_compile_rules() -> None:
    """Test parsing GHDL compile output."""
    # Get the count, categories, and lines of the test input
    count = len(ghdl_compile_patterns)
    categories, lines = zip(*ghdl_compile_patterns)

    # Get lines as single string
    text = '\n'.join(lines)

    # Parse the text using the GHDL compile rules
    results = RunResults(None, 1.0, 0, text, GHDL.compile_rules)

    assert len(results.lines) == count
    for i in range(count):
        assert results.lines[i].category == categories[i]
        assert results.lines[i].text == lines[i]


def test_ghdl_test_rules() -> None:
    """Test parsing GHDL test output."""
    # Get the count, categories, and lines of the test input
    count = len(ghdl_test_patterns)
    categories, lines = zip(*ghdl_test_patterns)

    # Get lines as single string
    text = '\n'.join(lines)

    # Parse the text using the GHDL test rules
    results = RunResults(None, 1.0, 0, text, GHDL.test_rules)

    assert len(results.lines) == count
    for i in range(count):
        assert results.lines[i].category == categories[i]
        assert results.lines[i].text == lines[i]
