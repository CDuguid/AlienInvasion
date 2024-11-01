from alien_invasion import AlienInvasion
from alien import Alien
from explosion import Explosion
import unittest.mock as mock
import pygame

class TestExplosion:
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
        self.explosion = Explosion(self.alien.rect.center)
    
    @mock.patch("pygame.time.get_ticks")
    def test_update(self, mock_pygame_time_get_ticks):
        self.explosion.last_update = 0
        mock_pygame_time_get_ticks.return_value = self.explosion.frame_rate + 10
        self.explosion.update()
        assert self.explosion.image == self.explosion.explosion_animation[1]
        