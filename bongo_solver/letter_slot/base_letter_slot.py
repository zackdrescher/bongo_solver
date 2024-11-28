"""Contains the LetterSlot class."""

from __future__ import annotations

from typing import Any

from typing_extensions import Self

from bongo_solver.letter_tile import LetterTile  # noqa: TC001


class BaseLetterSlot:
    """An abstract base class for a slot containing a letter in a word."""

    def __new__(cls, *args: tuple[Any], **kwargs: dict[str, Any]) -> Self:  # noqa: ARG003
        """Create a new instance of the class."""
        if cls is BaseLetterSlot:
            msg = f"{BaseLetterSlot.__name__} cannot be instantiated directly."
            raise TypeError(msg)
        return super().__new__(cls)

    letter_tile: LetterTile | None = None

    def place_letter(self, letter_tile: LetterTile) -> None:
        """Place a letter tile in the slot."""
        self.letter_tile = letter_tile

    def remove_letter(self) -> None:
        """Remove the letter tile from the slot."""
        self.letter_tile = None

    def score(self) -> int:
        """Return the score of the letter tile in the slot."""
        if self.letter_tile is None:
            return 0

        return self.letter_tile.score

    def is_empty(self) -> bool:
        """Return True if the slot is empty."""
        return self.letter_tile is None

    def __repr__(self) -> str:
        """Return a string representation of the letter slot."""
        return f"{self.__class__.__name__}({self.letter_tile})"
