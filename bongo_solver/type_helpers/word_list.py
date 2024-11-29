"""Type helpers for word lists."""

WordList = set[str] | list[str]


def coerce_to_set(words: WordList) -> set[str]:
    """Coerce a list of words to a set."""
    if isinstance(words, list):
        words = set(words)
    return words
