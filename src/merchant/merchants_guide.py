"""Merchant's guide to the galaxy."""
from __future__ import annotations

from typing import Optional

from merchant import roman_numeral


class Guide:
    """Class for storing transmitted information and answering queries about the intergalactic market."""

    def __init__(self):
        """Set up empty dictionaries for information storage."""
        self.numbers: dict[str, str] = {}
        # self.prices assigns to each tuple (material,currency) a price in units of currency per material
        self.prices: dict[tuple[str, str], float] = {}

    def _list_to_number(self, words: list[str], empty_list_is_one: bool = False) -> int:
        """Convert a list of number words into a valid roman numeral.

        The default return value for an empty list of words is 0.
        If empty_list_is_one is set to True 1 is returned instead.
        Raises KeyError when encountering an unknown word.
        Passes a ValueError if the roman numeral is not correct.
        """
        if empty_list_is_one and len(words) == 0:
            return 1
        letters = map(self.numbers.__getitem__, [w.lower() for w in words])
        return roman_numeral.convert("".join(letters))

    def _parse_number_definition(self, words: list[str]) -> None:
        """Save the number assignment from the statement '<numeral word> is [IVXLCDM]'.

        Raises AssertionError if the second word differs from `is`
        or the last word is not a valid letter.
        """
        assert words[1] == "is"
        assert len(words[2]) == 1
        assert words[2] in "IVXLCDMivxlcdm"
        self.numbers[words[0].lower()] = words[2].upper()
        return None

    def _parse_price_definition(self, words: list[str]) -> None:
        """Save the price assignment from the statement '<numeral word>* <material> is <number> <currency>'.

        Saves the price for a single unit of material if no numeral-words are supplied.
        Raises AssertionError if the sentence is too short
        or does not contain the word `is` in the correct location.
        Raises ValueError if second-to-last word can not be parsed into a number
        or the numeral words do not correspond to a valid roman numeral.
        """
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

    def _parse_number_query(self, words: list[str]) -> str:
        """Answer the correct number for the query 'how much is <numeral-word>* ?'.

        Returns 0 if no numeral-words are supplied.
        Raises AssertionError if the sentence is too short.
        Raises KeyError if the used number-words are not known.
        Raises ValueError if the numeral words do not correspond to a valid roman numeral.
        """
        assert len(words) >= 4
        number_words = words[3:-1]
        result = self._list_to_number(number_words)
        return f"{' '.join(number_words)} is {result}"

    def _parse_price_query(self, words: list[str]) -> str:
        """Answer the correct price for the query 'how many <currency> is <numeral-word>* <material> ?'.

        Returns the price of a single unit of material if no numeral-words are supplied.
        Raises AssertionError if the sentence is too short or does not contain the correct keywords.
        Passes ValueError if the numeral words do not correspond to a valid roman numeral.
        Raises KeyError if the price of the material in that currency is not known.
        """
        assert words[:2] == ["how", "many"]
        assert words[3] == "is"
        assert len(words) >= 6
        currency = words[2]
        material = words[-2]
        number_words = words[4:-2]
        price = self.prices[
            (material.lower(), currency.lower())
        ] * self._list_to_number(number_words, True)
        return f"{' '.join(number_words)} {material} is {price} {currency}"

    def consume(self, line: str) -> Optional[str]:
        """Try to consume a single message by storing the given information or answering the query.

        Inform about malformed input otherwise.
        """
        words = line.split(" ")
        try:
            if words[-1] == "?":
                if line.lower().startswith("how much is "):
                    return self._parse_number_query(words)
                else:
                    return self._parse_price_query(words)
            else:
                if len(words) == 3:
                    self._parse_number_definition(words)
                    return None
                else:
                    self._parse_price_definition(words)
                    return None
        except (AssertionError, KeyError, ValueError):
            return "I have no idea what you are talking about"
