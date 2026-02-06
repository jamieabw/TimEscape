import pygame
from level import Level
from menu import Menu

"""
the hope is that eventually a scene management system can be used to more efficiently change scenes (levels, menus) more
fluidly without annoying repeated code
"""
class SceneManager:
    def __init__(self, initialScene):
        self.currentScene = initialScene
        self.screen = pygame.display.set_mode((1800,1000))
         
    def changeScene(self, newScene):
        self.currentScene = newScene

    def beginScene(self, menu=False):
        if menu:
            self.currentScene(self.screen, self)
        else:
            self.currentScene.run(self.screen)


