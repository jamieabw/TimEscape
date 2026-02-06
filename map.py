from tile import Tile
from tile import TileType
from island import Island
from random import randrange, randint, choice, seed


X_TILES_GAP = 4 # maximum 14 tiles away x
Y_TILES_GAP = 3
SPAWN_TILE_X = 1
SPAWN_TILE_Y = 97

class Map:
    TILE_SIZE = Tile.TILE_SIZE
    MAP_TILE_SIZE = 100 # 800x800 tile map, so 6400x6400 pixel map
    def __init__(self, mapSeed):
        self.mapGrid = []
        self.islands = []
        seed(mapSeed)
        
        

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

        #self.mapGrid[Map.MAP_TILE_SIZE - 2][Map.MAP_TILE_SIZE - 2].tileType = TileType.EXIT
        self.populateWithIslands()
        #self.fillAmbientIslands()
        for island in self.islands:
            startTileX = int((island.x - (island.width // 2)) // Map.TILE_SIZE)
            startTileY = int((island.y - (island.height // 2))  // Map.TILE_SIZE)
            endTileX = int((island.x + (island.width // 2)) // Map.TILE_SIZE)
            endTileY = int((island.y + (island.height // 2))  // Map.TILE_SIZE)#
            for y in range(startTileY, endTileY):
                for x in range(startTileX, endTileX):
                    if x <= 2 or y >= Map.MAP_TILE_SIZE - 2 or x >= Map.MAP_TILE_SIZE - 2 or y <= 2:
                        continue # temp fix for bug involving being trapped inside spawn island
                    if x == startTileX or x == endTileX - 1  or y == endTileY - 1:
                        if randint(0,2) == 1:
                            continue
                    """
                    CRITICAL BUG HERE INVOLVING INDEX OUT OF BOUNDS
                    """
                    try:
                        self.mapGrid[y][x].tileType = TileType.BLOCK
                    except IndexError:
                        continue
        self.generateExit()
        self.populateWithSpikes()




    """
    Populates the map with path islands
    """
    def populateWithIslands(self):
        self.islands.append(Island(Map.TILE_SIZE * 10, Map.TILE_SIZE * 97, 4 * Map.TILE_SIZE, 4 * Map.TILE_SIZE))
        for i in range(100):
            for attempt in range(5):
                try:
                    self.islands.append(self.createPathIsland(self.islands[-1]))
                    break
                except IndexError:
                    break
    



    """
    Generates islands to fill the empty space in the map, some may be unreachable by the player
    """
    def fillAmbientIslands(self, count=250):
        counter = 0
        while counter < count:
            counter+= 1
            for attempt in range(5):

                x = randint(2, Map.MAP_TILE_SIZE - 2) * Map.TILE_SIZE
                y = randint(2, Map.MAP_TILE_SIZE - 2) * Map.TILE_SIZE

                width = randint(4, 10) * Map.TILE_SIZE
                height = randint(4, 10) * Map.TILE_SIZE

                island = Island(x, y, width, height)
                if not any(self.intersects(island, other) for other in self.islands):
                    self.islands.append(island)
                    break


        


        
    """
    Generates an island based on a previous island to ensure a reachable path is created for the player
    """
    def createPathIsland(self, prevIsland):
        xGap = (X_TILES_GAP + (randrange(4, 9) / 10)) * Map.TILE_SIZE
        yGap = (Y_TILES_GAP + (randrange(4, 9) / 10)) * Map.TILE_SIZE

        direction = choice([-1, 1, 1, 1, 1])

        width = randint(4, 8) * Map.TILE_SIZE
        height = randint(4, 6) * Map.TILE_SIZE

        newX = (
            prevIsland.x
            + direction * (prevIsland.width // 2 + width // 2)
            + direction * xGap
        )

        # top-to-top spacing
        prevTop = prevIsland.y - (prevIsland.height // 2)
        newTop = prevTop - yGap
        newY = newTop + (height // 2)

        island = Island(newX, newY, width, height)

        tileX = int(island.x // Map.TILE_SIZE)
        tileY = int(island.y // Map.TILE_SIZE)
        self.mapGrid[tileY][tileX]
        if tileY < 0 or tileX < 0:
            raise IndexError
        if any(self.intersects(island, other, paddingTiles=1) for other in self.islands):
            raise IndexError
        

        return island




    """def createPathIsland(self, prevIsland):
        xGap = (X_TILES_GAP + (randrange(4, 9) / 10)) * Map.TILE_SIZE
        yGap = (Y_TILES_GAP - (randrange(4,9) / 10)) * Map.TILE_SIZE

        direction = choice([-1, 1, 1, 1, 1])  # -1 = left, 1 = right

        width = randint(4, 10) * Map.TILE_SIZE
        height = randint(4, 8) * Map.TILE_SIZE

        newX = (
            prevIsland.x
            + direction * (prevIsland.width // 2 + width // 2)
            + direction * xGap
        )

        newY = prevIsland.y - (prevIsland.height // 2) - (height // 2) - yGap

        island = Island(newX, newY, width, height)

        tileX = int(island.x // Map.TILE_SIZE)
        tileY = int(island.y // Map.TILE_SIZE)
        self.mapGrid[tileY][tileX]  # bounds check

        return island"""

    """def createPathIsland(self, prevIsland):
        xGap = (X_TILES_GAP * (randrange(4, 9) / 10)) * Map.TILE_SIZE
        yGap = (Y_TILES_GAP * (randrange(4,9) / 10)) * Map.TILE_SIZE
        if randint(0,2) == 1:
            xGap *= -1
        width = randint(4, 10) * Map.TILE_SIZE
        height = randint(4, 8) * Map.TILE_SIZE
        island = Island(prevIsland.x + prevIsland.width + xGap, prevIsland.y - int(prevIsland.height // 2) - yGap, width, height)
        #island = Island(prevIsland.x +  xGap, prevIsland.y -  yGap, width, height)
        tileX = int(island.x // Map.TILE_SIZE)
        tileY = int(island.y // Map.TILE_SIZE)
        self.mapGrid[tileY][tileX]
        return island"""
    


    """
    Check if two objects are intersecting
    """
    def intersects(self, a, b, paddingTiles=2):
        pad = paddingTiles * Map.TILE_SIZE

        return not (
            a.x + a.width + pad <= b.x - pad or
            a.x - pad >= b.x + b.width + pad or
            a.y + a.height + pad <= b.y - pad or
            a.y - pad >= b.y + b.height + pad
        )
    

    def populateWithSpikes(self):
        for y in range(1, Map.MAP_TILE_SIZE):
            for x in range(2, Map.MAP_TILE_SIZE - 1):
                if self.mapGrid[y][x].tileType == TileType.BLOCK and self.mapGrid[y-1][x].tileType == TileType.EMPTY:
                    if randint(0,12) == 1:
                        self.mapGrid[y-1][x].tileType = TileType.SPIKE


    def generateExit(self):
        finalIsland = self.islands[-1]
        topOfIsland = finalIsland.y - (finalIsland.height // 2)
        x = finalIsland.x // Map.TILE_SIZE
        y = topOfIsland // Map.TILE_SIZE
        print(topOfIsland, y, x)
        self.mapGrid[int(y +1)][int(x)].tileType == TileType.EXIT


        

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

