import pygame
import pygame_menu
from level import Level
from menu import Menu
import json

class MainMenu(Menu):
    def __init__(self, sceneManager):
        self.Level = Level
        super().__init__(sceneManager)
        with open("data/data.json", "r") as f:
            self.highScore = json.load(f)["highestLevel"]
        self.menu.add.label(
            "TimEscape",
            font_name=self.font,
            font_size=50,
            align=pygame_menu.locals.ALIGN_CENTER
        )
        self.menu.add.label(f"High score  {self.highScore}")

        self.menu.add.vertical_margin(80)
        self.menu.add.button('Play', self.startLevel)
        self.menu.add.button('Shop', self.startShop)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def startLevel(self):
        self.sceneManager.changeScene(self.sceneManager.Level)

    def startShop(self):
        self.sceneManager.changeScene(self.sceneManager.ShopMenu)

