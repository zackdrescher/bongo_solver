"""Type helpers for words."""

from bongo_solver.word.word import Word

WordLike = str | Word


def coerce_to_str(word: WordLike) -> str:
    """Coerce a word to a string."""
    if isinstance(word, Word):
        word = word.word
    return word
