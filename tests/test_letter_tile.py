"""Contains tests for the LetterTile class."""

from unittest.mock import MagicMock

import pytest

from bongo_solver.letter import Letter
from bongo_solver.letter_tile import LetterTile


@pytest.fixture
def mock_try_get_letter_score(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch the letter_scores module."""
    mock_try_get_letter_score = MagicMock(return_value=1)
    monkeypatch.setattr(
        "bongo_solver.letter_tile.try_get_letter_score",
        mock_try_get_letter_score,
    )
    return mock_try_get_letter_score


def test_init__valid_letter_str__creates_letter_tile(
    mock_try_get_letter_score: MagicMock,
) -> None:
    """Test that a valid letter creates a LetterTile object."""
    letter_tile = LetterTile("A")
    assert str(letter_tile.letter) == "A"
    assert letter_tile.score == 1
    mock_try_get_letter_score.assert_called_once_with(Letter("A"))


def test_init__valid_letter__creates_letter_tile(
    mock_try_get_letter_score: MagicMock,
) -> None:
    """Test that a valid letter creates a LetterTile object."""
    letter = Letter("A")
    letter_tile = LetterTile(letter)
    assert str(letter_tile.letter) == "A"
    assert letter_tile.score == 1
    mock_try_get_letter_score.assert_called_once_with(letter)


def test_str__returns_string(mock_try_get_letter_score: MagicMock) -> None:
    """Test that the __str__ method returns a string."""
    letter_tile = LetterTile("A")
    assert str(letter_tile) == "A(1)"


def test_repr__returns_string(mock_try_get_letter_score: MagicMock) -> None:
    """Test that the __repr__ method returns a string."""
    letter_tile = LetterTile("A")
    assert repr(letter_tile) == "LetterTile(A, 1)"
