from pygame import init
from menu import Menu
from sceneManager import SceneManager

def main(debug=False):
    init()
    SceneManager(Menu).beginScene(menu=True)

if __name__ == "__main__":
    main()

# broken map seeds:
# 6065102 weird vertical islands
#
#
"""
potential idea to incorporate the inaccesibility of some islands as a feature of the game and to have a "multijump" ability
purchasable in the shop for a large amount which is similar to the debugging jumping mechanism

"""