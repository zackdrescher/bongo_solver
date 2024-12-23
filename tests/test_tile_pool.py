"""Tests for TilePool class."""

import pytest

from bongo_solver.letter import Letter
from bongo_solver.tile_pool import TilePool


def test_from_string__single__is_right() -> None:
    """Test that a single tile pool is created correctly."""
    string = "A(20)"

    result = TilePool.from_str(string)

    letter = result["A"]
    assert len(result) == 1
    assert letter[0] is not None
    assert letter[0].score == 20


def test_from_string__quantity__is_right() -> None:
    """Tests the quantity parsing is correct."""
    string = "A(20)2"

    result = TilePool.from_str(string)

    assert len(result) == 2
    assert all(tile.score == 20 for tile in result["A"])


def test_from_string__multiple__is_right() -> None:
    """Tests that multiple tiles are created correctly."""
    string = "A(20)2B(30)C(40)3"

    result = TilePool.from_str(string)

    assert len(result) == 6
    assert all(tile.score == 20 for tile in result["A"])
    assert all(tile.score == 30 for tile in result["B"])
    assert all(tile.score == 40 for tile in result["C"])


def test_init__no_tiles__is_empty() -> None:
    """Tests that an empty tile pool is created correctly."""
    result = TilePool()

    assert len(result) == 0


def test_get_item__str__is_right() -> None:
    """Tests that getting a letter from the pool is correct."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")

    result = pool["A"]

    assert len(result) == 2
    assert all(tile.score == 20 for tile in result)


def test_get_item__tile__is_right() -> None:
    """Tests that getting a tile from the pool is correct."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")

    result = pool[pool["A"][0]]

    assert len(result) == 2
    assert all(tile.score == 20 for tile in result)


def test_get_item__letter__is_right() -> None:
    """Tests that getting a letter from the pool is correct."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")

    result = pool[Letter("A")]

    assert len(result) == 2
    assert all(tile.score == 20 for tile in result)


def test_get_item__not_in_pool__is_empty() -> None:
    """Tests that getting a letter not in the pool is correct."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")

    result = pool["D"]

    assert len(result) == 0


def test_contains() -> None:
    """Tests that the contains method works correctly."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")
    assert "A" in pool
    assert "B" in pool
    assert "C" in pool
    assert "D" not in pool


def test_count_by_letter() -> None:
    """Tests that the count by letter method works correctly."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")
    result = pool.count_by_letter()
    assert result == {Letter("A"): 2, Letter("B"): 1, Letter("C"): 3}


def test_score_by_letter() -> None:
    """Tests that the score by letter method works correctly."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")
    result = pool.score_by_letter()
    assert result == {Letter("A"): 20, Letter("B"): 30, Letter("C"): 40}


def test_count_of() -> None:
    """Tests that the count of method works correctly."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")
    assert pool.count_of("A") == 2
    assert pool.count_of("B") == 1
    assert pool.count_of("C") == 3
    assert pool.count_of("D") == 0


def test_score_of() -> None:
    """Tests that the score of method works correctly."""
    pool = TilePool.from_str("A(20)2B(30)C(40)3")
    assert pool.score_of("A") == 20
    assert pool.score_of("B") == 30
    assert pool.score_of("C") == 40
    assert pool.score_of("D") is None


def test_validate_scores__not_valid__raises() -> None:
    """Tests that the validate scores function works correctly."""
    with pytest.raises(ValueError, match="Scores of tiles are inconsistent."):
        TilePool.from_str("A(20)2A(30)C(40)3D(10)")
