"""Contains the BonusLetterSlot class."""

from .base_letter_slot import BaseLetterSlot


class BonusLetterSlot(BaseLetterSlot):
    """A letter slot that is used a part of the bonus word."""

    def __init__(self) -> None:
        """Initialize the bonus letter slot."""
        super().__init__()
