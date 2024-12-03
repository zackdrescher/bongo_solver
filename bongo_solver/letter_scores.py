"""Contains the point value of each letter in Bongo."""

from __future__ import annotations

from .letter import Letter


def try_get_letter_score(letter: str | Letter) -> int:
    """Return the point value of the given letter."""
    if isinstance(letter, str):
        letter = Letter(letter)

    try:
        return LETTER_SCORES[letter.letter]
    except KeyError as e:
        msg = f"Letter '{letter}' does not have a score defined."
        raise ValueError(msg) from e


LETTER_SCORES = {
    "V": 85,
    "F": 65,
    "K": 50,
    "B": 45,
    "G": 45,
    "C": 40,
    "H": 40,
    "P": 35,
    "N": 20,
    "T": 10,
    "I": 9,
    "O": 7,
    "R": 7,
    "A": 5,
    "E": 5,
    "S": 5,
}
