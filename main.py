from pygame import init, mixer
from mainMenu import MainMenu
from sceneManager import SceneManager
from deathMenu import DeathMenu
from shopMenu import ShopMenu
from level import Level
import json
import os

def main():
    mixer.init()
    init()
    if not os.path.exists("data/data.json"):
        defaultData = {"coins": 0, "highestLevel" : 0, "healthUpgrade":0, "multijumpUpgrade":0}
        with open("data/data.json", "w") as f:
            json.dump(defaultData, f)

    manager = SceneManager(MainMenu, Level, MainMenu, DeathMenu, ShopMenu)
    manager.run()

if __name__ == "__main__":
    main()

"""
features to add:
- particle system
BUG: when jumping on the exit it double increments the level counter, no idea why
"""