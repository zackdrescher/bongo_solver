"""Tests for the AbstractLetterSlot class."""

from unittest.mock import MagicMock

import pytest

from bongo_solver.letter_slot import base_letter_slot
from bongo_solver.letter_tile import LetterTile


def test_abstract_letter_slot__new__raises_error() -> None:
    """Test that BaseLetterSlot.__new__ raises an error."""
    with pytest.raises(
        TypeError,
        match="BaseLetterSlot cannot be instantiated directly.",
    ):
        base_letter_slot.BaseLetterSlot()


class ConcreteLetterSlot(base_letter_slot.BaseLetterSlot):
    """A concrete implementation of the BaseLetterSlot class."""


def test_letter_slot__init__no_tile() -> None:
    """Test that a letter slot is empty when created."""
    slot = ConcreteLetterSlot()
    assert slot.letter_tile is None


def test_letter_slot__place_letter() -> None:
    """Test that a letter tile can be placed in the slot."""
    # arrange
    slot = ConcreteLetterSlot()
    letter_mock = MagicMock(spec=LetterTile)

    # act
    slot.place_letter(letter_mock)

    # assert
    assert slot.letter_tile == letter_mock


def test_letter_slot__remove_letter() -> None:
    """Test that a letter tile can be removed from the slot."""
    # arrange
    slot = ConcreteLetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    slot.place_letter(letter_mock)

    # act
    slot.remove_letter()

    # assert
    assert slot.letter_tile is None


def test_letter_slot__score__no_tile() -> None:
    """Test that the score is zero when the slot is empty."""
    slot = ConcreteLetterSlot()
    assert slot.score() == 0


def test_letter_slot__score__with_tile() -> None:
    """Test that the score is the score of the letter tile."""
    # arrange
    slot = ConcreteLetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    letter_mock.score = 5
    slot.place_letter(letter_mock)

    # act
    score = slot.score()

    # assert
    assert score == 5


def test_is_empty__is_empty() -> None:
    """Test that is_empty returns True when the slot is empty."""
    slot = ConcreteLetterSlot()
    assert slot.is_empty() is True


def test_is_empty_not_empty() -> None:
    """Test that is_empty returns False when the slot is not empty."""
    # arrange
    slot = ConcreteLetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    slot.place_letter(letter_mock)

    # act
    is_empty = slot.is_empty()

    # assert
    assert is_empty is False
