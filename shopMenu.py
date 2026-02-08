from menu import Menu
import pygame_menu
import json

class ShopItem:
    def __init__(self, abilityName, abilityKey, defaultAbilityCost, upgradable=True):
        self.abilityName = abilityName
        self.abilityKey = abilityKey
        self.defaultAbilityCost = defaultAbilityCost
        self.upgradable = upgradable


class ShopMenu(Menu):
    abilities = [
        ShopItem("Health upgrade", "healthUpgrade", 250),
        ShopItem("MultiJump", "multijumpUpgrade", 4000, upgradable=False)
    ]

    def __init__(self, sceneManager):
        super().__init__(sceneManager)
        with open("data/data.json", "r") as f:
            self.data = json.load(f)

        self.coins = self.data["coins"]
        self.customTheme.title = True
        self.menu.set_title("Shop")
        self.coinLabel = self.menu.add.label(f"{self.coins} coins")
        self.menu.add.vertical_margin(240)
        self.abilitiesContainer = {}
        for ability in ShopMenu.abilities:
            temp = []
            self.menu.add.vertical_margin(100)
            cost = self.getCost(ability)
            temp.append(self.menu.add.label(f"{ability.abilityName} {cost}"))
            if ability.upgradable or self.data[ability.abilityKey] == 0:
                temp.append(self.menu.add.button("Purchase", lambda a=ability: self.purchase(a)))
            else:
                temp.append(self.menu.add.button("Purchased", None))
            self.abilitiesContainer[ability.abilityKey] = temp
        self.menu.add.vertical_margin(150)
        self.menu.add.button('Exit', self.titleScreen)

    def getCost(self, ability):
        level = self.data[ability.abilityKey]
        return ability.defaultAbilityCost * ((2 ** (level + 1)))

    def purchase(self, ability):
        cost = self.getCost(ability)
        if self.coins < cost:
            return
        self.coins -= cost
        self.data["coins"] = self.coins
        self.data[ability.abilityKey] += 1
        with open("data/data.json", "w") as f:
            json.dump(self.data, f)
        self.coinLabel.set_title(f"{self.coins} coins")
        for ability in ShopMenu.abilities:
            key = ability.abilityKey
            label, button = self.abilitiesContainer[key]
            newCost = self.getCost(ability)
            label.set_title(f"{ability.abilityName} {newCost}")
            if not ability.upgradable and self.data[key] == 1:
                button.set_title("Purchased")
                button.readonly = True

    def titleScreen(self):
        self.sceneManager.changeScene(self.sceneManager.MainMenu)
