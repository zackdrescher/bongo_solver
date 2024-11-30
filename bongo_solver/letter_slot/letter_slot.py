"""Contains the LetterSlot class."""

from .base_letter_slot import BaseLetterSlot


class LetterSlot(BaseLetterSlot):
    """A typical letter slot with a multiplier."""

    def __init__(self, multiplier: int = 1) -> None:
        """Initialize the letter slot."""
        self.__multiplier: int = multiplier

    @property
    def multiplier(self) -> int:
        """Get the multiplier."""
        return self.__multiplier

    @property
    def is_multiplier(self) -> bool:
        """Return True if the slot is a multiplier."""
        return self.__multiplier > 1

    @property
    def score(self) -> int:  # noqa: D102
        return super().score * self.multiplier

    def __str__(self) -> str:  # noqa: D105
        if self.is_empty and self.is_multiplier:
            return f"[{self.__multiplier}x]"

        return super().__str__()
