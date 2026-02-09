import random
from pygame import Rect
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velX = random.uniform(-20, 20)
        self.velY = random.uniform(-20, 20)
        self.size = random.randint(2,6)
        self.colour = (255,255,255)
        self.lifeTimer = random.randint(2,6) / 10

    def getRect(self):
        return Rect(self.x, self.y, self.size, self.size)

