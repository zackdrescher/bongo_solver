"""Test the BonusLetterSlot class."""

from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot


def test_bonus_letter_slot__init__no_tile() -> None:
    """Test that a bonus letter slot is empty when created."""
    slot = BonusLetterSlot()
    assert slot.letter_tile is None
