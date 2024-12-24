"""Tests for the WordRow class."""

from unittest.mock import MagicMock

import pytest

from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.base_letter_slot import BaseLetterSlot
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_slot.letter_slot import LetterSlot
from bongo_solver.word.word_row import WordRow


def test_init__successful() -> None:
    """Test that a WordRow can be initialized."""
    slots: list[BaseLetterSlot] = [
        LetterSlot(),
        LetterSlot(),
        LetterSlot(),
        LetterSlot(),
        LetterSlot(),
    ]
    dictionary = MagicMock(Dictionary)

    word_row = WordRow(slots, dictionary)

    assert word_row.slots == slots
    assert word_row.dictionary == dictionary


def test_init__invalid_length() -> None:
    """Test that a WordRow cannot be initialized with an invalid number of slots."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="A word row must contain 5 slots."):
        WordRow(slots, dictionary)


def test_init__too_many_bonus_slots() -> None:
    """Test that a WordRow cannot be initialized with more than one bonus slot."""
    slots = [
        LetterSlot(),
        BonusLetterSlot(),
        BonusLetterSlot(),
        LetterSlot(),
        LetterSlot(),
    ]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="A word row can only contain one bonus slot."):
        WordRow(slots, dictionary)


def test_get_bonus_ix__no_bonus() -> None:
    """Test that get_bonus_ix returns -1 when there is no bonus slot."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

    bonus_ix = word_row.get_bonus_ix()

    assert bonus_ix == -1


@pytest.mark.parametrize("bonus_ix", [0, 1, 2, 3, 4])
def test_get_bonus_ix__with_bonus(bonus_ix: int) -> None:
    """Test that get_bonus_ix returns the index of the bonus slot."""
    slots: list[BaseLetterSlot] = [LetterSlot() for _ in range(5)]
    slots[bonus_ix] = BonusLetterSlot()
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

    result = word_row.get_bonus_ix()

    assert result == bonus_ix


def test_from_str__empty__successful() -> None:
    """Test that a WordRow can be created from a string."""
    row_string = "[     ]"
    dictionary = MagicMock(Dictionary)

    word_row = WordRow.from_str(row_string, dictionary)

    assert isinstance(word_row, WordRow)
    assert len(word_row.slots) == 5
    assert all(isinstance(slot, LetterSlot) for slot in word_row.slots)


def replace_char(string: str, index: int, new_char: str) -> str:
    """Replace a character in a string."""
    if index < 0 or index >= len(string):
        msg = "Index out of range"
        raise IndexError(msg)
    return string[:index] + new_char + string[index + 1 :]


@pytest.mark.parametrize(
    ("bonus_ix", "bonus_symbol"),
    zip(list(range(5)) * 2, ["B", "b"] * 5),
)
def test_from_str__with_bonus__successful(bonus_ix: int, bonus_symbol: str) -> None:
    """Test that a WordRow can be created from a string."""
    row_string = replace_char("[     ]", bonus_ix + 1, bonus_symbol)
    dictionary = MagicMock(Dictionary)

    word_row = WordRow.from_str(row_string, dictionary)

    assert isinstance(word_row, WordRow)
    assert len(word_row.slots) == 5
    assert all(isinstance(slot, BaseLetterSlot) for slot in word_row.slots[:bonus_ix])
    assert all(
        isinstance(slot, BaseLetterSlot) for slot in word_row.slots[bonus_ix + 1 :]
    )
    assert isinstance(word_row.slots[bonus_ix], BonusLetterSlot)


@pytest.mark.parametrize("mult", [1, 2, 3, 4, 5])
def test_from_str__with_mult__has_mult(mult: int) -> None:
    """Test that a WordRow can be created from a string."""
    innards = "".join([str(mult)] * 5)
    row_string = f"[{innards}]"
    dictionary = MagicMock(Dictionary)

    word_row = WordRow.from_str(row_string, dictionary)

    assert isinstance(word_row, WordRow)
    assert len(word_row.slots) == 5
    assert all(isinstance(slot, LetterSlot) for slot in word_row.slots)
    # TODO (ZD): Uncomment this line
    # https://github.com/zackdrescher/bongo_solver/issues/8
    # assert all(slot.multiplier == mult for slot in word_row.slots)  # noqa: ERA001


def test_from_str__invalid_string() -> None:
    """Test that from_str raises an error when given an invalid string."""
    row_string = "[ 1 2 3 4 5 ]"
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="Imporoperly formated WordRow string."):
        WordRow.from_str(row_string, dictionary)
