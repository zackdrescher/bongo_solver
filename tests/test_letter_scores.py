from pytest import MonkeyPatch, fixture, raises

from bongo_solver.letter import Letter
from bongo_solver.letter_scores import try_get_letter_score

TEST_LETTER_SCORES = {
    "A": 1,
}


@fixture
def mock_letter_scores(monkeypatch: MonkeyPatch) -> None:
    """Patch the letter_scores module."""
    monkeypatch.setattr("bongo_solver.letter_scores.LETTER_SCORES", TEST_LETTER_SCORES)


def test_try_get_letter_score__valid_letter__returns_score(
    mock_letter_scores: None,
) -> None:
    """Test that a valid letter returns the correct score."""
    letter = Letter("A")
    assert try_get_letter_score(letter) == 1


def test_try_get_letter_score__invalid_letter__raises_error(
    mock_letter_scores: None,
) -> None:
    """Test that an invalid letter raises an error."""
    letter = Letter("B")
    with raises(ValueError, match="Letter 'B' does not have a score defined."):
        try_get_letter_score(letter)


def test_try_get_letter_score__valid_letter_str__returns_score(
    mock_letter_scores: None,
) -> None:
    """Test that a valid letter string returns the correct score."""
    assert try_get_letter_score("A") == 1


def test_try_get_letter_score__invalid_letter_str__raises_error(
    mock_letter_scores: None,
) -> None:
    """Test that an invalid letter string raises an error."""
    with raises(ValueError, match="Letter 'B' does not have a score defined."):
        try_get_letter_score("B")
