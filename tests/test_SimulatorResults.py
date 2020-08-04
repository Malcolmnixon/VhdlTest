from datetime import datetime
from VHDLTest.simulator.SimulatorResults import SimulatorResults
from VHDLTest.simulator.SimulatorResults import ResultLineType


def append_output() -> None:
    now = datetime.now()
    res = SimulatorResults(now, 1.2, 3, ['Hello', 'World'], [])
    assert res is not None
    assert res.start == now
    assert res.duration == 1.2
    assert res.returncode == 3
    assert len(res.lines) == 2
    assert res.lines[0].line_type == ResultLineType.text
    assert res.lines[0].text == 'Hello'
    assert res.lines[1].line_type == ResultLineType.text
    assert res.lines[1].text == 'World'
