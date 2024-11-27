"""Class for storing a set of valid bongo words."""

from __future__ import annotations

from pathlib import Path


class BongoDictionary:
    """Class for storing a set of valid bongo words."""

    @classmethod
    def from_text_file(cls, file_path: str | Path) -> BongoDictionary:
        """Initialize a dictionary with a set of words from a text file."""
        if isinstance(file_path, str):
            file_path = Path(file_path)

        with file_path.open() as file:
            words = file.read().splitlines()
        return cls(words)

    def __init__(self, words: set[str] | list[str]) -> None:
        """Initialize the dictionary with a set of valid bongo words."""
        if isinstance(words, list):
            words = set(words)
        self.words = words
