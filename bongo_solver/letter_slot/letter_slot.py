"""Contains the LetterSlot class."""

from __future__ import annotations

from bongo_solver.letter_tile import LetterTile  # noqa: TC001


class LetterSlot:
    """A slot to contain a letter in a word."""

    container_format = "[{}]"

    letter_tile: LetterTile | None = None

    def __init__(self, multiplier: int = 1) -> None:
        """Initialize the letter slot."""
        self.__multiplier: int = multiplier

    @property
    def multiplier(self) -> int:
        """Get the multiplier."""
        return self.__multiplier

    @property
    def is_multiplier(self) -> bool:
        """Return True if the slot is a multiplier."""
        return self.__multiplier > 1

    @property
    def score(self) -> int:
        """Return the score of the letter tile in the slot."""
        if self.letter_tile is None:
            return 0

        return self.letter_tile.score * self.__multiplier

    @property
    def is_empty(self) -> bool:
        """Return True if the slot is empty."""
        return self.letter_tile is None

    @property
    def contents(self) -> str:
        """Gets the string representation of the contents of the slot."""
        if self.letter_tile is not None:
            return (
                str(self.letter_tile)
                if not self.is_multiplier
                else f"{self.letter_tile.letter}"
                f"({self.letter_tile.score}){self.__multiplier}x"
            )
        return f"{self.multiplier}" if self.is_multiplier else " "

    def __str__(self) -> str:
        """Return a string representation of the letter slot."""
        return self.container_format.format(self.contents)

    def __repr__(self) -> str:
        """Return a string representation of the letter slot."""
        return f"{self.__class__.__name__}({self.letter_tile}, {self.__multiplier})"

    def __eq__(self, other: object) -> bool:
        """Check if other object is same as this letter slot."""
        if not isinstance(other, LetterSlot):
            return False

        return self.letter_tile == other.letter_tile
