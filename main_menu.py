import sys
from os import path
import pygame
import pygamepopup
from pygamepopup.components import Button, InfoBox, TextElement
from pygamepopup.menu_manager import MenuManager

images_dir = path.join(path.dirname(__file__), 'images')

class MainMenuScene:
    """A class to generate the main menu buttons for the game."""
    def __init__(self, ai_game):
        """Create the menu."""
        self.screen = ai_game.screen
        self.ai_game = ai_game
        self.menu_manager = MenuManager(self.screen)
        # Track whether the starting level has been increased
        self.level_modified = False

        self.create_main_menu_interface()

    def create_main_menu_interface(self):
        """Defines the menu buttons and what happens when clicked."""
        main_menu = InfoBox(
            "Main Menu",
            [
                [Button(title="Play", callback=lambda: self.play_game(), 
                        background_path=path.join(images_dir, "blue_box.png"),
                        background_hover_path=path.join(images_dir, "blue_box_hover.png"))],
                [Button(title="Help", callback=lambda: self.create_help_menu(), 
                        background_path=path.join(images_dir, "green_box.png"),
                        background_hover_path=path.join(images_dir, "green_box_hover.png"))],
                [Button(title="Increase Level", callback=lambda: self.increase_level(),
                        background_path=path.join(images_dir, "red_box.png"),
                        background_hover_path=path.join(images_dir, "red_box_hover.png"))],
                [Button(title="Reset Level", callback=lambda: self.reset_starting_difficulty(),
                        background_path=path.join(images_dir, "purple_box.png"),
                        background_hover_path=path.join(images_dir, "purple_box_hover.png"))],
                [Button(title="Exit", callback=lambda: self.exit())],
            ],
            has_close_button=False,
            background_path=path.join(images_dir, "grey_box.png")
        )
        self.menu_manager.open_menu(main_menu)

    def play_game(self):
        """Starts the game when Play is pressed."""
        self.ai_game.start_game()
    
    def create_help_menu(self):
        """Creates the help box popup."""
        help_menu = InfoBox(
            "Game Help",
            [
                [TextElement(text="Welcome to Alien Invasion!")],
                [TextElement(text="Earth is in danger from waves of marauding aliens "
                             "and you are the last line of defence. You must stop any of "
                             "the aliens from landing on the planet by shooting them down.")],
                [TextElement(text="Use the Left and Right arrow keys to position your ship "
                             "and use Spacebar to fire. Due to strict air traffic control "
                             "rules, there is a limit of 3 bullets that can be in the air "
                             "at any one time. A limited number of replacement ships have "
                             "been made available to you, indicated in the top left of the "
                             "screen. In the top right, you'll see your performance review. "
                             "Remember that departmental figures are down this year, so "
                             "we'd appreciate a good score while you save the planet.")],
                [TextElement(text="Press P to begin play, L to increase the "
                             "starting level, R to reset the starting level, "
                             "and Q to dishonourably surrender. Good luck, pilot.")]
            ],
            width=800,
        )
        self.menu_manager.open_menu(help_menu)
    
    def increase_level(self):
        """Increases the game's difficulty level."""
        self.ai_game.start_new_level()
        self.level_modified = True
    
    def reset_starting_difficulty(self):
        """Reverts the game's difficulty to level 1."""
        self.ai_game.settings.initialise_dynamic_settings()
        self.ai_game.stats.reset_level()
        self.ai_game.sb.prep_level()
        self.ai_game.empty_sprites()
        self.ai_game.create_fleet()

    def exit(self):
        """Quits the game."""
        sys.exit()

    def display(self) -> None:
        self.menu_manager.display()

    def motion(self, position: pygame.Vector2) -> None:
        self.menu_manager.motion(position)

    def click(self, button: int, position: pygame.Vector2) -> bool:
        self.menu_manager.click(button, position)