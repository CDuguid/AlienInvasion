from alien_invasion.alien_invasion import AlienInvasion
from alien_invasion.alien import Alien
from alien_invasion.bullet import Bullet, YellowBullet, RedBullet
import pytest

@pytest.fixture
def ai():
    return AlienInvasion(testing=True)

@pytest.fixture
def alien(ai):
    return Alien(ai)

@pytest.fixture
def bullet(ai):
    return Bullet(ai)

@pytest.fixture
def alien_bullet(ai, alien):
    return YellowBullet(ai, alien)


class TestBullet:
    
    def test_update(self, bullet):
        starting_y = bullet.y
        bullet.update()
        assert bullet.y < starting_y

class TestAlienBullet:
    
    def test_update(self, alien_bullet):
        starting_y = alien_bullet.y
        alien_bullet.update()
        assert alien_bullet.y > starting_y