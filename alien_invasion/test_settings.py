from alien_invasion import AlienInvasion


class TestSettings:
    
    def setup_method(self):
        self.ai = AlienInvasion()
    
    def test_initialise_dynamic_settings(self):
        self.ai.settings.ship_speed = 5.0
        self.ai.settings.initialise_dynamic_settings()
        assert self.ai.settings.ship_speed == 2.0
    
    def test_increase_speed(self):
        self.ai.settings.increase_speed()
        assert self.ai.settings.ship_speed == 2.0 * 1.1