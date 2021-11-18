"""Tester for the merchants guide to the galaxy."""
import subprocess

import pytest

from merchant import merchants_guide


@pytest.fixture
def guide():
    """Supply an empty instance of Guide."""
    return merchants_guide.Guide()


@pytest.fixture
def guide_with_numbers():
    """Supply an instance of Guide with some defined numbers."""
    guide = merchants_guide.Guide()
    values = (
        ("i", "I"),
        ("v", "V"),
        ("x", "X"),
        ("foo", "L"),
        ("bar", "L"),
        ("foobar", "L"),
        ("Glob", "M"),
    )
    for name, value in values:
        guide._parse_number_definition([name, "is", value])
    return guide


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        (["i"], 1),
        (["foobar"], 50),
        (["foo"], 50),
        (["Glob", "foo", "i", "x"], 1059),
    ],
)
def test_list_to_number(guide_with_numbers, test_input, expected_output):
    """Test the consume function."""
    assert guide_with_numbers._list_to_number(test_input) == expected_output


def test_input():
    """Run a full test."""
    p = subprocess.run(
        ["python", "-m", "merchant", "tests/samples/input1.txt"],
        capture_output=True,
        text=True,
    )
    assert "pish tegj glob glob is 42" in p.stdout
    assert "glob prok Gold is 57800.0 Credits" in p.stdout
    assert (
        "> how much wood could a woodchuck chuck if a woodchuck could chuck wood ?\n\
I have no idea what you are talking about"
        in p.stdout
    )
