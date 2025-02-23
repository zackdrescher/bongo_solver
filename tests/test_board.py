"""Tests for the board module."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast
from unittest.mock import MagicMock, patch

import pytest

from bongo_solver.board import Board, try_get_bonus_word
from bongo_solver.dictionary import Dictionary
from bongo_solver.letter_slot.bonus_letter_slot import BonusLetterSlot
from bongo_solver.letter_slot.letter_slot import LetterSlot
from bongo_solver.word.bonus_word import BonusWord
from bongo_solver.word.word_row import WordRow

if TYPE_CHECKING:
    from collections.abc import Generator


def test_try_get_bonus_word__no_bonus__invalid() -> None:
    """Test that try_get_bonus_word returns False when there is no bonus slot."""
    mock_dictionary = MagicMock(Dictionary)
    rows = [MagicMock(WordRow) for _ in range(5)]
    for row in rows:
        row.get_bonus_ix.return_value = -1

    result = try_get_bonus_word(rows, mock_dictionary)  # type: ignore[arg-type]

    assert not result


def test_try_get_bonus_word__all_bonus__invalid() -> None:
    """Test that try_get_bonus_word returns True when the bonus slots are valid."""
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
def test_try_get_bonus_word__valid(bonus_ixs: list[int]) -> None:
    """Test that try_get_bonus_word returns True when the bonus slots are valid."""
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
def test_try_get_bonus_word__invalid(bonus_ixs: list[int]) -> None:
    """Test that try_get_bonus_word returns False when the bonus slots are invalid."""
    mock_dictionary = MagicMock(Dictionary)
    rows = [MagicMock(WordRow) for _ in range(5)]

    for i, ix in enumerate(bonus_ixs):
        rows[i].get_bonus_ix.return_value = ix
        rows[i].__getitem__.return_value = MagicMock(BonusLetterSlot)

    rows[-1].get_bonus_ix.return_value = -1

    result = try_get_bonus_word(rows, mock_dictionary)  # type: ignore[arg-type]

    assert not result


CONTENTS = "     "
ROW = f"[{CONTENTS}]"


@pytest.fixture
def mock_word_row__from_str() -> Generator[MagicMock, None, None]:
    """Patch the WordRow.from_str method with a MagicMock."""
    mock = MagicMock(WordRow)

    with patch(
        "bongo_solver.board.WordRow.from_str",
        return_value=mock,
    ) as mock_from_str:
        yield mock_from_str


@pytest.mark.parametrize(
    "str_board",
    ["", ROW, "".join([ROW] * 4), "\n".join([ROW] * 4)],
)
def test_from_str__invalid(mock_word_row__from_str: MagicMock, str_board: str) -> None:
    """Test that from_str raises a ValueError when the board string is invalid."""
    mock_dictionary = MagicMock(Dictionary)
    with pytest.raises(
        ValueError,
        match="Insufficient board configuration in board_str.",
    ):
        Board.from_str(str_board, mock_dictionary)

    mock_word_row__from_str.assert_not_called()


@pytest.fixture
def mock_try_get_bonus_word() -> Generator[MagicMock, None, None]:
    """Patch the try_get_bonus_word method with a MagicMock."""
    mock = MagicMock(BonusWord)
    with patch(
        "bongo_solver.board.try_get_bonus_word",
        return_value=mock,
    ) as mock_try_get_bonus_word:
        yield mock_try_get_bonus_word


@pytest.mark.parametrize(
    "str_board",
    ["".join([ROW] * 5), "\n".join([ROW] * 5)],
)
def test_from_str__valid__calls_from_str(
    mock_word_row__from_str: MagicMock,
    mock_try_get_bonus_word: MagicMock,
    str_board: str,
) -> None:
    """Test that from_str raises a ValueError when the board string is invalid."""
    mock_dictionary = MagicMock(Dictionary)
    Board.from_str(str_board, mock_dictionary)

    assert mock_word_row__from_str.call_count == 5
    mock_try_get_bonus_word.assert_called_once()


def test_init__invalid_rows(mock_try_get_bonus_word: MagicMock) -> None:
    """Test that the Board constructor raises a ValueError when the rows are invalid."""
    mock_dictionary = MagicMock(Dictionary)
    with pytest.raises(
        ValueError,
        match="A board must contain 5 rows.",
    ):
        Board([MagicMock(WordRow) for _ in range(4)], mock_dictionary)

    mock_try_get_bonus_word.assert_not_called()


def test_init__invalid_bonus_word() -> None:
    """Test  constructor raises a ValueError when the bonus word is invalid."""
    mock_dictionary = MagicMock(Dictionary)
    with patch(
        "bongo_solver.board.try_get_bonus_word",
        return_value=None,
    ) as mock_try_get_bonus_word:
        with pytest.raises(
            ValueError,
            match="The board does not have a valid bonus word configuration.",
        ):
            Board([MagicMock(WordRow) for _ in range(5)], mock_dictionary)

        mock_try_get_bonus_word.assert_called_once()


def test_init__valid(mock_try_get_bonus_word: MagicMock) -> None:
    """Test that the Board constructor initializes the object with valid arguments."""
    mock_dictionary = MagicMock(Dictionary)

    board = Board([MagicMock(WordRow) for _ in range(5)], mock_dictionary)

    assert board
    mock_try_get_bonus_word.assert_called_once()


def test_get_position_slot__invalid_position__raises(
    monkeypatch: pytest.MonkeyPatch,
    mock_try_get_bonus_word: MagicMock,
) -> None:
    """Test that get_position_slot raises index error when positon is invalid."""
    check_position_mock = MagicMock()
    check_position_mock.return_value = False

    monkeypatch.setattr("bongo_solver.board.position_valid", check_position_mock)

    mock_dictionary = MagicMock(Dictionary)

    row_mock = MagicMock(WordRow)
    row_mock.__getitem__.return_value = MagicMock(LetterSlot)

    board = Board([row_mock for _ in range(5)], mock_dictionary)

    p = (1, 2)
    with pytest.raises(IndexError):
        board.get_position_slot(p)

    check_position_mock.assert_called_once_with(p)


def test_get_position_slot__position__returns(
    mock_try_get_bonus_word: MagicMock,
) -> None:
    """Test that get_position_slot raises index error when positon is invalid."""
    # arrange
    mock_dictionary = MagicMock(Dictionary)

    slot_mock = MagicMock(LetterSlot)

    row_mocks = [
        MagicMock(WordRow),
        MagicMock(WordRow),
        MagicMock(WordRow),
        MagicMock(WordRow),
        MagicMock(WordRow),
    ]

    for row_mock in row_mocks:
        row_mock.__getitem__.return_value = slot_mock

    board = Board([cast(WordRow, i) for i in row_mocks], mock_dictionary)

    p = (1, 2)

    # act
    result = board.get_position_slot(p)

    assert result is slot_mock

    # assert
    i, j = p

    for ix, row in enumerate(row_mocks):
        if ix != i:
            row.__getitem__.assert_not_called()
        else:
            row.__getitem__.assert_called_once_with(j)


# TODO: (ZD) TEST PLACE TILE
