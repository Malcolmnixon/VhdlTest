import pytest
from VHDLTest.Configuration import Configuration

def test_load_missing():
    """
    Test that loading a missing configuration generates a RuntimeError.
    """
    with pytest.raises(RuntimeError):
        conf = Configuration('tests/configurations/missing.yaml')
        assert conf == None
    
def test_load_empty():
    """
    Test that loading an empty configuration works but provides no files or tests.
    """
    conf = Configuration('tests/configurations/empty.yaml')
    assert conf != None
    assert len(conf.files) == 0
    assert len(conf.tests) == 0
    
def test_load_valid():
    """
    Test that loading a valid configuration provides the files and tests.
    """
    conf = Configuration('tests/configurations/valid.yaml')
    assert conf != None
    assert len(conf.files) == 2
    assert 'file1.vhd' in conf.files
    assert 'file2.vhd' in conf.files
    assert len(conf.tests) == 2
    assert 'file1_tb' in conf.tests
    assert 'file2_tb' in conf.tests
