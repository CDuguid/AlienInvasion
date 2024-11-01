from alien_invasion import AlienInvasion
from game_stats import GameStats


class TestGameStats:
    
    def setup_method(self):
        self.ai = AlienInvasion()
    
    def test_reset_stats(self):
        self.ai.stats.ships_left = 1
        self.ai.stats.score = 50
        self.ai.stats.reset_stats()
        assert self.ai.stats.ships_left == self.ai.settings.ship_limit and \
            self.ai.stats.score == 0
    
    def test_reset_level(self):
        self.ai.stats.level = 5
        self.ai.stats.reset_level()
        assert self.ai.stats.level == 1