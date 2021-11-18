"""Tester for the merchants guide to the galaxy."""
import subprocess
from contextlib import contextmanager

import pytest

from merchant import merchants_guide


@contextmanager
def does_not_raise():
    """No exception may be raised."""
    yield


@pytest.fixture
def guide():
    """Supply an empty instance of Guide."""
    return merchants_guide.Guide()


@pytest.fixture
def guide_with_numbers(guide):
    """Supply an instance of Guide with some defined numbers."""
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


@pytest.fixture
def guide_with_prices(guide_with_numbers):
    """Supply an instance of Guide with some defined numbers and prices."""
    values = (
        (("Silver", "Rocks"), 36.0),
        (("Gold", "Rocks"), 136.0),
        (("Silver", "Coins"), 5.0),
    )
    for pair, value in values:
        guide_with_numbers._parse_price_definition(["i", pair[0], "is", value, pair[1]])
    return guide_with_numbers


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
    """Test the list to number conversion."""
    assert guide_with_numbers._list_to_number(test_input) == expected_output


@pytest.mark.parametrize(
    "test_input, bool, expected_output",
    [
        ([], True, 1),
        ([], False, 0),
    ],
)
def test_list_to_number_empty_list(guide, test_input, bool, expected_output):
    """Test the list to number conversion for empty lists."""
    assert guide._list_to_number(test_input, bool) == expected_output


@pytest.mark.parametrize(
    "test_input, expectation",
    [
        (["foo", "is", "L"], does_not_raise()),
        (["foobar", "bii", "baz"], pytest.raises(AssertionError)),
        (["foo", "is", "Q"], pytest.raises(AssertionError)),
    ],
)
def test_parse_number_definition(guide, test_input, expectation):
    """Test the number parsing."""
    with expectation:
        guide._parse_number_definition(test_input)
        assert len(guide.numbers) > 0


@pytest.mark.parametrize(
    "test_input, expectation",
    [
        (["foo"], pytest.raises(AssertionError)),
        (["glog", "silver", "17", "Coins"], pytest.raises(AssertionError)),
        (["glog", "silver", "is", "17", "Coins"], pytest.raises(KeyError)),
        (["silver", "is", "17", "Coins"], does_not_raise()),
        (["silver", "is", "abc", "Coins"], pytest.raises(ValueError)),
    ],
)
def test_parse_price_definition(guide, test_input, expectation):
    """Test the price parsing."""
    with expectation:
        guide._parse_price_definition(test_input)
        assert len(guide.prices) > 0


@pytest.mark.parametrize(
    "test_input, expected_output, expectation",
    [
        (["how", "much", "is", "?"], "is 0", does_not_raise()),
        (["how", "much", "is", "foo", "?"], "is 50", does_not_raise()),
        (
            ["how", "much", "is", "Glob", "barb", "?"],
            "is 3001",
            pytest.raises(KeyError),
        ),
        (
            ["how", "much", "is", "GLOB", "glob", "Glob", "i", "?"],
            "is 3001",
            does_not_raise(),
        ),
        (["how", "much", "is", "i", "Glob", "?"], "is 3001", pytest.raises(ValueError)),
    ],
)
def test_parse_number_query(
    guide_with_numbers, test_input, expected_output, expectation
):
    """Test the number querying."""
    with expectation:
        assert guide_with_numbers._parse_number_query(test_input).endswith(
            expected_output
        )


@pytest.mark.parametrize(
    "test_input, expected_output, expectation",
    [
        (
            ["how", "many", "Rocks", "is", "Glob", "Gold", "?"],
            "Glob Gold is 136000.0 Rocks",
            does_not_raise(),
        ),
        (
            ["how", "many", "Coins", "is", "Glob", "Gold", "?"],
            "",
            pytest.raises(KeyError),
        ),
        (
            ["how", "much", "Rocks", "is", "Glob", "Gold", "?"],
            "",
            pytest.raises(AssertionError),
        ),
    ],
)
def test_parse_price_query(guide_with_prices, test_input, expected_output, expectation):
    """Test the price querying."""
    with expectation:
        assert guide_with_prices._parse_price_query(test_input) == expected_output


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
