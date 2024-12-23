"""Tests for TilePool class."""

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
