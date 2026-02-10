class Island:
    def __init__(self, centreX, centreY, width, height):
        self.x = centreX
        self.y = centreY
        self.width = width
        self.height = height
        self.top = self.y - (self.height // 2)
        self.hasEnemy = False