"""Contains the WordRow class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bongo_solver.dictionary import Dictionary  # noqa: TC001
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot

if TYPE_CHECKING:  # pragma: no cover
    from bongo_solver.letter_tile import LetterTile

    from .letter_slot.base_letter_slot import LetterSlot

WORD_ROW_LENGTH = 5


class WordRow:
    """A row of letter slots that make up a word."""

    def __init__(self, slots: list[LetterSlot], dictionary: Dictionary) -> None:
        """Initialize the word row."""
        if len(slots) != WORD_ROW_LENGTH:
            msg = f"A word row must contain {WORD_ROW_LENGTH} slots."
            raise ValueError(msg)
        if sum(isinstance(slot, BonusLetterSlot) for slot in slots) > 1:
            msg = "A word row can only contain one bonus slot."
            raise ValueError(msg)
        self.__slots = slots
        self.__dictionary = dictionary

    @property
    def slots(self) -> list[LetterSlot]:
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

    def get_bonus_ix(self) -> int:
        """Return the index of the bonus slot."""
        return next(
            (
                ix
                for ix, slot in enumerate(self.__slots)
                if isinstance(slot, BonusLetterSlot)
            ),
            -1,
        )

    def __getitem__(self, index: int) -> LetterSlot:
        """Return the slot at the given index."""
        return self.__slots[index]

    def __setitem__(self, index: int, tile: LetterTile | None) -> None:
        """Placees a tile in the slot at the given index."""
        self.__slots[index].letter_tile = tile

    def __str__(self) -> str:
        """Return a string representation of the word row."""
        return "".join(str(slot) for slot in self.__slots)
