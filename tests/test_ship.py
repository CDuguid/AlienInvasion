from alien_invasion.alien_invasion import AlienInvasion
import pytest

@pytest.fixture
def ai():
    return AlienInvasion(testing=True)


class TestShip:
    
    def test_moving_left(self, ai):
        starting_x = ai.ship.x
        ai.ship.moving_left = True
        ai.ship.update()
        assert ai.ship.x < starting_x
    
    def test_left_boundary(self, ai):
        ai.ship.x = 0
        ai.ship.update()
        ai.ship.moving_left = True
        ai.ship.update()
        assert ai.ship.x == 0
    
    def test_centering(self, ai):
        ai.ship.x = 0
        ai.ship.centre_ship()
        expected = (ai.screen_width / 2, ai.screen_height)
        assert ai.ship.rect.midbottom == expected