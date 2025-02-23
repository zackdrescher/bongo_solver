"""A board of word rows that make up a Bongo puzzle."""

from __future__ import annotations

import re
from typing import cast

from bongo_solver.dictionary import Dictionary  # noqa: TC001
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_slot.letter_slot import LetterSlot
from bongo_solver.letter_tile import LetterTile
from bongo_solver.word.bonus_word import BonusWord

from .word.word_row import WordRow

BOARD_SIZE = 5

Position = tuple[int, int]


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


def position_valid(p: Position) -> bool:
    """Check if postion is valid in board."""
    return pos_ix_valid(p[0]) and pos_ix_valid(p[1])


def pos_ix_valid(i: int) -> bool:
    """Check if int is valid position."""
    return i >= 0 and i < BOARD_SIZE


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

    def get_slot(self, i: int, j: int) -> LetterSlot:
        """Get the letter slot at a board position."""
        return self.get_position_slot((i, j))

    def get_position_slot(self, p: Position) -> LetterSlot:
        """Get the letter slot at a board position."""
        if not position_valid(p):
            msg = f"position {p} out of bounds."
            raise IndexError(msg)
        i, j = p
        return self.__rows[i][j]

    def place_tile(self, tile: LetterTile | None, p: Position) -> LetterTile | None:
        """Places the provided tile in the letter slot at postion.

        if previouslt occupied returns previously occupying tile otherwise returns null.
        """
        postion_slot = self.get_position_slot(p)
        prev_tile = postion_slot.letter_tile

        postion_slot.letter_tile = tile

        return prev_tile

    def __getitem__(self, p: Position) -> LetterSlot:
        """Get letter slot at position."""
        return self.get_position_slot(p)

    def __setitem__(self, p: Position, tile: LetterTile) -> None:
        """Set letter tile in position slot."""
        self.place_tile(tile, p)

    # TODO(ZD): SCORE
    # https://github.com/zackdrescher/bongo_solver/issues/2
