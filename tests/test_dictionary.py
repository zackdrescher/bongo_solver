"""Tests for the BongoDictionary class."""

from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

from bongo_solver.dictionary import Dictionary, coerce_to_str, load_word_file


def test_coerce_to_str__str__returns_str() -> None:
    """Test that the coerce_to_str function returns a string."""
    word = "test"
    assert coerce_to_str(word) == word


def test_load_word_file__path__opens() -> None:
    """Test that the load_word_file function loads words from a file."""
    # arrange
    mock_path = MagicMock(spec=Path)
    content = "a\nb\nc"
    mock_path.open = mock_open(read_data=content)

    expected = {"a", "b", "c"}

    # act
    result = load_word_file(mock_path)

    # assert
    assert result == expected
    mock_path.open.assert_called_once()


def test_load_word_file__str__opens() -> None:
    """Test that the load_word_file function loads words from a file."""
    # arrange
    file_path = "test.txt"
    content = "a\nb\nc"
    expected = {"a", "b", "c"}

    with patch("bongo_solver.dictionary.Path") as mock_path_class:
        mock_path_instance = MagicMock(spec=Path)
        mock_path_instance.open = mock_open(read_data=content)
        mock_path_class.return_value = mock_path_instance

        # act
        result = load_word_file(file_path)

        # assert
        assert result == expected
        mock_path_class.assert_called_once_with(file_path)
        mock_path_instance.open.assert_called_once()


def test_init__list__has_words() -> None:
    """Test that the dictionary is initialized with a list of words."""
    common_words = ["a", "b", "c"]
    valid_words = ["d", "e", "f"]
    dictionary = Dictionary(common_words, valid_words)
    assert dictionary.common_words == set(common_words)
    assert dictionary.valid_words == set(valid_words)
    assert dictionary.all_words == set(common_words + valid_words)


def test_init__set__has_words() -> None:
    """Test that the dictionary is initialized with a set of words."""
    common_words = {"a", "b", "c"}
    valid_words = {"d", "e", "f"}
    dictionary = Dictionary(common_words, valid_words)
    assert dictionary.common_words == common_words
    assert dictionary.valid_words == valid_words
    assert dictionary.all_words == common_words | valid_words


def test_init__duplicates__dedupes() -> None:
    """Test that the dictionary removes duplicates."""
    common_words = ["a", "b", "c"]
    valid_words = ["a", "d", "e", "f"]
    dictionary = Dictionary(common_words, valid_words)
    assert dictionary.common_words == {"a", "b", "c"}
    assert dictionary.valid_words == {"d", "e", "f"}
    assert dictionary.all_words == {"a", "b", "c", "d", "e", "f"}


def test_contains() -> None:
    """Test that the __contains__ method returns True for a valid word."""
    dictionary = Dictionary(["a"], ["b"])
    assert "a" in dictionary
    assert "b" in dictionary
    assert "c" not in dictionary


def test_is_common() -> None:
    """Test that the is_common method returns True for a common word."""
    dictionary = Dictionary(["a"], ["b"])
    assert dictionary.is_common("a")
    assert not dictionary.is_common("b")
    assert not dictionary.is_common("c")


def test_from_text_files() -> None:
    """Test that the from_text_files method creates a dictionary from text files."""
    common_words_path = "common.txt"
    valid_words_path = "valid.txt"
    common_words = ["a", "b", "c"]
    valid_words = ["d", "e", "f"]

    with patch("bongo_solver.dictionary.load_word_file") as mock_load:
        mock_load.side_effect = [set(common_words), set(valid_words)]
        dictionary = Dictionary.from_text_files(common_words_path, valid_words_path)

        mock_load.assert_has_calls(
            [call(common_words_path), call(valid_words_path)],
        )
        assert mock_load.call_count == 2

    assert dictionary.common_words == set(common_words)
    assert dictionary.valid_words == set(valid_words)
    assert dictionary.all_words == set(common_words + valid_words)


def test_from_directory() -> None:
    """Test that the from_directory method creates a dictionary from a directory."""
    directory = "test"

    with patch(
        "bongo_solver.dictionary.Dictionary.from_text_files",
        return_value=MagicMock(spec=Dictionary),
    ) as mock_from_text_files:
        Dictionary.from_directory(directory)

        mock_from_text_files.assert_called_once_with(
            Path(directory) / "common_words.txt",
            Path(directory) / "valid_words.txt",
        )
