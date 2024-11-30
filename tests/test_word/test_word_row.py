"""Tests for the WordRow class."""

from unittest.mock import MagicMock

import pytest

from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.base_letter_slot import BaseLetterSlot
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.word.word_row import WordRow, parse_slot_from_symbol


def test_init__successful() -> None:
    """Test that a WordRow can be initialized."""
    slots = [
        BaseLetterSlot(),
        BaseLetterSlot(),
        BaseLetterSlot(),
        BaseLetterSlot(),
        BaseLetterSlot(),
    ]
    dictionary = MagicMock(Dictionary)

    word_row = WordRow(slots, dictionary)

    assert word_row.slots == slots
    assert word_row.dictionary == dictionary


def test_init__invalid_length() -> None:
    """Test that a WordRow cannot be initialized with an invalid number of slots."""
    slots = [BaseLetterSlot(), BaseLetterSlot(), BaseLetterSlot(), BaseLetterSlot()]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="A word row must contain 5 slots."):
        WordRow(slots, dictionary)


def test_init__too_many_bonus_slots() -> None:
    """Test that a WordRow cannot be initialized with more than one bonus slot."""
    slots = [
        BaseLetterSlot(),
        BonusLetterSlot(),
        BonusLetterSlot(),
        BaseLetterSlot(),
        BaseLetterSlot(),
    ]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="A word row can only contain one bonus slot."):
        WordRow(slots, dictionary)


def test_get_bonus_ix__no_bonus() -> None:
    """Test that get_bonus_ix returns -1 when there is no bonus slot."""
    slots = [BaseLetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

    bonus_ix = word_row.get_bonus_ix()

    assert bonus_ix == -1


@pytest.mark.parametrize("bonus_ix", [0, 1, 2, 3, 4])
def test_get_bonus_ix__with_bonus(bonus_ix: int) -> None:
    """Test that get_bonus_ix returns the index of the bonus slot."""
    slots = [BaseLetterSlot() for _ in range(5)]
    slots[bonus_ix] = BonusLetterSlot()
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

    result = word_row.get_bonus_ix()

    assert result == bonus_ix


def test_parse_slot_from_symbol__space__empty_slot():
    result = parse_slot_from_symbol(" ")

    assert result == BaseLetterSlot()
