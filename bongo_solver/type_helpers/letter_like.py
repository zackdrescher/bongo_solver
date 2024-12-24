"""contains type and conversions for letter like types."""

from bongo_solver.letter import Letter
from bongo_solver.letter_tile import LetterTile

LetterLike = str | Letter | LetterTile


def coerce_to_letter(letter_like: LetterLike) -> Letter:
    """Coerce a letter-like object to a letter."""
    if isinstance(letter_like, LetterTile):
        letter_like = letter_like.letter
    if isinstance(letter_like, str):
        letter_like = Letter(letter_like)

    return letter_like
