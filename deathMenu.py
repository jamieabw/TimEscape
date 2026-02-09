import pygame_menu
from menu import Menu

class DeathMenu(Menu):
    def __init__(self, sceneManager):
        super().__init__(sceneManager)
        self.menu.add.label("You Died", font_name=self.font, font_size=50, align=pygame_menu.locals.ALIGN_CENTER)    
        self.menu.add.vertical_margin(80)
        self.menu.add.button('Retry', self.retry)
        self.menu.add.button('Quit to title screen', self.titleScreen)

    def retry(self):
        self.sceneManager.changeScene(self.sceneManager.Level)

    def titleScreen(self):
        self.sceneManager.changeScene(self.sceneManager.MainMenu)
        

        
