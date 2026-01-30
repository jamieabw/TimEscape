from enum import Enum
from pygame import Rect
class Tile:
    TILE_SIZE = 64
    def __init__(self, tileX, tileY):
        self.tileX = tileX
        self.tileY = tileY
        self.x = self.tileX * Tile.TILE_SIZE
        self.y = self.tileY * Tile.TILE_SIZE
        self.tileType = TileType.EMPTY
        # i believe these will be the top left corner of each cell?

    def getRect(self):
        return Rect(self.x, self.y, Tile.TILE_SIZE, Tile.TILE_SIZE)


class TileType(Enum):
    EMPTY = "EMPTY"
    BLOCK = "BLOCK"
    EXIT = "EXIT"
    SPIKE = "SPIKE"

