"""Contains the WordRow class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bongo_solver.dictionary import Dictionary  # noqa: TC001
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot

from .word import Word

if TYPE_CHECKING:  # pragma: no cover
    from bongo_solver.letter_slot.base_letter_slot import LetterSlot

WORD_ROW_LENGTH = 5


class WordRow(Word):
    """A row of letter slots that make up a word."""

    def __init__(self, slots: list[LetterSlot], dictionary: Dictionary) -> None:
        """Initialize the word row."""
        if len(slots) != WORD_ROW_LENGTH:
            msg = f"A word row must contain {WORD_ROW_LENGTH} slots."
            raise ValueError(msg)
        if sum(isinstance(slot, BonusLetterSlot) for slot in slots) > 1:
            msg = "A word row can only contain one bonus slot."
            raise ValueError(msg)

        super().__init__(slots, dictionary)

    def get_bonus_ix(self) -> int:
        """Return the index of the bonus slot."""
        return next(
            (
                ix
                for ix, slot in enumerate(self.slots)
                if isinstance(slot, BonusLetterSlot)
            ),
            -1,
        )
