"""Contains the TilePool class and supporting methods."""

from __future__ import annotations

import re

from bongo_solver.letter import Letter

from .letter_tile import LetterTile

tile_quantity_patern = re.compile(r"([A-Za-z])\((\d+)\)\s?(\d?)")


class TilePool:
    """Contains a finite set of letter tiles."""

    @classmethod
    def from_str(cls, tile_str: str) -> TilePool:
        """Convert a string containing a tile pool configuration."""
        tiles = []
        for match in tile_quantity_patern.finditer(tile_str):
            letter = match.group(1)
            score = int(match.group(2))
            quantity = match.group(3)
            quantity = int(quantity) if quantity else None

            tile = LetterTile(letter, score)

            if quantity is None:
                tiles.append(tile)
            else:
                tiles.extend([tile] * quantity)

        return cls(tiles)

    def __init__(self, tiles: list[LetterTile] | None = None) -> None:
        """Initialize the tile pool."""
        if tiles is None:
            tiles = []
        self.__letter_dict: dict[Letter, list[LetterTile]] = {}
        for tile in tiles:
            if tile.letter in self.__letter_dict:
                self.__letter_dict[tile.letter].append(tile)
            else:
                self.__letter_dict[tile.letter] = [tile]

    def __getitem__(self, item: str | Letter | LetterTile) -> list[LetterTile]:
        """Get a tile from the pool."""
        if isinstance(item, LetterTile):
            item = item.letter
        if isinstance(item, str):
            item = Letter(item)

        return self.__letter_dict.get(item, [])

    def __contains__(self, item: str | LetterTile | Letter) -> bool:
        """Check if the pool contains a letter tile."""
        return bool(self[item])

    def __len__(self) -> int:
        """Return the number of tiles in the pool."""
        return sum(len(tiles) for tiles in self.__letter_dict.values())
