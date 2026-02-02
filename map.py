from tile import Tile
from tile import TileType

class Map:
    TILE_SIZE = Tile.TILE_SIZE
    MAP_TILE_SIZE = 100 # 800x800 tile map, so 6400x6400 pixel map
    def __init__(self):
        self.mapGrid = []
        

    """
    currently a temp function to draw a random hardcoded map, will eventually generate a random map
    """
    def createMapGrid(self):
        for y in range(Map.MAP_TILE_SIZE):
            temp = [] # stores all x for a given y
            for x in range(Map.MAP_TILE_SIZE):
                temp.append(Tile(x, y))
            self.mapGrid.append(temp)
        for cell in self.mapGrid[99]:
            cell.tileType = TileType.BLOCK
        for cell in self.mapGrid[98]:
            cell.tileType = TileType.BLOCK

        for i in range(0, len(self.mapGrid), 3):
            for j in range(0, len(self.mapGrid[i]), 4):
                self.mapGrid[j][i].tileType = TileType.BLOCK
        self.mapGrid[98][20].tileType = TileType.SPIKE
        

    """
    debugging function to print out the grid in terminal
    """
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

