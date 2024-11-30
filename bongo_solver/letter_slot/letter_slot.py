from .base_letter_slot import BaseLetterSlot


class LetterSlot(BaseLetterSlot):
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
    def score(self) -> int:
        return super().score * self.multiplier

    def __str__(self) -> str:
        if self.is_empty and self.is_multiplier:
            return f"[{self.__multiplier}x]"
        return super().__str__()
