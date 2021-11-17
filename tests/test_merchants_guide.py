"""Tester for the merchants guide to the galaxy."""
import subprocess

import pytest

from merchant import merchants_guide


@pytest.fixture
def guide():
    """Supply an empty instance of the guide class."""
    return merchants_guide.Guide()


def test_consume(guide):
    """Test the consume function."""
    assert guide.consume("") == ""


@pytest.mark.xfail(reason="not implemented yet")
def test_input():
    """Run a full test."""
    p = subprocess.run(
        ["python", "-m", "merchant", "tests/samples/input1.txt"],
        capture_output=True,
        text=True,
    )
    assert "Gold is 57800 Credits" in p.stdout
