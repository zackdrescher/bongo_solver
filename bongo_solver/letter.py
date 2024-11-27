"""Provides a class for representing a letter in Bongo."""


class Letter:
    """A class to represent a letter in Bongo."""

    def __init__(self, letter: str) -> None:
        """Initialize the letter with a single character and score."""
        if len(letter) != 1:
            msg = "Letter must be a single character."
            raise ValueError(msg)

        if not letter.isalpha():
            msg = "Letter must be a letter."
            raise ValueError(msg)

        self.letter = letter.upper()

    def __str__(self) -> str:
        """Return the letter as a string."""
        return self.letter

    def __repr__(self) -> str:
        """Return a string representation of the letter."""
        return f"Letter('{self.letter}')"

    def __eq__(self, other: object) -> bool:
        """Return True if the letters are the same."""
        if isinstance(other, Letter):
            return self.letter == other.letter

        if isinstance(other, str):
            return self.letter == other.upper()

        return False
