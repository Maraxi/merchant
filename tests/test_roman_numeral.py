"""Tester for roman numeral conversion."""
import pytest

from merchant import roman_numeral


@pytest.mark.parametrize(
    "test_input, expected_value",
    (
        ("", 0),
        ("I", 1),
        ("V", 5),
        ("X", 10),
        ("L", 50),
        ("C", 100),
        ("D", 500),
        ("M", 1000),
        ("MMMCMXCIX", 3999),
        ("DV", 505),
        ("MMCDLXXXVII", 2487),
        ("MCXI", 1111),
        ("XLIV", 44),
        ("CCCXC", 390),
    ),
)
def test_valid_input(test_input, expected_value):
    """Test valid inputs containing zero, one or a combination of letters."""
    assert roman_numeral.convert(test_input) == expected_value


@pytest.mark.parametrize(
    "test_input",
    (
        "m",
        "v",
        "E",
        "23",
        ".",
        "MCSI",
    ),
)
def test_unknown_input(test_input):
    """Test invalid inputs such as lower case and undefined letters aswell as numbers and symbols."""
    with pytest.raises(ValueError):
        roman_numeral.convert(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "VX",
        "VC",
        "LC",
        "DM",
        "IL",
        "IM",
        "IC",
        "XD",
    ),
)
def test_invalid_ordering(test_input):
    """Test invalid combinations/orders of letters."""
    with pytest.raises(ValueError):
        roman_numeral.convert(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "IIII",
        "VV",
        "XXXX",
        "LL",
        "CCCC",
        "DD",
        "MMMM",
    ),
)
def test_invalid_letter_count(test_input):
    """Test numerals with too many occurances of single letters."""
    with pytest.raises(ValueError):
        roman_numeral.convert(test_input)
