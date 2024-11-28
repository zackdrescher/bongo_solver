"""Contains the LetterTile class."""

from __future__ import annotations

from .letter import Letter
from .letter_scores import try_get_letter_score


class LetterTile:
    """A class to represent a letter tile in Bongo."""

    def __init__(self, letter: str | Letter) -> None:
        """Initialize the letter tile with a single character."""
        if isinstance(letter, str):
            letter = Letter(letter)

        self.letter = letter
        self.score = try_get_letter_score(letter)

    def __repr__(self) -> str:
        """Return a string representation of the letter tile."""
        return f"{self.__class__.__name__}({self.letter}, {self.score})"

    def __str__(self) -> str:
        """Return a string representation of the letter tile."""
        return f"{self.letter}({self.score})"
