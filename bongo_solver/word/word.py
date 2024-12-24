"""Base class for a word."""

from __future__ import annotations

from collections.abc import Sequence  # noqa: TC003
from typing import TYPE_CHECKING, Any, Self

from bongo_solver import nobeartype
from bongo_solver.dictionary import Dictionary  # noqa: TC001

if TYPE_CHECKING:  # pragma: no cover
    from bongo_solver.letter_slot.base_letter_slot import BaseLetterSlot
    from bongo_solver.letter_tile import LetterTile


class Word:
    """A word made up of letter slots."""

    @nobeartype
    def __new__(cls, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Self:  # noqa: ARG003
        """Prevent instantiation of the base class."""
        if cls is Word:
            msg = "Cannot instantiate the base class."
            raise TypeError(msg)
        return super().__new__(cls)

    def __init__(self, slots: Sequence[BaseLetterSlot], dictionary: Dictionary) -> None:
        """Initialize the word."""
        self.__slots = slots
        self.__dictionary = dictionary

    @property
    def slots(self) -> Sequence[BaseLetterSlot]:
        """Return the slots in the word row."""
        return self.__slots

    @property
    def dictionary(self) -> Dictionary:
        """Return the dictionary used to validate words."""
        return self.__dictionary

    @property
    def score(self) -> int:
        """Return the score of the word row."""
        score = sum(slot.score for slot in self.__slots)

        if self.__dictionary.is_common(self.word):
            return round(score * 1.3)
        if self.word in self.__dictionary:
            return score

        return 0

    @property
    def word(self) -> str:
        """Return the word represented by the word row."""
        return "".join(
            str(slot.letter_tile.letter) if not slot.is_empty else " "  # type: ignore[union-attr]
            for slot in self.__slots
        ).strip()

    def __getitem__(self, index: int) -> BaseLetterSlot:
        """Return the slot at the given index."""
        return self.__slots[index]

    def __setitem__(self, index: int, tile: LetterTile | None) -> None:
        """Placees a tile in the slot at the given index."""
        self.__slots[index].letter_tile = tile

    def __str__(self) -> str:
        """Return a string representation of the word row."""
        return "".join(str(slot) for slot in self.__slots)
