"""Contains parse_slot_from_symbol function."""

from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_slot.letter_slot import LetterSlot


def parse_slot_from_symbol(symbol: str) -> LetterSlot:
    """Parse LetterSlot from a symbol string."""
    symbol_len = len(symbol)
    if symbol_len < 1 or symbol_len > 2:  # noqa: PLR2004
        msg = "Symbol can only be a single character or astrisk following digit."
        raise ValueError(msg)

    if symbol == " ":
        return LetterSlot()
    if symbol.isdigit():
        return LetterSlot(int(symbol))
    if symbol.upper() == "B":
        return BonusLetterSlot()
    if symbol_len == 2 and symbol[-1] == "*":  # noqa: PLR2004
        return BonusLetterSlot(int(symbol[0]))

    msg = f"Encountered invlaid slot symbol: {symbol}."
    raise ValueError(msg)
