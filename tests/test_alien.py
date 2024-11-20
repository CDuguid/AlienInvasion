from alien_invasion.alien_invasion import AlienInvasion
from alien_invasion.alien import Alien
import pytest


@pytest.fixture
def ai():
    return AlienInvasion(testing=True)


@pytest.fixture
def alien(ai):
    return Alien(ai)


class TestAlien:

    def test_update(self, ai, alien):
        starting_x = alien.x
        alien.update()
        assert alien.x > starting_x

    def test_check_edges(self, ai, alien):
        alien.rect.right = ai.screen_width
        alien.x = alien.rect.x
        assert alien.check_edges() == True
