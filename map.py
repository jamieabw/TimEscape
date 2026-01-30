from typing import override
from tile import Tile

class Map:
    TILE_SIZE = Tile.TILE_SIZE
    MAP_TILE_SIZE = 100 # 800x800 tile map, so 6400x6400 pixel map
    def __init__(self):
        self.mapGrid = []
        
    def createMapGrid(self):
        for y in range(Map.MAP_TILE_SIZE):
            temp = [] # stores all x for a given y
            for x in range(Map.MAP_TILE_SIZE):
                temp.append(Tile(x, y))
            self.mapGrid.append(temp)

    @override
    def __str__(self):
        result = ""
        for row in self.mapGrid:
            tempRow = []
            for tile in row:
                tempRow.append((tile.tileX, tile.tileY, tile.tileType.value))
            result += f"{tempRow}" + "\n"
        return result
    



if __name__ == "__main__":
    map = Map()
    map.createMapGrid()
    print(map)

