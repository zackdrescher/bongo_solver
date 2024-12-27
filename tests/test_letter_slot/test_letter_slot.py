"""Tests for the BaseLetterSlot class."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from bongo_solver.letter_slot.letter_slot import LetterSlot
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
    letter_mock = MagicMock(spec=LetterSlot)
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
    letter_mock = MagicMock(spec=LetterSlot)
    slot.letter_tile = letter_mock

    # act
    is_empty = slot.is_empty

    # assert
    assert is_empty is False


def test__str__empty() -> None:
    """Test that str returns the expected value when the slot is empty."""
    slot = LetterSlot()
    assert str(slot) == "[ ]"


def test__str__letter() -> None:
    """Test that str returns the expected value when the slot contains a letter."""
    # arrange
    slot = LetterSlot()
    letter_mock = MagicMock(spec=LetterSlot)
    letter_mock.__str__.return_value = "A(1)"  # type: ignore[attr-defined]
    slot.letter_tile = letter_mock

    # act
    result = str(slot)

    # assert
    assert result == "[A(1)]"


def test__str__multiplier() -> None:
    """Test that str returns the expected value when the slot is a multiplier."""
    slot = LetterSlot(multiplier=2)
    assert str(slot) == "[2]"


# TODO(ZD): TEST STR LETTER MULTIPLIER
# https://github.com/zackdrescher/bongo_solver/issues/8


@pytest.mark.parametrize(
    ("multiplier", "letter_tile"),
    [  # noqa: ERA001, RUF100
        (1, MagicMock(LetterTile)),
        (2, MagicMock(LetterTile)),
        (1, None),
        (2, None),
    ],
)  # noqa: ERA001, RUF100
def test_eq__is_equal__returns_true(
    multiplier: int,
    letter_tile: LetterTile | None,
) -> None:
    """Test identical slots are equal."""
    slot1 = LetterSlot(multiplier)
    slot1.letter_tile = letter_tile
    slot2 = LetterSlot(multiplier)
    slot2.letter_tile = letter_tile

    assert slot1 == slot2


def test_is_multiplier__is_multiplier() -> None:
    """Test that is_multiplier returns True when the slot is a multiplier."""
    slot = LetterSlot(multiplier=2)
    assert slot.is_multiplier is True


def test_is_multiplier__not_multiplier() -> None:
    """Test that is_multiplier returns False when the slot is not a multiplier."""
    slot = LetterSlot()
    assert slot.is_multiplier is False
