"""Tests for the AbstractLetterSlot class."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from bongo_solver.letter_slot.base_letter_slot import BaseLetterSlot
from bongo_solver.letter_tile import LetterTile


def test_init__raises() -> None:
    """Test that a BaseLetterSlot cannot be initialized."""
    with pytest.raises(TypeError, match="Cannot instantiate the base class."):
        BaseLetterSlot()


class ConcreteLetterSlot(BaseLetterSlot):
    """Test concrete class for the BaseLetterSlot class."""


def test_letter_slot__init__no_tile() -> None:
    """Test that a letter slot is empty when created."""
    slot = ConcreteLetterSlot()
    assert slot.letter_tile is None


def test_letter_slot__score__no_tile() -> None:
    """Test that the score is zero when the slot is empty."""
    slot = ConcreteLetterSlot()
    assert slot.score == 0


def test_letter_slot__score__with_tile() -> None:
    """Test that the score is the score of the letter tile."""
    # arrange
    slot = ConcreteLetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    letter_mock.score = 5
    slot.letter_tile = letter_mock

    # act
    score = slot.score

    # assert
    assert score == 5


def test_is_empty__is_empty() -> None:
    """Test that is_empty returns True when the slot is empty."""
    slot = ConcreteLetterSlot()
    assert slot.is_empty is True


def test_is_empty_not_empty() -> None:
    """Test that is_empty returns False when the slot is not empty."""
    # arrange
    slot = ConcreteLetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    slot.letter_tile = letter_mock

    # act
    is_empty = slot.is_empty

    # assert
    assert is_empty is False


def test__str__empty() -> None:
    """Test that str returns the expected value when the slot is empty."""
    slot = ConcreteLetterSlot()
    assert str(slot) == "[ ]"


def test__str__letter() -> None:
    """Test that str returns the expected value when the slot contains a letter."""
    # arrange
    slot = ConcreteLetterSlot()
    letter_mock = MagicMock(spec=LetterTile)
    letter_mock.__str__.return_value = "A(1)"  # type: ignore[attr-defined]
    slot.letter_tile = letter_mock

    # act
    result = str(slot)

    # assert
    assert result == "[A(1)]"


# TODO(ZD): UNCOMMENT THESE TESTS
# https://github.com/zackdrescher/bongo_solver/issues/8
# @pytest.mark.parametrize(
#     ("multiplier", "letter_tile"),  # noqa: ERA001
#     [  # noqa: ERA001, RUF100
#         (1, MagicMock(LetterTile)),  # noqa: ERA001
#         (2, MagicMock(LetterTile)),  # noqa: ERA001
#         (1, None),  # noqa: ERA001
#         (2, None),  # noqa: ERA001
#     ],
# )  # noqa: ERA001, RUF100
# def test_eq__is_equal__returns_true(
#     multiplier: int,
#     letter_tile: LetterTile | None,
# ) -> None:
#     """Test identical slots are equal."""
#     slot1 = ConcreteLetterSlot(multiplier)  # noqa: ERA001
#     slot1.letter_tile = letter_tile  # noqa: ERA001
#     slot2 = ConcreteLetterSlot(multiplier)  # noqa: ERA001
#     slot2.letter_tile = letter_tile  # noqa: ERA001

#     assert slot1 == slot2  # noqa: ERA001
