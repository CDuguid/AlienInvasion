import sys
import pygame
import pygamepopup
from pygamepopup.components import Button, InfoBox, TextElement
from pygamepopup.menu_manager import MenuManager


class MainMenuScene:
    """A class to generate the main menu buttons for the game."""
    def __init__(self, ai_game):
        """Create the menu."""
        self.screen = ai_game.screen
        self.ai_game = ai_game
        self.menu_manager = MenuManager(self.screen)

        self.create_main_menu_interface()

    def create_main_menu_interface(self):
        """Defines the menu buttons and what happens when clicked."""
        main_menu = InfoBox(
            "Main Menu",
            [
                [Button(title="Play", callback=lambda: self.play_game(), 
                        background_path="images/blue_box.png",
                        background_hover_path="images/blue_box_hover.png")],
                [Button(title="Help", callback=lambda: self.create_help_menu(), 
                        background_path="images/green_box.png",
                        background_hover_path="images/green_box_hover.png")],
                [Button(title="Exit", callback=lambda: self.exit(), 
                        background_path="images/red_box.png",
                        background_hover_path="images/red_box_hover.png")],
            ],
            has_close_button=False,
            background_path="images/grey_box.png"
        )
        self.menu_manager.open_menu(main_menu)

    def play_game(self):
        self.ai_game.start_game()
    
    def create_help_menu(self):
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
                [TextElement(text="Press p to begin play, h for this help and q to "
                             "dishonourably surrender. Good luck, pilot.")]
            ],
            width=800,
        )
        self.menu_manager.open_menu(help_menu)

    def exit(self):
        sys.exit()

    def display(self) -> None:
        self.menu_manager.display()

    def motion(self, position: pygame.Vector2) -> None:
        self.menu_manager.motion(position)

    def click(self, button: int, position: pygame.Vector2) -> bool:
        self.menu_manager.click(button, position)