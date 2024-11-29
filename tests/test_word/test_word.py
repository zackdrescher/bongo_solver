"""Tests the Word class."""

from unittest.mock import MagicMock

import pytest

from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.base_letter_slot import LetterSlot
from bongo_solver.letter_tile import LetterTile
from bongo_solver.word.word import Word


def test_init__raises() -> None:
    """Test that a WordRow cannot be initialized with an invalid number of slots."""
    slots = [LetterSlot() for _ in range(4)]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(TypeError, match="Cannot instantiate the base class."):
        Word(slots, dictionary)


class ConcreteWord(Word):
    """Test concrete class for the Word class."""


def test_init__successful() -> None:
    """Test that a WordRow can be initialized."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)

    word_row = ConcreteWord(slots, dictionary)

    assert word_row.slots == slots
    assert word_row.dictionary == dictionary


def test_get_item__successful() -> None:
    """Test that a slot can be retrieved from a WordRow."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)
    word_row = ConcreteWord(slots, dictionary)

    slot = word_row[2]

    assert slot == slots[2]


def test_set_item__successful() -> None:
    """Test that a tile can be placed in a slot in a WordRow."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)
    word_row = ConcreteWord(slots, dictionary)

    tile = MagicMock(LetterTile)
    word_row[2] = tile

    assert word_row[2].letter_tile == tile


@pytest.mark.parametrize(
    ("indecies", "expected_word"),
    [
        ([], ""),
        ([0], "A"),
        ([1], "A"),
        ([2], "A"),
        ([3], "A"),
        ([4], "A"),
        ([0, 1], "AA"),
        ([1, 2], "AA"),
        ([2, 3], "AA"),
        ([3, 4], "AA"),
        ([0, 2], "A A"),
        ([1, 3], "A A"),
        ([2, 4], "A A"),
        ([0, 3], "A  A"),
        ([1, 4], "A  A"),
        ([0, 1, 2], "AAA"),
        ([1, 2, 3], "AAA"),
        ([2, 3, 4], "AAA"),
        ([0, 1, 3], "AA A"),
        ([0, 2, 3], "A AA"),
        ([1, 2, 4], "AA A"),
        ([1, 3, 4], "A AA"),
        ([0, 1, 4], "AA  A"),
        ([0, 2, 4], "A A A"),
        ([0, 3, 4], "A  AA"),
        ([0, 1, 2, 3], "AAAA"),
        ([1, 2, 3, 4], "AAAA"),
        ([0, 2, 3, 4], "A AAA"),
        ([0, 1, 3, 4], "AA AA"),
        ([0, 1, 2, 4], "AAA A"),
        ([0, 1, 2, 3, 4], "AAAAA"),
    ],
)
def test_word__with_tiles(indecies: list[int], expected_word: str) -> None:
    """Test that the word property returns the correct word when tiles are placed."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    word_row = ConcreteWord(slots, dictionary)

    def create_tile() -> MagicMock:
        tile = MagicMock(LetterTile)
        tile.letter = "A"
        return tile

    for index in indecies:
        word_row[index] = create_tile()

    word = word_row.word

    assert word == expected_word


@pytest.fixture
def score_tile() -> MagicMock:
    """Return a tile with a score of 10."""
    tile = MagicMock(LetterTile)
    tile.score = 10

    return tile


def test_score__not_valid__zero(score_tile: MagicMock) -> None:
    """Test that the score property returns 0 when the word is not valid."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    dictionary.is_common.return_value = False
    dictionary.__contains__.return_value = False
    word_row = ConcreteWord(slots, dictionary)

    word_row[0] = score_tile

    score = word_row.score

    assert score == 0


def test_score__valid__score(score_tile: MagicMock) -> None:
    """Test that the score property returns the score of the word when it is valid."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    dictionary.is_common.return_value = False
    dictionary.__contains__.return_value = True
    word_row = ConcreteWord(slots, dictionary)

    word_row[0] = score_tile

    score = word_row.score

    assert score == 10


def test_score__common__score(score_tile: MagicMock) -> None:
    """Test that the score returns 1.3 times the score of the word when it is common."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    dictionary.is_common.return_value = True
    dictionary.__contains__.return_value = False
    word_row = ConcreteWord(slots, dictionary)

    word_row[0] = score_tile

    score = word_row.score

    assert score == 13
