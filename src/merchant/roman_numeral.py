"""Converter for roman numerals to int."""
import re
from typing import Final

"""Translations to find the base 10 digits for the thousands, hundreds, tens or unit-blocks of a roman numeral.

The digit is given by the index inside the corresponding tuple.
"""
LETTERS: Final = (
    ("", "M", "MM", "MMM"),
    ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"),
    ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"),
    ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),
)

"""Compiled regular expressions to find the end of thousands, hundreds, tens and units sections of a roman numeral.

Thousands contains only `M` so the first other letter or end of line marks the end of the thousands block.
Other blocks work the same except for the different admissible letters.
"""
BOUNDARY_FINDER: Final = (
    re.compile(r"[^M]|$"),
    re.compile(r"[^MDC]|$"),
    re.compile(r"[^CLX]|$"),
    re.compile(r"$"),
)


def convert(string: str) -> int:
    """Calculate the corresponding integer for a given roman numeral.

    Raises `ValueError` if the string does not represent a valid roman numeral.
    """
    sum = 0
    start = 0

    for regex, values in zip(BOUNDARY_FINDER, LETTERS):
        sum *= 10
        match = regex.search(string, start)
        assert match is not None
        end = match.start()
        sum += values.index(string[start:end])
        start = end

    return sum
