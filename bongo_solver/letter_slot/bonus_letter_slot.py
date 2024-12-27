"""Contains the BonusLetterSlot class."""

from .letter_slot import LetterSlot


class BonusLetterSlot(LetterSlot):
    """A letter slot that is used a part of the bonus word."""

    def __str__(self) -> str:
        """Return a string representation of the letter slot."""
        contents: str
        if self.letter_tile is not None:
            contents = (
                str(self.letter_tile)
                if not self.is_multiplier
                else f"{self.letter_tile.letter}"
                f"({self.letter_tile.score}x{self.__multiplier})B"
            )
        else:
            contents = "B"

        return f"[{contents}]"
