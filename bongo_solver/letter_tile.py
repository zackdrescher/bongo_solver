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

        self.__letter = letter
        self.__score = try_get_letter_score(letter)

    @property
    def letter(self) -> Letter:
        """Return the letter of the tile."""
        return self.__letter

    @property
    def score(self) -> int:
        """Return the point value of the tile."""
        return self.__score

    def __repr__(self) -> str:
        """Return a string representation of the letter tile."""
        return f"{self.__class__.__name__}({self.letter}, {self.__score})"

    def __str__(self) -> str:
        """Return a string representation of the letter tile."""
        return f"{self.letter}({self.__score})"

    def __eq__(self, value: object) -> bool:
        """Check if object is equal to this letter tile."""
        if not isinstance(value, LetterTile):
            return False

        return self.letter == value.letter and self.score == value.score
