from alien_invasion.alien_invasion import AlienInvasion
import pytest


@pytest.fixture
def ai():
    return AlienInvasion(testing=True)


class TestGameStats:

    def test_reset_stats(self, ai):
        ai.stats.ships_left = 1
        ai.stats.score = 50
        ai.stats.reset_stats()
        assert ai.stats.ships_left == ai.settings.ship_limit and ai.stats.score == 0

    def test_reset_level(self, ai):
        ai.stats.level = 5
        ai.stats.reset_level()
        assert ai.stats.level == 1
