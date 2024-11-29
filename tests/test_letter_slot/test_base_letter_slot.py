"""Tests for the AbstractLetterSlot class."""

from unittest.mock import MagicMock

from bongo_solver.letter_slot.base_letter_slot import LetterSlot
from bongo_solver.letter_tile import LetterTile


def test_letter_slot__init__no_tile() -> None:
    """Test that a letter slot is empty when created."""
    slot = LetterSlot()
    assert slot.letter_tile is None


def test_letter_slot__score__no_tile() -> None:
    """Test that the score is zero when the slot is empty."""
    slot = LetterSlot()
    assert slot.score == 0


def test_letter_slot__score__with_tile() -> None:
    """Test that the score is the score of the letter tile."""
    # arrange
    slot = LetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    letter_mock.score = 5
    slot.letter_tile = letter_mock

    # act
    score = slot.score

    # assert
    assert score == 5


def test_is_empty__is_empty() -> None:
    """Test that is_empty returns True when the slot is empty."""
    slot = LetterSlot()
    assert slot.is_empty is True


def test_is_empty_not_empty() -> None:
    """Test that is_empty returns False when the slot is not empty."""
    # arrange
    slot = LetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    slot.letter_tile = letter_mock

    # act
    is_empty = slot.is_empty

    # assert
    assert is_empty is False


def test_is_multiplier__is_multiplier() -> None:
    """Test that is_multiplier returns True when the slot is a multiplier."""
    slot = LetterSlot(multiplier=2)
    assert slot.is_multiplier is True


def test_is_multiplier__not_multiplier() -> None:
    """Test that is_multiplier returns False when the slot is not a multiplier."""
    slot = LetterSlot()
    assert slot.is_multiplier is False
