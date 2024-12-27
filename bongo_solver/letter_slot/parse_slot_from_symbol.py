"""Contains parse_slot_from_symbol function."""

from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_slot.letter_slot import LetterSlot


def parse_slot_from_symbol(symbol: str) -> LetterSlot:
    """Parse LetterSlot from a symbol string."""
    if len(symbol) != 1:
        msg = "Symbol can only be a single character."
        raise ValueError(msg)

    if symbol == " ":
        return LetterSlot()
    if symbol.isdigit():
        return LetterSlot(int(symbol))
    if symbol.upper() == "B":
        return BonusLetterSlot()

    msg = f"Encountered invlaid slot symbol: {symbol}."
    raise ValueError(msg)
