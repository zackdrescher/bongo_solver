"""Contains the TilePool class and supporting methods."""

from __future__ import annotations

import re

from bongo_solver.letter import Letter
from bongo_solver.type_helpers.letter_like import coerce_to_letter

from .letter_tile import LetterTile

tile_quantity_patern = re.compile(r"([A-Za-z])\((\d+)\)\s?(\d?)")

VALIDATE_SCORES = True


def validate_scores(letter_dict: dict[Letter, list[LetterTile]]) -> bool:
    """Check that the scores of the tiles are consistent."""
    for tiles in letter_dict.values():
        if not all(tile.score == tiles[0].score for tile in tiles):
            return False
    return True


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

        if VALIDATE_SCORES and not validate_scores(self.__letter_dict):
            msg = "Scores of tiles are inconsistent."
            raise ValueError(msg)

    def __getitem__(self, item: str | Letter | LetterTile) -> list[LetterTile]:
        """Get a tile from the pool."""
        item = coerce_to_letter(item)

        return self.__letter_dict.get(item, [])

    def __contains__(self, item: str | LetterTile | Letter) -> bool:
        """Check if the pool contains a letter tile."""
        return bool(self[item])

    def __len__(self) -> int:
        """Return the number of tiles in the pool."""
        return sum(len(tiles) for tiles in self.__letter_dict.values())

    def count_by_letter(self) -> dict[Letter, int]:
        """Return the count of each letter in the pool."""
        return {letter: len(tiles) for letter, tiles in self.__letter_dict.items()}

    def score_by_letter(self) -> dict[Letter, int]:
        """Return the score of each letter in the pool."""
        return {letter: tiles[0].score for letter, tiles in self.__letter_dict.items()}

    def count_of(self, letter: str | Letter) -> int:
        """Return the count of a letter in the pool."""
        return len(self[letter])

    def score_of(self, letter: str | Letter) -> int | None:
        """Return the score of a letter in the pool."""
        letters = self[letter]
        if not letters:
            return None

        return letters[0].score

    def take(self, letter: str | Letter) -> LetterTile | None:
        """Take a letter from the pool."""
        letter = coerce_to_letter(letter)
        tiles = self[letter]

        if not tiles:
            return None

        tile = tiles.pop()

        if not tiles:
            del self.__letter_dict[letter]

        return tile

    def add(self, tile: LetterTile) -> None:
        """Add a tile to the pool."""
        if tile.letter in self.__letter_dict:
            tiles = self.__letter_dict[tile.letter]
            if VALIDATE_SCORES and not all(t.score == tile.score for t in tiles):
                msg = "New tile score does not match existing tiles."
                raise ValueError(msg)
            tiles.append(tile)
        else:
            self.__letter_dict[tile.letter] = [tile]
