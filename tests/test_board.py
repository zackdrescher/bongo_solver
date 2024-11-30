"""Tests for the board module."""

from unittest.mock import MagicMock

import pytest

from bongo_solver.board import try_get_bonus_word
from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.word.word_row import WordRow


def test_validate_bonus_slots__no_bonus__invalid() -> None:
    """Test that validate_bonus_slots returns False when there is no bonus slot."""
    mock_dictionary = MagicMock(Dictionary)
    rows = [MagicMock(WordRow) for _ in range(5)]
    for row in rows:
        row.get_bonus_ix.return_value = -1

    result = try_get_bonus_word(rows, mock_dictionary)  # type: ignore[arg-type]

    assert not result


def test_validate_bonus_slots__all_bonus__invalid() -> None:
    """Test that validate_bonus_slots returns True when the bonus slots are valid."""
    mock_dictionary = MagicMock(Dictionary)
    rows = [MagicMock(WordRow) for _ in range(5)]
    for row in rows:
        row.get_bonus_ix.return_value = 1

    result = try_get_bonus_word(rows, mock_dictionary)  # type: ignore[arg-type]

    assert not result


@pytest.mark.parametrize(
    "bonus_ixs",
    [[0, 0, 0, 0], [0, 1, 2, 3], [4, 3, 2, 1], [0, 1, 0, 1]],
)
def test_validate_bonus_slots__valid(bonus_ixs: list[int]) -> None:
    """Test that validate_bonus_slots returns True when the bonus slots are valid."""
    mock_dictionary = MagicMock(Dictionary)
    rows = [MagicMock(WordRow) for _ in range(5)]

    mock_bonus_slots = []
    for i, ix in enumerate(bonus_ixs):
        rows[i].get_bonus_ix.return_value = ix
        mock_slot = MagicMock(BonusLetterSlot)
        rows[i].__getitem__.return_value = mock_slot
        mock_bonus_slots.append(mock_slot)

    rows[-1].get_bonus_ix.return_value = -1

    result = try_get_bonus_word(rows, mock_dictionary)  # type: ignore[arg-type]

    assert result
    assert result.slots == mock_bonus_slots


@pytest.mark.parametrize(
    "bonus_ixs",
    [
        [0, -1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
        [0, 2, 2, 2],
        [4, 4, 2, 1],
        [0, 1, 0, 4],
    ],
)
def test_validate_bonus_slots__invalid(bonus_ixs: list[int]) -> None:
    """Test that validate_bonus_slots returns False when the bonus slots are invalid."""
    mock_dictionary = MagicMock(Dictionary)
    rows = [MagicMock(WordRow) for _ in range(5)]

    for i, ix in enumerate(bonus_ixs):
        rows[i].get_bonus_ix.return_value = ix
        rows[i].__getitem__.return_value = MagicMock(BonusLetterSlot)

    rows[-1].get_bonus_ix.return_value = -1

    result = try_get_bonus_word(rows, mock_dictionary)  # type: ignore[arg-type]

    assert not result
