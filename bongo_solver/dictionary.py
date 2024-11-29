"""Class for storing a set of valid bongo words."""

from __future__ import annotations

from pathlib import Path

from bongo_solver.word_row import WordRow

WordList = set[str] | list[str]

WordLike = str | WordRow


def coerce_to_str(word: WordLike) -> str:
    """Coerce a word to a string."""
    if isinstance(word, WordRow):
        word = word.word
    return word


def coerce_to_set(words: WordList) -> set[str]:
    """Coerce a list of words to a set."""
    if isinstance(words, list):
        words = set(words)
    return words


def load_word_file(file_path: str | Path) -> set[str]:
    """Load a set of words from a text file."""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with file_path.open() as file:
        words = file.read().splitlines()
    return set(words)


class Dictionary:
    """Class for storing a set of valid bongo words."""

    @classmethod
    def from_text_files(
        cls,
        common_words_path: str | Path,
        valid_words_path: str | Path,
    ) -> Dictionary:
        """Initialize a dictionary with a set of words from a text file."""
        common_words = load_word_file(common_words_path)
        valid_words = load_word_file(valid_words_path)

        return cls(common_words, valid_words)

    @classmethod
    def from_directory(cls, directory: str | Path) -> Dictionary:
        """Initialize a dictionary with a set of words from a directory."""
        directory = Path(directory)
        common_words_path = directory / "common_words.txt"
        valid_words_path = directory / "valid_words.txt"

        return cls.from_text_files(common_words_path, valid_words_path)

    def __init__(
        self,
        common_words: WordList,
        valid_words: WordList,
    ) -> None:
        """Initialize the dictionary with a set of valid bongo words."""
        self.__common_words = coerce_to_set(common_words)
        self.__valid_words = coerce_to_set(valid_words) - self.__common_words

    @property
    def common_words(self) -> set[str]:
        """Return the set of common words."""
        return self.__common_words

    @property
    def valid_words(self) -> set[str]:
        """Return the set of valid words."""
        return self.__valid_words

    @property
    def all_words(self) -> set[str]:
        """Return the set of all words."""
        return self.__common_words | self.__valid_words

    def __contains__(self, word: WordLike) -> bool:
        """Return True if the word is in the dictionary."""
        word = coerce_to_str(word)
        return word in self.all_words

    def is_common(self, word: WordLike) -> bool:
        """Return True if the word is a common word."""
        word = coerce_to_str(word)
        return word in self.__common_words
