from alien_invasion.alien_invasion import AlienInvasion
from alien_invasion.alien import Alien
from alien_invasion.explosion import Explosion
import unittest.mock as mock
import pygame
import pytest

@pytest.fixture
def ai():
    return AlienInvasion()

@pytest.fixture
def alien(ai):
    return Alien(ai)

@pytest.fixture
def explosion(alien):
    return Explosion(alien.rect.center)

class TestExplosion:
    
    @mock.patch("pygame.time.get_ticks")
    def test_update(self, mock_pygame_time_get_ticks, explosion):
        explosion.last_update = 0
        mock_pygame_time_get_ticks.return_value = explosion.frame_rate + 10
        explosion.update()
        assert explosion.image == explosion.explosion_animation[1]
        