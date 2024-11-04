from alien_invasion.alien_invasion import AlienInvasion
import pytest

@pytest.fixture
def ai():
    return AlienInvasion()


class TestSettings:
    
    def test_increase_level(self, ai):
        ai.main_menu_scene.increase_level()
        assert ai.stats.level == 2
    
    def test_reset_starting_difficulty(self, ai):
        ai.stats.level = 5
        ai.main_menu_scene.reset_starting_difficulty()
        assert ai.stats.level == 1