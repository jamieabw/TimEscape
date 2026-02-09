import pygame_menu

class Menu:
    def __init__(self, sceneManager):
        self.customTheme = pygame_menu.themes.THEME_DARK.copy()
        self.customTheme.background_color = (15, 15, 20)
        self.customTheme.title_background_color = (25, 25, 35)
        self.customTheme.widget_font_color = (220, 220, 220)
        self.customTheme.widget_selection_color = (100, 100, 255)
        self.customTheme.title = False
        self.font = pygame_menu.font.FONT_8BIT
        self.customTheme.title_font = self.font
        self.customTheme.widget_font = self.font
        self.customTheme.widget_font_size = 30
        self.customTheme.title_font_size = 50
        self.screen = sceneManager.screen
        self.sceneManager = sceneManager
        self.menu = pygame_menu.Menu("", self.screen.get_width(), self.screen.get_height(), theme=self.customTheme)

    def run(self, screen):
        self.menu.mainloop(screen, disable_loop=True)
        
        

