from alien_invasion.alien_invasion import AlienInvasion


class TestSettings:
    
    def setup_method(self):
        self.ai = AlienInvasion()
    
    def test_increase_level(self):
        self.ai.main_menu_scene.increase_level()
        assert self.ai.stats.level == 2
    
    def test_reset_starting_difficulty(self):
        self.ai.stats.level = 5
        self.ai.main_menu_scene.reset_starting_difficulty()
        assert self.ai.stats.level == 1