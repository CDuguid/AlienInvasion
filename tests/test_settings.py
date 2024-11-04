from alien_invasion.alien_invasion import AlienInvasion
import pytest

@pytest.fixture
def ai():
    return AlienInvasion()


class TestSettings:
    
    def test_initialise_dynamic_settings(self, ai):
        ai.settings.ship_speed = 5.0
        ai.settings.initialise_dynamic_settings()
        assert ai.settings.ship_speed == 2.0
    
    def test_increase_speed(self, ai):
        ai.settings.increase_speed()
        assert ai.settings.ship_speed == 2.0 * 1.1