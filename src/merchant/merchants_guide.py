"""Merchant's guide to the galaxy."""
from typing import Optional

from merchant import roman_numeral


class Guide:
    """Class for storing transmitted information and answering queries about the intergalactic market."""

    def __init__(self):
        """Set up empty dictionaries for information storage."""
        self.numbers: dict[str, str] = {}
        # self.prices assigns to each tupple (material,currency) a price in units of currency per material
        self.prices: dict[tuple[str, str], float] = {}

    def _list_to_number(self, words: list[str], empty_list_is_one: bool = False) -> int:
        """Convert a list of number words into a valid roman numeral.

        The default return value for an empty list of words is 0.
        If empty_list_is_one is set to True 1 is returned instead.
        Raises KeyError when encountering an unknown word.
        """
        if empty_list_is_one and len(words) == 0:
            return 1
        letters = map(self.numbers.__getitem__, words)
        return roman_numeral.convert("".join(letters))

    def consume(self, line: str) -> Optional[str]:
        """Try to consume a single message by storing the given information or answering the query.

        Inform about malformed input otherwise.
        """
        words = line.split(" ")
        try:
            if len(words) == 3:
                # number assignment
                assert words[1] == "is"
                assert len(words[2]) == 1
                assert words[2] in "IVXLCDMivxlcdm"
                self.numbers[words[0]] = words[2].upper()
                return None
            elif words[-1] == "?":
                # query
                assert words.count("is") == 1
                index = words.index("is")
                if index == 2 and line.lower().startswith("how much is "):
                    assert len(words) >= 4
                    number_words = words[3:-1]
                    result = self._list_to_number(number_words)
                    return f"{' '.join(number_words)} is {result}"
                else:
                    assert index == 3
                    assert len(words) >= 6
                    assert line.lower().startswith("how much ")
                    currency = words[2]
                    material = words[-2]
                    number_words = words[4:-2]
                    price = self.prices[
                        (material.lower(), currency.lower())
                    ] * self._list_to_number(number_words, True)
                    return f"{' '.join(number_words)} {material} is {price} {currency}"
            else:
                # price assignment
                assert len(words) >= 4
                number_words = words[:-4]
                material = words[-4].lower()
                assert words[-3] == "is"
                number = float(words[-2])
                currency = words[-1].lower()
                self.prices[(material, currency)] = number / self._list_to_number(
                    number_words, True
                )
                return None
        except (AssertionError, KeyError, ValueError):
            return "I have no idea what you are talking about"
