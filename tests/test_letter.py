import pytest

from bongo_solver.letter import Letter

from beartype.roar import BeartypeCallHintParamViolation


def test_init__valid_letter__creates_letter() -> None:
    """Test that a valid letter creates a Letter object."""
    letter = Letter("A")
    assert str(letter) == "A"


def test_init__non_string__raises() -> None:
    """Test that a non non typed input raises."""
    with pytest.raises(BeartypeCallHintParamViolation):
        Letter(1)  # type: ignore[arg-type]


def test_init__lower_letter__creates_letter() -> None:
    """Test that a valid letter creates a Letter object."""
    letter = Letter("a")
    assert str(letter) == "A"


@pytest.mark.parametrize("letter", ["1", "`", "abc", "Aa", " "])
def test_init__invalid_letter__raises_error(letter: str) -> None:
    """Test that an invalid letter raises an error."""
    match = "Letter must be a single character.|Letter must be a letter."
    with pytest.raises(ValueError, match=match):
        Letter(letter)


def test_eq__same_letter__returns_true() -> None:
    """Test that the __eq__ method returns True for the same letter."""
    letter1 = Letter("A")
    letter2 = Letter("A")
    assert letter1 == letter2


def test_eq__different_letter__returns_false() -> None:
    """Test that the __eq__ method returns False for different letters."""
    letter1 = Letter("A")
    letter2 = Letter("B")
    assert letter1 != letter2


def test_eq__same_letter_str__returns_true() -> None:
    """Test that the __eq__ method returns True for the same letter string."""
    letter = Letter("A")
    assert letter == "A"


def test_eq__same_letter_str_lower__returns_true() -> None:
    """Test that the __eq__ method returns True for the same letter string."""
    letter = Letter("A")
    assert letter == "a"


def test_eq__different_letter_str__returns_false() -> None:
    """Test that the __eq__ method returns False for different letter strings."""
    letter = Letter("A")
    assert letter != "B"


def test_eq__different_object__returns_false() -> None:
    """Test that the __eq__ method returns False for different objects."""
    letter = Letter("A")
    assert letter != 1


def test_repr__returns_string_representation() -> None:
    """Test that the __repr__ method returns a string representation."""
    letter = Letter("A")
    assert repr(letter) == "Letter('A')"
