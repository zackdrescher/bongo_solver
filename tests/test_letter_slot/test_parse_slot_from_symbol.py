"""Tests for the parse_slot_from_symbol function."""

import pytest

from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_slot.letter_slot import LetterSlot
from bongo_solver.letter_slot.parse_slot_from_symbol import parse_slot_from_symbol


def test_parse_slot_from_symbol__space__empty_slot() -> None:
    """Test that parse_slot_from_symbol returns an empty slot when passed a space."""
    result = parse_slot_from_symbol(" ")

    assert result == LetterSlot()


@pytest.mark.parametrize("multiplier", list(range(1, 4)))
def test_parse_slot_from_symbol__digit__letter_slot(multiplier: int) -> None:
    """Test that parse_slot_from_symbol returns a letter slot when passed a digit."""
    result = parse_slot_from_symbol(str(multiplier))

    assert result == LetterSlot(multiplier)


@pytest.mark.parametrize("value", ["B", "b"])
def test_parse_slot_from_symbol__b__bonus_letter_slot(value: str) -> None:
    """Test that parse_slot_from_symbol returns a bonus letter slot when passed "B"."""
    result = parse_slot_from_symbol(value)

    assert isinstance(result, BonusLetterSlot)


@pytest.mark.parametrize("value", ["A", "a", "-", "/"])
def test_parse_slot_from_symbol__invalid(value: str) -> None:
    """Test that parse_slot_from_symbol raises a ValueError when symbolis  invalid."""
    with pytest.raises(ValueError, match=f"Encountered invlaid slot symbol: {value}."):
        parse_slot_from_symbol(value)


def test_parse_slot_from_symbol__invalid_length() -> None:
    """Test that parse_slot_from_symbol raises a ValueError string length > 1."""
    with pytest.raises(ValueError, match="Symbol can only be a single character."):
        parse_slot_from_symbol("ab")
