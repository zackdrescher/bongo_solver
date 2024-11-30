"""Tests for the BaseLetterSlot class."""

from unittest.mock import MagicMock

from bongo_solver.letter_slot.letter_slot import LetterSlot
from bongo_solver.letter_tile import LetterTile


def test_is_multiplier__is_multiplier() -> None:
    """Test that is_multiplier returns True when the slot is a multiplier."""
    slot = LetterSlot(multiplier=2)
    assert slot.is_multiplier is True


def test_is_multiplier__not_multiplier() -> None:
    """Test that is_multiplier returns False when the slot is not a multiplier."""
    slot = LetterSlot()
    assert slot.is_multiplier is False


def test__str__multiplier() -> None:
    """Test that str returns the expected value when the slot is a multiplier."""
    slot = LetterSlot(multiplier=2)
    assert str(slot) == "[2x]"


def test__str__empty() -> None:
    """Test that str returns the expected value when the slot is empty."""
    slot = LetterSlot()
    assert str(slot) == "[ ]"


def test__str__letter() -> None:
    """Test that str returns the expected value when the slot contains a letter."""
    # arrange
    slot = LetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    letter_mock.__str__.return_value = "A(1)"  # type: ignore[attr-defined]
    slot.letter_tile = letter_mock

    # act
    result = str(slot)

    # assert
    assert result == "[A(1)]"
