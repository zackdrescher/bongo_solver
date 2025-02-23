"""Test the BonusLetterSlot class."""

from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot


def test_bonus_letter_slot__init__no_tile() -> None:
    """Test that a bonus letter slot is empty when created."""
    slot = BonusLetterSlot()
    assert slot.letter_tile is None


def test_bonus_letter_slot_str__empty__contains_b() -> None:
    """Test that an empty bonus slot contains B."""
    slot = BonusLetterSlot()
    assert slot.contents == "B"


def test_bonus_letter_slot_str__mult__has_parens() -> None:
    """Test that an multiplier bonus slot contains uses parenthesis."""
    slot = BonusLetterSlot(multiplier=2)

    assert str(slot) == "(2)"
