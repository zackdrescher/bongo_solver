"""Type helpers for words."""

from bongo_solver.word_row import WordRow

WordLike = str | WordRow


def coerce_to_str(word: WordLike) -> str:
    """Coerce a word to a string."""
    if isinstance(word, WordRow):
        word = word.word
    return word
