from enum import Enum
from pygame import Rect
from random import randint
class Tile:
    TILE_SIZE = 64
    def __init__(self, tileX, tileY):
        self.tileX = tileX
        self.tileY = tileY
        self.x = self.tileX * Tile.TILE_SIZE
        self.y = self.tileY * Tile.TILE_SIZE
        self.tileType = TileType.EMPTY
        self.debuggingColors = (50,0,randint(0,255))
        # i believe these will be the top left corner of each cell?

    def getRect(self):
        return Rect(self.x, self.y, Tile.TILE_SIZE, Tile.TILE_SIZE)
    
    def getColour(self):
        if self.tileType == TileType.EMPTY:
            return self.debuggingColors
        elif self.tileType == TileType.BLOCK:
            return (0,0,0)
        elif self.tileType  == TileType.EXIT:
            return (0,255,0)
        elif self.tileType == TileType.SPIKE:
            return (255,0,0)
        else:
            print(self.tileType)
            raise ValueError("Invalid tile type")


class TileType(Enum):
    EMPTY = "EMPTY"
    BLOCK = "BLOCK"
    EXIT = "EXIT"
    SPIKE = "SPIKE"

