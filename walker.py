from enemy import Enemy # type: ignore
from random import randint
from pygame import draw
DEFAULT_MOVEMENT_SPEED = 75

class Walker(Enemy):
    def __init__(self, x, y, width, height, health, islands, map):
        super().__init__(x, y, width, height, health)
        island = self.getSpawnIsland(islands, map)
        
        self.x = island.x
        self.y = island.y - self.height - (island.height // 2)
        tileTop = int((island.y - (island.height // 2)) // map.TILE_SIZE)
        pixelTop = tileTop * map.TILE_SIZE

        self.y = pixelTop - self.height
        self.x = island.x - self.width // 2
        self.vel = DEFAULT_MOVEMENT_SPEED


    def getSpawnIsland(self, islands, map):
        islandChoice = None
        while islandChoice is None:
            islandChoice = islands[randint(0, len(islands) - 1)]
            try:
                if islandChoice.width < 3 or map.mapGrid[int((islandChoice.y - (islandChoice.height)) // map.TILE_SIZE)][int(islandChoice.x // map.TILE_SIZE)].tileType.name == "BLOCK":
                    islandChoice = None
            except IndexError:
                continue
                
        return islandChoice
    
        

    def movement(self, map, delta):
        if not self.alive:
            return
        try:
            if map.mapGrid[int(self.y // map.TILE_SIZE) + 1][(int(self.x + self.vel + (self.width // 2)) // map.TILE_SIZE)].tileType.name != "BLOCK":
                self.vel *= -1
            self.x += self.vel * delta
        except IndexError:
            self.alive = False # kill it if glitches, dont have time for a proper fix for this
