import pygame # type: ignore
import random
from map import Map, SPAWN_TILE_X, SPAWN_TILE_Y
from player import Player
from tile import TileType
from walker import Walker
import json


# constants
FPS = 60
DOWN_ACCELERATION = 10 * FPS
JUMP_ACCELERATION = -10 * FPS
MOVEMENT_ACCELERATION = 20 * FPS
FRICTION_MULTIPLIER = 0.9 # yes this is hardcoded, leave me alomne
MAX_DOWN_VELOCITY = 25 * FPS
MAX_SIDEWAY_VELOCITY = 10 * FPS
MIN_MOVE_SPEED = 0
TIME_TO_REACH_MAX_MOV = MAX_SIDEWAY_VELOCITY / MOVEMENT_ACCELERATION
INITIAL_TIMER = 100



class Level:
    def __init__(self, sceneManager):
        self.sceneManager = sceneManager
        self.level = 0
        with open("data/data.json", "r") as f:
            self.data = json.load(f)
        if self.data["multijumpUpgrade"] > 0:
            self.multijump = 4
        else:
            self.multijump = 1
        self.blockImage = pygame.image.load("Assets/blockPLACEHOLDER3.png").convert_alpha()
        self.blockImage = pygame.transform.scale(self.blockImage, (Map.TILE_SIZE, Map.TILE_SIZE))

        self.exitImage = pygame.image.load("Assets/exitPLACEHOLDER.png").convert_alpha()
        self.exitImage = pygame.transform.scale(self.exitImage, (Map.TILE_SIZE, Map.TILE_SIZE))
        self.spikeImage = pygame.image.load("Assets/spikePLACEHOLDER.png").convert_alpha()

        self.enemyImage = pygame.image.load("Assets/enemyPLACEHOLDER.png").convert_alpha()

        self.font = pygame.font.Font("Assets/ThaleahFat.ttf", 64)
        self.background = pygame.image.load("Assets/background2.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (Map.TILE_SIZE * Map.MAP_TILE_SIZE, Map.TILE_SIZE * Map.MAP_TILE_SIZE))
        self.clockLoopAudio = pygame.mixer.Sound("Assets/clockLoop.wav")
        self.deathAudio = pygame.mixer.Sound("Assets/death.wav")
        self.enemyAttackAudio = pygame.mixer.Sound("Assets/enemyAttack.wav")
        self.playerAttackAudio = pygame.mixer.Sound("Assets/playerAttack.wav")
        self.jumpAudio = pygame.mixer.Sound("Assets/jump.wav")


    # function to start the game
    def run(self, screen):
        self.screen = screen#pygame.display.set_mode((1000, 800))
        self.running = True
        self.clock = pygame.time.Clock()
        self.startMap()
        self.runLoop()
        #self.sceneManager.changeScene( DeathMenu )
        #self.sceneManager.beginScene(menu=True)
        

    """
    Generate i enemies in the map
    """

    def generateEnemies(self, enemyCount=10):
        for i in range(enemyCount):
            self.enemies.append(Walker(0,0,50,50,100,self.map.islands, self.map))


    """
    Currently a test function, spawns enemies and checks for collisions, CHANGE THIS 
    """
    def renderEnemies(self):
        for enemy in self.enemies:
            if enemy.alive:
                enemy.movement(self.map, self.delta)
                tempRect = pygame.Rect(enemy.x - self.cameraX, enemy.y - self.cameraY, enemy.width, enemy.height)
                #pygame.draw.rect(self.screen, (255,255,255), tempRect)
                self.screen.blit(self.enemyImage, (tempRect.left, tempRect.top))

                

    """
    start a new map and reset all the player attributes which are not global to all maps
    """
    def startMap(self):
        self.level += 1
        if self.level > self.data["highestLevel"]:
            self.data["highestLevel"] = self.level
        self.player = Player(SPAWN_TILE_X * Map.TILE_SIZE, SPAWN_TILE_Y * Map.TILE_SIZE)
        seed = random.randint(0,10000000)
        print(f"MAP SEED: {seed}")
        self.map = Map(seed)
        self.map.createMapGrid()
        self.enemies = []
        self.generateEnemies()
        self.enemyAcceleration = 0
        self.delta = 0
        self.tilesToCheck = ()
        self.cameraX, self.cameraY = (0,0)
        self.collisionTypes = {"top": False, "bottom":False, "left":False,"right":False}
        self.airTimer =0
        self.timer = INITIAL_TIMER
        self.health = 3 + self.data["healthUpgrade"]
        self.downVel = 0
        self.moveVel = 0
        self.clockLoopAudio.play(loops=-1)


    
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
                if event.key == pygame.K_SPACE and self.airTimer < 0.1 * self.multijump:
                    self.jumpAudio.play()
                    self.downVel = JUMP_ACCELERATION
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.moveVel > 0: # moving right/facing right
                    print("facing right")
                    tempRect = pygame.rect.Rect((self.player.x + self.player.width), (self.player.y), self.player.width * 1.5, self.player.height)
                    self.screen.blit(self.spikeImage, (tempRect.x - self.cameraX, tempRect.y - self.cameraY))
                    self.weaponCollision(tempRect)
                    pygame.display.flip()
                    print(tempRect.x, tempRect.y)
                elif self.moveVel < 0: # moving left / facing left
                    print("facing left")
                    tempRect = pygame.rect.Rect((self.player.x -  (1.5 *self.player.width)), (self.player.y), self.player.width * 1.5, self.player.height)
                    self.screen.blit(self.spikeImage, (tempRect.x - self.cameraX, tempRect.y - self.cameraY))
                    self.weaponCollision(tempRect)
                    pygame.display.flip()
                    


        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if self.moveVel < 0:
                self.moveVel = 0
            self.moveVel = min(self.moveVel + (MOVEMENT_ACCELERATION * self.delta), MAX_SIDEWAY_VELOCITY)
        if keys[pygame.K_a]:
            if self.moveVel > 0:
                self.moveVel = 0
            self.moveVel = max(self.moveVel - (MOVEMENT_ACCELERATION * self.delta), -MAX_SIDEWAY_VELOCITY)
        if not ((pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d])):
            if self.moveVel > 0:
                self.moveVel = max(0, self.moveVel * FRICTION_MULTIPLIER * self.delta * FPS)
            elif self.moveVel < 0:
                self.moveVel = min(0, self.moveVel * FRICTION_MULTIPLIER * self.delta * FPS)

# idea for the weapon, create a rect and check for intersections


    """
    the game loop, the order of which functions are called 
    """
    def runLoop(self):
        while self.running:
            self.delta = self.clock.tick(FPS) / 1000
            self.render()
            self.eventLoop()
            self.update()

    """
    render loop, renders things onto the scren
    """
    def render(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (-self.cameraX, -self.cameraY))
        startX = min(int(self.cameraX // Map.TILE_SIZE), 100)
        endX   = min(int((self.cameraX + self.screen.get_width()) // (Map.TILE_SIZE - 1)) + 1, 100)
        startY = min(int(self.cameraY // Map.TILE_SIZE), 100)
        endY   = min(int((self.cameraY + self.screen.get_height()) // (Map.TILE_SIZE)) + 1, 100)
        # utilise above variables to optimise enemy spawning

        for y in range(startY, endY):
            for x in range(startX, endX):
                tempRect = self.map.mapGrid[y][x].getRect()
                tempRect.x -= (self.cameraX)
                tempRect.y -= (self.cameraY)
                #pygame.draw.rect(self.screen, self.map.mapGrid[y][x].getColour(), tempRect)
                if self.map.mapGrid[y][x].tileType.name == "BLOCK":
                    self.screen.blit(pygame.transform.flip(self.blockImage, (y * x + x) % 2, (x * y * x ** 2) % 2), (tempRect.x, tempRect.y))
                    
                elif self.map.mapGrid[y][x].tileType.name == "SPIKE":
                    #pygame.draw.rect(self.screen, self.map.mapGrid[y][x].getColour(), tempRect)
                    self.screen.blit(self.spikeImage, (tempRect.x, tempRect.y))
                elif self.map.mapGrid[y][x].tileType.name == "EXIT":
                    self.screen.blit(self.exitImage, (tempRect.x, tempRect.y))
                """else:
                    pygame.draw.rect(self.screen, self.map.mapGrid[y][x].getColour(), tempRect)"""
        pygame.draw.rect(self.screen, self.player.getColour(), self.player.getRect().move(-self.cameraX, -self.cameraY))
        self.renderEnemies()
        self.levelText = self.font.render(f"Level {self.level}", True, (255,255,255,0.54))
        self.timerText = self.font.render(f"{round(self.timer)}", True, (255,255,255,0.54))
        self.healthText = self.font.render(f"HP: {self.health}", True, (255,255,255,0.54))
        self.scoreText = self.font.render(f"Coins: {self.data['coins']}", True, (255,255,255,0.54))
        self.screen.blit(self.levelText, (0,0))
        self.screen.blit(self.timerText, (self.screen.get_width() //2, 0))
        self.screen.blit(self.healthText, (0, self.screen.get_height() - self.healthText.get_height()))
        self.screen.blit(self.scoreText, (0, self.screen.get_height() - self.healthText.get_height() - self.scoreText.get_height()))
        pygame.display.flip()
    
    """
    the update loop:
    - player movement
    - timer updates
    - collision checking
    - camera logic
    """
    def update(self):
        self.timer -= self.delta
        if self.timer <= 0:
            self.reset()
        if round(self.timer) % 2 == 0:
            self.clockLoopAudio.set_volume(self.clockLoopAudio.get_volume() * 2)
        if self.collisionTypes["bottom"]:
            self.airTimer = 0
        else:
            self.airTimer += self.delta
        self.moveVel += self.enemyAcceleration
        self.enemyAcceleration *= FRICTION_MULTIPLIER

        self.player.x += self.moveVel * self.delta
        self.newCollisionLogicX()

        self.downVel = min(MAX_DOWN_VELOCITY, self.downVel + (DOWN_ACCELERATION * self.delta))
        self.player.y += self.downVel * self.delta
        self.newCollisionLogicY()

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
            x = min(x, 99)
            y = min(y, 99)
            if self.player.getRect().colliderect(self.map.mapGrid[int(y)][int(x)].getRect()):
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
    def newCollisionLogicX(self):
        self.enemyCollisionLogicX()
        self.collisionTypes["left"] = False
        self.collisionTypes["right"] = False
        for tile in self.getTilesToCheck():
            if tile.tileType.name == "BLOCK":
                if self.moveVel > 0:
                    self.player.x = tile.x - self.player.width # self.player.left = tile.right
                    self.collisionTypes["right"] = True
                    self.moveVel = 0
                elif self.moveVel < 0:
                    self.player.x = tile.x + Map.TILE_SIZE
                    self.collisionTypes["left"] = True
                    self.moveVel = 0
            elif tile.tileType.name == "SPIKE":
                self.reset()

            elif tile.tileType.name == "EXIT":
                self.proceedToNextLevel()
                self.player.x, self.player.y = (SPAWN_TILE_X * Map.TILE_SIZE,SPAWN_TILE_Y* Map.TILE_SIZE) # fixes jumping to double increment level


    """
    Handles enemy collisions with the player, reduces health and check whether the player is now dead
    """
    def enemyCollisionLogicX(self):
        self.collisionTypes["left"] = False
        self.collisionTypes["right"] = False
        for enemy in self.enemies:
            if self.player.getRect().colliderect(enemy.getRect()):
                if self.moveVel < 0.5 * FPS and self.moveVel > -0.5 * FPS:
                    print(self.moveVel)
                    if enemy.vel > 0: # enemy moving right
                        self.player.x = enemy.x + enemy.width + 32
                        self.collisionTypes["left"] = True
                        self.enemyAcceleration = 2 * FPS
                    else:
                        self.player.x = enemy.x - self.player.width - 32
                        self.collisionTypes["right"] = True
                        self.enemyAcceleration = -2 * FPS
                elif self.moveVel > -0.5 * FPS:
                    self.player.x = enemy.x - self.player.width - 32
                    self.collisionTypes["right"] = True
                    self.enemyAcceleration = -2 * FPS
                elif self.moveVel < 0.5 * FPS:
                    self.player.x = enemy.x + enemy.width + 32
                    self.collisionTypes["left"] = True
                    self.enemyAcceleration = 2 * FPS

                self.health -= 1
                if self.health == 0:
                    self.reset()
                self.moveVel = 0
                self.enemyAttackAudio.play()

        


    """
    deals with collisions on the y-axis
    """
    def newCollisionLogicY(self):
        self.collisionTypes["top"] = False
        self.collisionTypes["bottom"] = False
        for tile in self.getTilesToCheck():
            if tile.tileType.name == "BLOCK":
                if self.downVel > 0:
                    self.player.y = tile.y - self.player.height
                    self.collisionTypes["bottom"] = True
                    self.downVel = 0
                elif self.downVel < 0:
                    self.player.y = tile.y + Map.TILE_SIZE
                    self.collisionTypes["top"] = True
                    self.downVel = 0
            elif tile.tileType.name == "SPIKE":
                self.reset()

            elif tile.tileType.name == "EXIT":
                self.proceedToNextLevel()
                self.player.x, self.player.y = (SPAWN_TILE_X * Map.TILE_SIZE,SPAWN_TILE_Y* Map.TILE_SIZE) # fixes jumping to double increment level


    def weaponCollision(self, weaponRect):
        collisionIndex = weaponRect.collidelist([enemy.getRect() for enemy in self.enemies])
        if collisionIndex != -1:
            self.enemies[collisionIndex].alive = False
            self.enemies.remove(self.enemies[collisionIndex])
            self.timer += 5
            self.data["coins"] += 10
            self.playerAttackAudio.play()



    def proceedToNextLevel(self):
        self.data["coins"] += INITIAL_TIMER - round(self.timer)
        self.clockLoopAudio.stop()
        self.startMap()
        
        


    """
    when player dies to spike or entity, reset everything
    """
    def reset(self):
        self.running = False
        self.clockLoopAudio.stop()
        self.deathAudio.play()
        with open("data/data.json", "w") as f:
            json.dump(self.data, f)
        self.sceneManager.changeScene(self.sceneManager.DeathMenu)  
