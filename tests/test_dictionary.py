"""Tests for the BongoDictionary class."""

import pytest

from bongo_solver.dictionary import BongoDictionary


def test_init__list__has_words() -> None:
    """Test that the dictionary is initialized with a list of words."""
    words = ["a", "b", "c"]
    dictionary = BongoDictionary(words)
    assert dictionary.words == set(words)


def test_init__set__has_words() -> None:
    """Test that the dictionary is initialized with a set of words."""
    words = {"a", "b", "c"}
    dictionary = BongoDictionary(words)
    assert dictionary.words == words


def test_from_text_file__file_exists__has_words() -> None:
    """Test that the dictionary is initialized with words from a text file."""
    file_path = "tests/fixtures/dictionary.txt"
    dictionary = BongoDictionary.from_text_file(file_path)
    assert dictionary.words == {"a", "b", "c"}


def test_from_text_file__file_does_not_exist__raises_error() -> None:
    """Test that an error is raised if the file does not exist."""
    file_path = "tests/fixtures/non_existent_file.txt"
    with pytest.raises(FileNotFoundError):
        BongoDictionary.from_text_file(file_path)
