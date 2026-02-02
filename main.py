from pygame import init
from menu import Menu
from sceneManager import SceneManager

def main(debug=False):
    init()
    SceneManager(Menu).beginScene(menu=True)

if __name__ == "__main__":
    main() 