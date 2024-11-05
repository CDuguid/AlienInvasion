from os import path
import pygame
from pygame.sprite import Sprite

images_dir = path.join(path.dirname(__file__), 'assets', 'images')

class Ship(Sprite):
    """A class to manage the ship."""
    
    def __init__(self, ai_game):
        """Initialise the ship and its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        self.image = pygame.image.load(path.join(images_dir, 'ship.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        self.rect.x = self.x
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        
    def centre_ship(self):
        """Centre the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)