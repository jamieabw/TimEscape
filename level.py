import pygame # type: ignore
import random
from map import Map
from player import Player
from tile import TileType

"""
CURRENTLY: there is a grid system, and a player (kind of?), there is momentum type physics and
gravity is already implemented, the camera has also been successfully implemented
TODO: 
- add spike generation
- test entity spawning
- entity pathfinding
- exit / entrance implementation
- timer implementation
- better movement physics

"""


# constants
FPS = 60
DOWN_ACCELERATION = 10
MOVEMENT_ACCELERATION = 1.5
FRICTION_ACCELERATION = 1.5

class Level:
    def __init__(self):
        self.delta = 0
        self.tilesToCheck = ()
        self.cameraX, self.cameraY = (0,0)


    # function to start the game
    def run(self, screen):
        self.screen = screen#pygame.display.set_mode((1000, 800))
        self.running = True
        self.clock = pygame.time.Clock()
        self.startMap()
        self.runLoop()


    """
    start a new map and reset all the player attributes which are not global to all maps
    """
    def startMap(self):
        self.player = Player(200, 800)
        self.map = Map()
        self.map.createMapGrid()
        self.downVel = 0
        self.moveVel = 0

    
    """
    loop for events such as inputs
    """
    def eventLoop(self):
        
        #self.checkCollision()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()

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


    """
    the game loop, the order of which functions are called 
    """
    def runLoop(self):
        while self.running:
            self.update()
            self.render()
            self.eventLoop()
            self.clock.tick(FPS)

    """
    render loop, renders things onto the scren
    """
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
    
    """
    the update loop:
    - player movement
    - timer updates
    - collision checking
    - camera logic
    """
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
        print(self.downVel)

        #self.player.x += self.moveVel
        # the following is camera physics
        self.cameraX = self.player.x - self.screen.get_width() // 2
        self.cameraX = min(max(0, self.cameraX), Map.TILE_SIZE * Map.MAP_TILE_SIZE - self.screen.get_width())
        self.cameraY = self.player.y - self.screen.get_height() // 2
        self.cameraY = min(max(0, self.cameraY), Map.TILE_SIZE * Map.MAP_TILE_SIZE - self.screen.get_height())

    """
    creates a list of coordinates to use for grid calculations
    """
    def getTilesToCheck(self):
        # i need to somehow get this to be the index not thed pixel pos
        cornerCoords = self.getPlayerCornerCoords()
        self.tilesToCheck = []
        for x,y in cornerCoords:
            self.tilesToCheck.append(self.map.mapGrid[int(y)][int(x)])
        return self.tilesToCheck
    
    

    """
    debugging function to permanently colour boxes which are being checked for collisions with the player
    """
    def testTiles(self):
        # debug function for checking if the tiling detection was correct
        for tile in self.tilesToCheck:
            tile.tileType = TileType.BLOCK
    


    """
    get the coordinates of each corner of the player's hitboxes to determine which tiles to check
    for collisions
    """
    def getPlayerCornerCoords(self):
        # gets each corner of the player rect hitbox for determining which tiles to check for collisions
        topLeft = (self.player.x // Map.TILE_SIZE, self.player.y // Map.TILE_SIZE)
        topRight= ((self.player.x + self.player.width) // Map.TILE_SIZE, self.player.y // Map.TILE_SIZE)
        bottomLeft = (self.player.x // Map.TILE_SIZE, (self.player.y + self.player.height) // Map.TILE_SIZE)
        bottomRight = ((self.player.x + self.player.width) // Map.TILE_SIZE, (self.player.y + self.player.height) // Map.TILE_SIZE)
        return [topLeft, topRight, bottomRight, bottomLeft]
    


    """
    deals with collisions on the x-axis
    """
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


    """
    COLLISION BUG URGENT:
    - when velocity is negative (Acting upwards), and a collision with a side of a block, the player
    will teleport to the bottom of the object, this seems to the reverse of the clipping to the top of an object
    issue which is experienced during falling, this needs to be urgently fixed as makes gameplay terrible
    """


    """
    deals with collisions on the y-axis
    """
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
            elif tile.tileType.name == "SPIKE" and self.player.getRect().colliderect(tile.getRect()):
                self.reset()
        self.player.isOnFloor = False


    """
    when player dies to spike or entity, reset everything
    """
    def reset(self):
        self.startMap()
