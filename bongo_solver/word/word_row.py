"""Contains the WordRow class."""

from __future__ import annotations

import re

from bongo_solver.dictionary import Dictionary  # noqa: TC001
from bongo_solver.letter_slot.base_letter_slot import BaseLetterSlot
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_slot.letter_slot import LetterSlot

from .word import Word

WORD_ROW_LENGTH = 5

STR_SLOT_SYMBOL_REGEX = r"(/d|[Bb ])"
STR_ROW_REGEX = rf"/[{STR_SLOT_SYMBOL_REGEX*WORD_ROW_LENGTH}/]"


def parse_slot_from_symbol(symbol: str) -> BaseLetterSlot:
    """Parse LetterSlot from a symbol string."""
    if len(symbol) != 1:
        msg = "Symbol can only be a single character."
        raise ValueError(msg)

    if symbol == " ":
        return LetterSlot()
    if symbol.isdigit():
        return BaseLetterSlot(int(symbol))
    if symbol.upper() == "B":
        return BonusLetterSlot()

    msg = f"Encountered invlaid slot symbol: {symbol}."
    raise ValueError(msg)


class WordRow(Word):
    """A row of letter slots that make up a word."""

    @classmethod
    def from_str(cls, row_string: str, dictionary: Dictionary) -> WordRow:
        """Parse a row string to WordRow."""
        match = re.match(STR_ROW_REGEX, row_string)

        if not match:
            msg = "Imporoperly formated WordRow string."
            raise ValueError(msg)

        slots = [parse_slot_from_symbol(g) for g in match.groups()]

        return cls(slots, dictionary)

    def __init__(self, slots: list[BaseLetterSlot], dictionary: Dictionary) -> None:
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
