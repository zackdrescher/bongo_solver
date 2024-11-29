"""Tests for the word_like module."""

from bongo_solver.type_helpers.word_like import coerce_to_str


def test_coerce_to_str__str__returns_str() -> None:
    """Test that the coerce_to_str function returns a string."""
    word = "test"
    assert coerce_to_str(word) == word
