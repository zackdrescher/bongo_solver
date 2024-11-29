"""Tests for the WordRow class."""

from unittest.mock import MagicMock

import pytest

from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.base_letter_slot import LetterSlot
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_tile import LetterTile
from bongo_solver.word_row import WordRow


def test_init__successful() -> None:
    """Test that a WordRow can be initialized."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)

    word_row = WordRow(slots, dictionary)

    assert word_row.slots == slots
    assert word_row.dictionary == dictionary


def test_init__invalid_length() -> None:
    """Test that a WordRow cannot be initialized with an invalid number of slots."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="A word row must contain 5 slots."):
        WordRow(slots, dictionary)


def test_init__too_many_bonus_slots() -> None:
    """Test that a WordRow cannot be initialized with more than one bonus slot."""
    slots = [
        LetterSlot(),
        BonusLetterSlot(),
        BonusLetterSlot(),
        LetterSlot(),
        LetterSlot(),
    ]
    dictionary = MagicMock(Dictionary)

    with pytest.raises(ValueError, match="A word row can only contain one bonus slot."):
        WordRow(slots, dictionary)


def test_get_item__successful() -> None:
    """Test that a slot can be retrieved from a WordRow."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

    slot = word_row[2]

    assert slot == slots[2]


def test_set_item__successful() -> None:
    """Test that a tile can be placed in a slot in a WordRow."""
    slots = [LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot(), LetterSlot()]
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

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
    word_row = WordRow(slots, dictionary)

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
    word_row = WordRow(slots, dictionary)

    word_row[0] = score_tile

    score = word_row.score

    assert score == 0


def test_score__valid__score(score_tile: MagicMock) -> None:
    """Test that the score property returns the score of the word when it is valid."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    dictionary.is_common.return_value = False
    dictionary.__contains__.return_value = True
    word_row = WordRow(slots, dictionary)

    word_row[0] = score_tile

    score = word_row.score

    assert score == 10


def test_score__common__score(score_tile: MagicMock) -> None:
    """Test that the score returns 1.3 times the score of the word when it is common."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    dictionary.is_common.return_value = True
    dictionary.__contains__.return_value = False
    word_row = WordRow(slots, dictionary)

    word_row[0] = score_tile

    score = word_row.score

    assert score == 13


def test_get_bonus_ix__no_bonus() -> None:
    """Test that get_bonus_ix returns -1 when there is no bonus slot."""
    slots = [LetterSlot() for _ in range(5)]
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

    bonus_ix = word_row.get_bonus_ix()

    assert bonus_ix == -1


@pytest.mark.parametrize("bonus_ix", [0, 1, 2, 3, 4])
def test_get_bonus_ix__with_bonus(bonus_ix: int) -> None:
    """Test that get_bonus_ix returns the index of the bonus slot."""
    slots = [LetterSlot() for _ in range(5)]
    slots[bonus_ix] = BonusLetterSlot()
    dictionary = MagicMock(Dictionary)
    word_row = WordRow(slots, dictionary)

    result = word_row.get_bonus_ix()

    assert result == bonus_ix
