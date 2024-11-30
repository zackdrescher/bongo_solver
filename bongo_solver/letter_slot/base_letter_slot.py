"""Contains the LetterSlot class."""

from __future__ import annotations

from typing import Any, Self

from bongo_solver import nobeartype
from bongo_solver.letter_tile import LetterTile  # noqa: TC001


class BaseLetterSlot:
    """A slot to contain a letter in a word."""

    @nobeartype
    def __new__(cls, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Self:  # noqa: ARG003
        """Prevent instantiation of the base class."""
        if cls is BaseLetterSlot:
            msg = "Cannot instantiate the base class."
            raise TypeError(msg)
        return super().__new__(cls)

    letter_tile: LetterTile | None = None

    @property
    def score(self) -> int:
        """Return the score of the letter tile in the slot."""
        if self.letter_tile is None:
            return 0

        return self.letter_tile.score

    @property
    def is_empty(self) -> bool:
        """Return True if the slot is empty."""
        return self.letter_tile is None

    def __str__(self) -> str:
        """Return a string representation of the letter slot."""
        contents = " "
        if self.letter_tile is not None:
            contents = str(self.letter_tile)

        return f"[{contents}]"

    def __repr__(self) -> str:
        """Return a string representation of the letter slot."""
        return f"{self.__class__.__name__}({self.letter_tile})"

    def __eq__(self, other: object) -> bool:
        """Check if other object is same as this letter slot."""
        if not isinstance(other, BaseLetterSlot):
            return False

        return self.letter_tile == other.letter_tile
