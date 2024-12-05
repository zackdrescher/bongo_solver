"""A board of word rows that make up a Bongo puzzle."""

from __future__ import annotations

import re
from typing import cast

from bongo_solver.dictionary import Dictionary  # noqa: TC001
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.word.bonus_word import BonusWord

from .word.word_row import WordRow

BOARD_SIZE = 5


def try_get_bonus_word(rows: list[WordRow], dictionary: Dictionary) -> BonusWord | None:
    """Validate that the rows contain only one bonus slot."""
    if rows[-1].get_bonus_ix() != -1:
        return None
    prev_bonus_ix = rows[0].get_bonus_ix()
    if prev_bonus_ix == -1:
        return None

    bonus_slots: list[BonusLetterSlot] = [cast(BonusLetterSlot, rows[0][prev_bonus_ix])]
    for row in rows[1:-1]:
        bonus_ix = row.get_bonus_ix()
        if bonus_ix == -1 or abs(bonus_ix - prev_bonus_ix) > 1:
            return None
        bonus_slots.append(cast(BonusLetterSlot, row[bonus_ix]))
        prev_bonus_ix = bonus_ix

    return BonusWord(bonus_slots, dictionary)


BOARD_ROW_PATTERN = re.compile(r"(\[.....\])")


class Board:
    """A board of word rows that make up a Bongo puzzle."""

    @classmethod
    def from_str(cls, board_str: str, dictionary: Dictionary) -> Board:
        """Convert a string contianin a board configuration."""
        matches = re.findall(BOARD_ROW_PATTERN, board_str)
        msg = "Insufficient board configuration in board_str."

        if len(matches) != BOARD_SIZE:
            raise ValueError(msg)
        words = [WordRow.from_str(row, dictionary) for row in matches]
        return cls(words, dictionary)

    def __init__(self, rows: list[WordRow], dictionary: Dictionary) -> None:
        """Initialize the board."""
        if len(rows) != BOARD_SIZE:
            msg = f"A board must contain {BOARD_SIZE} rows."
            raise ValueError(msg)
        self.__rows = rows
        self.__bonus_word = try_get_bonus_word(rows, dictionary)
        if not self.__bonus_word:
            msg = "The board does not have a valid bonus word configuration."
            raise ValueError(msg)

    # TODO: (ZD) SCORE
