"""Merchant's guide to the galaxy."""
from typing import Optional


class Guide:
    """Class for storing transmitted information and answering queries about the intergalactic market."""

    def consume(self, line: str) -> Optional[str]:
        """Consume a single message and store the given information or answer the query."""
        print(line)
        return ""
