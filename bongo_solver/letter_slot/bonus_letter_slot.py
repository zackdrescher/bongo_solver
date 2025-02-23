"""Contains the BonusLetterSlot class."""

from .letter_slot import LetterSlot


class BonusLetterSlot(LetterSlot):
    """A letter slot that is used a part of the bonus word."""

    container_format = "({})"

    @property
    def contents(self) -> str:
        """Gets the string representation of the contents of the slot."""
        contents = super().contents
        return "B" if contents == " " else contents
