"""A module for the BonusWord class."""

from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot

from .word import Word

BONUS_WORD_LENGTH = 4


class BonusWord(Word):
    """A word of bonus letter slots."""

    def __init__(self, slots: list[BonusLetterSlot], dictionary: Dictionary) -> None:
        """Initialize the bonus word."""
        if len(slots) != BONUS_WORD_LENGTH:
            msg = f"A bonus word must contain {BONUS_WORD_LENGTH} slots."
            raise ValueError(msg)

        super().__init__(slots, dictionary)
