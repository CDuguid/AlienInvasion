from os import path
import pygame
from pygame.sprite import Sprite

images_dir = path.join(path.dirname(__file__), 'images')

class Ship(Sprite):
    """A class to manage the ship."""
    
    def __init__(self, ai_game):
        """Initialise the ship and its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        # Load the ship image, get its rect and set the mask.
        self.image = pygame.image.load(path.join(images_dir, 'ship.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        # Start each new ship at the bottom centre of the screen.
        # For windowed mode, position manually or image is drawn below bottom of screen on laptop.
        # self.rect.midbottom = (625, 720)
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        
        # Movement flags; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on movement flags."""
        # Updates ship's x value, not its rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Update rect object from self.x
        self.rect.x = self.x
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        
    def centre_ship(self):
        """Centre the ship on the screen."""
        # In windowed mode, next line needs set to (625, 720) as above.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)