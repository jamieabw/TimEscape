from pygame import Rect

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = (255, 255, 255)  # White color

    def getRect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def getColour(self):
        return self.color

