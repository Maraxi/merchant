import subprocess

import pytest

from merchant import guide


def test_true():
    assert guide.true() is True


@pytest.mark.xfail(reason="not implemented yet")
def test_input():
    p = subprocess.run(
        ["python", "-m", "merchant", "tests/samples/input1.txt"],
        capture_output=True,
        text=True,
    )
    assert "Gold is 57800 Credits" in p.stdout
