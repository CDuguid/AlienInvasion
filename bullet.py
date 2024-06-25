import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    
    def __init__(self, ai_game):
        """Create a bullet at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
                
        self.image = pygame.image.load('images/player_bullet.bmp')
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    def blitme(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)

"""
class YellowBullet(Bullet):
    A class to manage bullets fired by yellow aliens.
    
    def __init__(self, ai_game, yellow_alien):
        Create a yellow bullet at the alien's current position.
        super().__init__(ai_game)
        # Overwrite bullet colour
        self.colour = self.settings.yellow_bullet_colour
        
        # Change starting position to the firing alien
        self.rect.midtop = yellow_alien.rect.midtop
    
    def update(self):
        Move the bullet down the screen.
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
"""

class YellowBullet(Sprite):
    """A class to manage bullets fired from yellow aliens."""
    
    def __init__(self, ai_game, yellow_alien):
        """Create a bullet at the alien's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.image = pygame.image.load('images/yellow_alien_bullet.bmp')
        self.rect = self.image.get_rect()
        self.rect.midtop = yellow_alien.rect.midtop
        
        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet down the screen."""
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    def blitme(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)

class RedBullet(Sprite):
    """A class to manage bullets fired from red aliens."""
    
    def __init__(self, ai_game, red_alien):
        """Create a bullet at the alien's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.image = pygame.image.load('images/red_alien_bullet.bmp')
        self.rect = self.image.get_rect()
        self.rect.midtop = red_alien.rect.midtop
        
        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet down the screen."""
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    def blitme(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)