import pygame

class SceneManager:
    def __init__(self, initialScene, Level, MainMenu, DeathMenu, ShopMenu):
        self.Level = Level
        self.MainMenu = MainMenu
        self.DeathMenu = DeathMenu
        self.ShopMenu = ShopMenu
        self.screen = pygame.display.set_mode((1800,1000))

        self.currentScene = initialScene(self)
         
    def changeScene(self, newScene):
        self.currentScene = newScene(self)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.currentScene.run(self.screen)
            pygame.display.flip()
            clock.tick(60)


