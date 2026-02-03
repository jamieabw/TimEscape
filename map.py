from tile import Tile
from tile import TileType
from island import Island
from random import randrange, randint


X_TILES_GAP = 6 # maximum 14 tiles away x
Y_TILES_GAP = 2
SPAWN_TILE_X = 1
SPAWN_TILE_Y = 98

class Map:
    TILE_SIZE = Tile.TILE_SIZE
    MAP_TILE_SIZE = 100 # 800x800 tile map, so 6400x6400 pixel map
    def __init__(self):
        self.mapGrid = []
        self.islands = []
        

    """
    currently a temp function to draw a random hardcoded map, will eventually generate a random map
    """
    def createMapGrid(self):
        for y in range(Map.MAP_TILE_SIZE):
            temp = [] # stores all x for a given y
            for x in range(Map.MAP_TILE_SIZE):
                temp.append(Tile(x, y))
            self.mapGrid.append(temp)
        for cell in self.mapGrid[Map.MAP_TILE_SIZE-1]:
            cell.tileType = TileType.BLOCK
        for cell in self.mapGrid[0]:
            cell.tileType = TileType.BLOCK
        for i in range(Map.MAP_TILE_SIZE):
            self.mapGrid[i][0].tileType = TileType.BLOCK
            self.mapGrid[i][Map.MAP_TILE_SIZE-1].tileType = TileType.BLOCK

        self.mapGrid[Map.MAP_TILE_SIZE - 2][Map.MAP_TILE_SIZE - 2].tileType = TileType.EXIT
        self.populateWithIslands()

    def populateWithIslands(self):
        self.islands.append(self.createIsland(Island(SPAWN_TILE_X * Map.TILE_SIZE, SPAWN_TILE_Y * Map.TILE_SIZE,0,0)))
        for i in range(100):
            try:
                self.islands.append(self.createIsland(self.islands[-1]))
            except IndexError:
                break
        for island in self.islands:
            print(island.x)
            tileX = int(island.x // Map.TILE_SIZE)
            tileY = int(island.y // Map.TILE_SIZE)
            self.mapGrid[tileY][tileX].tileType = TileType.BLOCK

    def createIsland(self, prevIsland):
        xGap = (X_TILES_GAP * (randrange(4, 9) / 10)) * Map.TILE_SIZE
        yGap = (Y_TILES_GAP * (randrange(4,9) / 10)) * Map.TILE_SIZE
        width = randint(2, 4) * Map.TILE_SIZE
        height = randint(2, 4) * Map.TILE_SIZE
        island = Island(prevIsland.x + prevIsland.width + xGap, prevIsland.y - prevIsland.height - yGap, width, height)
        island = Island(prevIsland.x +  xGap, prevIsland.y -  yGap, width, height)
        tileX = int(island.x // Map.TILE_SIZE)
        tileY = int(island.y // Map.TILE_SIZE)
        self.mapGrid[tileY][tileX]
        return island
        

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

