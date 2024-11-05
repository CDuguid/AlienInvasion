from os import path
import pygame
from pygame.sprite import Sprite

images_dir = path.join(path.dirname(__file__), 'assets', 'images')

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_game):
        """Initialise the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.image = pygame.image.load(path.join(images_dir, 'green_alien.bmp')).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """Move the alien to the right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

class YellowAlien(Alien):
    """A class to represent a yellow alien in the fleet which shoots back."""
    
    def __init__(self, ai_game):
        """Initialise the alien and set its starting position."""
        super().__init__(ai_game)
        
        self.image = pygame.image.load(path.join(images_dir, 'yellow_alien.bmp')).convert_alpha()
        
class RedAlien(Alien):
    """A class to represent a red alien in the fleet which shoots back."""
    
    def __init__(self, ai_game):
        """Initialise the alien and set its starting position."""
        super().__init__(ai_game)
        
        self.image = pygame.image.load(path.join(images_dir, 'red_alien.bmp')).convert_alpha()      