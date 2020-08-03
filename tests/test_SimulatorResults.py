from VHDLTest.simulator.SimulatorResults import SimulatorResults
from VHDLTest.simulator.SimulatorResults import ResultLineType


def test_empty_results():
    res = SimulatorResults()
    assert res is not None
    assert len(res.lines) == 0


def append_output():
    res = SimulatorResults()
    assert res is not None
    assert len(res.lines) == 0
    res.append_results(['Hello', 'World'], [])
    assert len(res.lines) == 2
    assert res.lines[0].line_type == ResultLineType.text
    assert res.lines[0].text == 'Hello'
    assert res.lines[1].line_type == ResultLineType.text
    assert res.lines[1].text == 'World'
