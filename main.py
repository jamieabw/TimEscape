import pygame # type: ignore
import random
from map import Map

"""
CURRENTLY: there is a grid system, and a player (kind of?), there is momentum type physics and
gravity is already implemented, the camera has also been successfully implemented
TODO: 
- collisions
- test hard coded map
- artwork

"""


# constants
FPS = 60
WIDTH = 30
HEIGHT = 30
DOWN_ACCELERATION = 5
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
        self.pipes = []
        self.cameraX, self.cameraY = (0,0)
        self.map = Map()
        self.map.createMapGrid()


    # function to start the game
    def run(self):
        self.screen = pygame.display.set_mode((1000, 800))
        self.running = True
        self.clock = pygame.time.Clock()
        self.x, self.y = (200,0)
        self.runLoop()

    
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.downVel = -10
                if event.key == pygame.K_d: # this is currently only tapping, not holding FIX THIS
                    self.moveVel += MOVEMENT_ACCELERATION

    def runLoop(self):
        while self.running:
            self.eventLoop()
            self.update()
            self.render()
            self.clock.tick(FPS)


    def render(self):
        self.screen.fill((0,0,0))
        for row in self.map.mapGrid:
            for tile in row:
                tempRect = tile.getRect()
                tempRect.x -= (self.cameraX)
                tempRect.y -= (self.cameraY)
                pygame.draw.rect(self.screen, (255,0,0), tempRect, 1)
        pygame.draw.circle(self.screen, (255,255,255), (self.x - self.cameraX, self.y - self.cameraY), 50)
        pygame.display.update()
        pygame.display.flip()

    def update(self):
        self.downVel += (DOWN_ACCELERATION / FPS)
        if self.moveVel != 0:
            self.moveVel = max(0, (self.moveVel - (FRICTION_ACCELERATION / FPS)))

        self.y += self.downVel
        self.x += self.moveVel
        self.cameraX = self.x - self.screen.get_width() // 2
        self.cameraX = max(0, self.cameraX)
        self.cameraY = self.y - self.screen.get_height() // 2
        self.cameraY = max(0, self.cameraY)

        

if __name__ == "__main__":
    main()