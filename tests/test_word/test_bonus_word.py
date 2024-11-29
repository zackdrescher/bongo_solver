from unittest.mock import MagicMock

import pytest

from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.word.bonus_word import BonusWord


def test_init__successful() -> None:
    """Test that a WordRow can be initialized."""
    slots = [
        BonusLetterSlot(),
        BonusLetterSlot(),
        BonusLetterSlot(),
        BonusLetterSlot(),
    ]
    dictionary = MagicMock(Dictionary)

    word_row = BonusWord(slots, dictionary)

    assert word_row.slots == slots
    assert word_row.dictionary == dictionary


def test_init__invalid_length() -> None:
    """Test that a WordRow cannot be initialized with an invalid number of slots."""
    slots = [BonusLetterSlot(), BonusLetterSlot(), BonusLetterSlot()]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="A bonus word must contain 4 slots."):
        BonusWord(slots, dictionary)
