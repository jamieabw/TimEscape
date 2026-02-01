import pygame # type: ignore
import random
from map import Map
from player import Player
from tile import TileType

"""
CURRENTLY: there is a grid system, and a player (kind of?), there is momentum type physics and
gravity is already implemented, the camera has also been successfully implemented
TODO: 
- collisions - figure out the tiling indexes for the left, right, up, and down
- implement left and right movement
- proper map loading from file
- procedural map generation
- test hard coded map
- artwork

"""


# constants
FPS = 60
WIDTH = 30
HEIGHT = 30
DOWN_ACCELERATION = 10
MOVEMENT_ACCELERATION = 1.5
FRICTION_ACCELERATION = 1.5

def main():
    test = TestGame()
    test.run()

class TestGame:
    def __init__(self):
        self.delta = 0
        self.downVel = 0
        self.moveVel = 0
        self.tilesToCheck = ()
        self.pipes = []
        self.cameraX, self.cameraY = (0,0)
        self.map = Map()
        self.map.createMapGrid()


    # function to start the game
    def run(self):
        self.screen = pygame.display.set_mode((1000, 800))
        self.running = True
        self.clock = pygame.time.Clock()
        self.player = Player(200, 800)
        self.runLoop()

    
    def eventLoop(self):
        
        #self.checkCollision()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.isOnFloor:
                    self.player.y -= 10
                    self.downVel = -10


            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                if self.moveVel < 0:
                    self.moveVel = 0
                self.moveVel += (10 / FPS)
            if keys[pygame.K_a]:
                if self.moveVel > 0:
                    self.moveVel = 0
                self.moveVel -= (10 / FPS)

    def runLoop(self):
        while self.running:
            self.update()
            self.render()
            self.eventLoop()
            self.clock.tick(FPS)


    def render(self):
        self.screen.fill((0,0,0))
        for row in self.map.mapGrid:
            for tile in row:
                tempRect = tile.getRect()
                tempRect.x -= (self.cameraX)
                tempRect.y -= (self.cameraY)
                pygame.draw.rect(self.screen, tile.getColour(), tempRect)
        pygame.draw.rect(self.screen, self.player.getColour(), self.player.getRect().move(-self.cameraX, -self.cameraY))
        pygame.display.update()
        pygame.display.flip()

    """def update(self):
        self.getTilesToCheck()
        if not self.player.isOnFloor((self.tilesToCheck[2], self.tilesToCheck[3])):
            self.downVel += (DOWN_ACCELERATION / FPS)
        else:
            self.downVel = 0
        if self.moveVel != 0:
            self.moveVel = max(0, (self.moveVel - (FRICTION_ACCELERATION / FPS)))"""
    
    def update(self):
        if self.downVel != 0:
            self.player.isOnFloor = False # this if statement fixes jittering as when snapping to the top,
            # it would then fall again and consecutively trigger collisions, this is only a temporary fix thoa

        self.player.x += self.moveVel
        self.checkXCollision()
        self.downVel += (DOWN_ACCELERATION / FPS)
        self.player.y += self.downVel
        self.checkYCollision()

        if self.player.isOnFloor:
            self.downVel = 0
            print("yes")
        print(self.downVel)

        #self.player.x += self.moveVel
        # the following is camera physics
        self.cameraX = self.player.x - self.screen.get_width() // 2
        self.cameraX = min(max(0, self.cameraX), Map.TILE_SIZE * Map.MAP_TILE_SIZE - self.screen.get_width())
        self.cameraY = self.player.y - self.screen.get_height() // 2
        self.cameraY = min(max(0, self.cameraY), Map.TILE_SIZE * Map.MAP_TILE_SIZE - self.screen.get_height())


    def getTilesToCheck(self):
        # i need to somehow get this to be the index not thed pixel pos
        cornerCoords = self.getPlayerCornerCoords()
        self.tilesToCheck = []
        for x,y in cornerCoords:
            self.tilesToCheck.append(self.map.mapGrid[int(y)][int(x)])
        return self.tilesToCheck
    
    
    def testTiles(self):
        # debug function for checking if the tiling detection was correct
        for tile in self.tilesToCheck:
            tile.tileType = TileType.BLOCK
    
    def getPlayerCornerCoords(self):
        # gets each corner of the player rect hitbox for determining which tiles to check for collisions
        topLeft = (self.player.x // Map.TILE_SIZE, self.player.y // Map.TILE_SIZE)
        topRight= ((self.player.x + self.player.width) // Map.TILE_SIZE, self.player.y // Map.TILE_SIZE)
        bottomLeft = (self.player.x // Map.TILE_SIZE, (self.player.y + self.player.height) // Map.TILE_SIZE)
        bottomRight = ((self.player.x + self.player.width) // Map.TILE_SIZE, (self.player.y + self.player.height) // Map.TILE_SIZE)
        return [topLeft, topRight, bottomRight, bottomLeft]
    

    def checkXCollision(self):
        tiles = self.getTilesToCheck()
        for tile in tiles[:2]:
            if tile.tileType.name == "BLOCK" and self.player.getRect().colliderect(tile.getRect()):
                if self.moveVel > 0: # if moving right
                    self.player.x = tile.x - self.player.width
                elif self.moveVel < 0: # if moving left
                    self.player.x = tile.x + self.map.TILE_SIZE
                print("Xcollision")
                self.moveVel = 0
                break
                #self.downVel = 0
                #self.player.y = tile.y - self.player.height

    def checkYCollision(self):
        tiles = self.getTilesToCheck()
        for tile in tiles:
            if tile.tileType.name == "BLOCK" and self.player.getRect().colliderect(tile.getRect()):
                if self.downVel >= 0: # if falling
                    self.player.y = tile.y - self.player.height + 1 # this fixes the jittering by planting the player 1px into ground
                    self.player.isOnFloor = True
                    self.downVel = 0
                    return
                elif self.downVel <= 0: # if jumpingd
                    self.player.y = tile.y + self.map.TILE_SIZE
                    self.downVel = 0
                    return
        self.player.isOnFloor = False



        

if __name__ == "__main__":
    main()