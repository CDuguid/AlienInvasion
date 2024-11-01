from alien_invasion import AlienInvasion
from alien import Alien
from bullet import Bullet, YellowBullet, RedBullet

class TestBullet:
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.bullet = Bullet(self.ai)
    
    def test_update(self):
        starting_y = self.bullet.y
        self.bullet.update()
        assert self.bullet.y < starting_y

class TestYellowBullet:
    """RedBullet's code is identical; no point in testing twice."""
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
        self.bullet = YellowBullet(self.ai, self.alien)
    
    def test_update(self):
        starting_y = self.bullet.y
        self.bullet.update()
        assert self.bullet.y > starting_y