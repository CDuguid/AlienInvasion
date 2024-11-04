from alien_invasion.alien_invasion import AlienInvasion
from alien_invasion.alien import Alien


class TestAlien:
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
    
    def test_update(self):
        starting_x = self.alien.x
        self.alien.update()
        assert self.alien.x > starting_x
    
    def test_check_edges(self):
        self.alien.rect.right = self.ai.screen_width
        self.alien.x = self.alien.rect.x
        assert self.alien.check_edges() == True
        