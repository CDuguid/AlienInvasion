from alien_invasion.alien_invasion import AlienInvasion


class TestShip:
    
    def setup_method(self):
        self.ai = AlienInvasion()
    
    def test_moving_left(self):
        starting_x = self.ai.ship.x
        self.ai.ship.moving_left = True
        self.ai.ship.update()
        assert self.ai.ship.x < starting_x
    
    def test_left_boundary(self):
        self.ai.ship.x = 0
        self.ai.ship.update()
        self.ai.ship.moving_left = True
        self.ai.ship.update()
        assert self.ai.ship.x == 0
    
    def test_centering(self):
        self.ai.ship.x = 0
        self.ai.ship.centre_ship()
        expected = (self.ai.screen_width / 2, self.ai.screen_height)
        assert self.ai.ship.rect.midbottom == expected