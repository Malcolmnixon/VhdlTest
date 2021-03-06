"""Tests for python configuration parsing."""

import pytest
from VHDLTest.Configuration import Configuration


def test_load_missing() -> None:
    """Test missing configuration."""
    with pytest.raises(RuntimeError):
        Configuration('tests/configurations/missing.yaml')


def test_load_empty() -> None:
    """Test empty configuration."""
    with pytest.raises(RuntimeError):
        Configuration('tests/configurations/empty.yaml')


def test_load_valid() -> None:
    """Test valid configuration and contents."""
    conf = Configuration('tests/configurations/valid.yaml')
    assert conf is not None
    assert len(conf.files) == 2
    assert 'file1.vhd' in conf.files
    assert 'file2.vhd' in conf.files
    assert len(conf.tests) == 2
    assert 'file1_tb' in conf.tests
    assert 'file2_tb' in conf.tests
