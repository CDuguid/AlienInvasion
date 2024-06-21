import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    
    def __init__(self, ai_game):
        """Create a bullet at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour
        
        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)

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
        self.colour = self.settings.yellow_bullet_colour
        
        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midbottom = yellow_alien.rect.midbottom
        
        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet down the screen."""
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)

class RedBullet(Sprite):
    """A class to manage bullets fired from red aliens."""
    
    def __init__(self, ai_game, red_alien):
        """Create a bullet at the alien's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.red_bullet_colour
        
        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midbottom = red_alien.rect.midbottom
        
        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet down the screen."""
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)