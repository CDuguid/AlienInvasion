from os import path
import pygame
from pygame.sprite import Sprite

images_dir = path.join(path.dirname(__file__), 'images')

class Explosion(Sprite):
    """A class to manage explosions when sprites are shot."""
    
    def __init__(self, location):
        """Initialise the list of explosion images."""
        super().__init__()
        self.explosion_animation = []
        for i in range(6):
            filename = f"explosion{i}.png"
            img = pygame.image.load(path.join(images_dir, filename)).convert_alpha()
            self.explosion_animation.append(img)
        self.image = self.explosion_animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    
    def update(self):
        """Move through the animation."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_animation):
                self.kill()
            else:
                location = self.rect.center
                self.image = self.explosion_animation[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = location