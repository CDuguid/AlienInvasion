import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    
    def __init__(self, ai_game):
        """Create a bullet at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
                
        self.image = pygame.image.load('images/player_bullet.bmp').convert()
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


class YellowBullet(Bullet):
    """A class to manage bullets fired by yellow aliens."""
    
    def __init__(self, ai_game, yellow_alien):
        """Create a yellow bullet at the alien's current position."""
        super().__init__(ai_game)
        # Overwrite bullet image
        self.image = pygame.image.load('images/yellow_alien_bullet.bmp').convert()
        self.rect = self.image.get_rect()
        
        # Change starting position to the firing alien
        self.rect.midbottom = yellow_alien.rect.midbottom
        
        # Without this line, bullets appear at the height of the ship
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet down the screen."""
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y


class RedBullet(Bullet):
    """A class to manage bullets fired from red aliens."""
    
    def __init__(self, ai_game, red_alien):
        """Create a red bullet at the alien's current position."""
        super().__init__(ai_game)
        # Overwrite bullet image
        self.image = pygame.image.load('images/red_alien_bullet.bmp').convert()
        self.rect = self.image.get_rect()
        
        # Change starting position to the firing alien
        self.rect.midbottom = red_alien.rect.midbottom
        
        # Without this line, bullets appear at the height of the ship
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet down the screen."""
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y