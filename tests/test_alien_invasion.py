from alien_invasion.alien_invasion import AlienInvasion
from alien_invasion.alien import Alien
from alien_invasion.bullet import Bullet, YellowBullet, RedBullet
import unittest.mock as mock
import pygame
import pytest


class TestSpriteCreation:
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
        self.ai.aliens.add(self.alien)
    
    # test fire_bullet adds a bullet to group and has upper limit
    @pytest.mark.parametrize("bullets_fired, bullets_active", [(0, 0), (1, 1), (4, 3)])
    def test_fire_bullet(self, bullets_fired, bullets_active):
        for i in range(bullets_fired):
            self.ai._fire_bullet()
        assert len(self.ai.bullets) == bullets_active
    
    # check both kinds of alien bullet are added to group
    def test_fire_yellow_bullet(self):
        self.ai._fire_yellow_bullet(self.alien)
        assert len(self.ai.alien_bullets) == 1
    
    def test_fire_red_bullet(self):
        self.ai._fire_red_bullet(self.alien)
        assert len(self.ai.alien_bullets) == 1
    
    # These 5 tests are the effects of empty_sprites
    def test_empty_sprites_bullets(self):
        self.ai._fire_bullet()
        self.ai.empty_sprites()
        assert len(self.ai.bullets) == 0
    
    def test_empty_sprites_aliens(self):
        self.ai.empty_sprites()
        assert len(self.ai.aliens) == 0
    
    def test_empty_sprites_yellow_aliens(self):
        self.ai._create_yellow_alien(0, 0)
        self.ai.empty_sprites()
        assert len(self.ai.yellow_aliens) == 0
    
    def test_empty_sprites_red_aliens(self):
        self.ai._create_red_alien(0, 0)
        self.ai.empty_sprites()
        assert len(self.ai.red_aliens) == 0
    
    def test_empty_sprites_alien_bullets(self):
        self.ai._fire_yellow_bullet(self.alien)
        self.ai._fire_red_bullet(self.alien)
        self.ai.empty_sprites()
        assert len(self.ai.alien_bullets) == 0
    
    # Adding 3 kinds of alien to groups
    def test_create_alien(self):
        self.ai.empty_sprites()
        self.ai._create_alien(0, 0)
        assert len(self.ai.aliens) == 1
        
    def test_create_yellow_alien(self):
        self.ai.empty_sprites()
        self.ai._create_yellow_alien(50, 50)
        assert len(self.ai.aliens) == 1 and len(self.ai.yellow_aliens) == 1
    
    def test_create_red_alien(self):
        self.ai.empty_sprites()
        self.ai._create_red_alien( 100, 100)
        assert len(self.ai.aliens) == 1 and len(self.ai.red_aliens) == 1
    
    # create fleet with and without red aliens
    def test_create_fleet(self):
        self.ai.empty_sprites()
        self.ai.create_fleet()
        assert len(self.ai.aliens) > 0 and len(self.ai.yellow_aliens) > 0
    
    def test_create_fleet_level_5(self):
        self.ai.empty_sprites()
        self.ai.stats.level = 5
        self.ai.create_fleet()
        assert len(self.ai.red_aliens) > 1

   
class TestUpdates:
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
        self.ai.aliens.add(self.alien)
    
    def test_update_bullets_player_offscreen(self):
        bullet = Bullet(self.ai)
        self.ai.bullets.add(bullet)
        bullet.y = -50
        self.ai._update_bullets()
        assert len(self.ai.bullets) == 0
    
    def test_update_bullets_alien_offscreen(self):
        bullet = YellowBullet(self.ai, self.alien)
        self.ai.alien_bullets.add(bullet)
        bullet.y = self.ai.screen_height + 50
        self.ai._update_bullets()
        assert len(self.ai.alien_bullets) == 0
    
    # mock randint to trigger firing and non-firing
    @mock.patch('alien_invasion.alien_invasion.randint')
    def test_check_alien_shooting_true(self, mock_randint):
        mock_randint.return_value = 3
        self.ai._check_alien_shooting()
        assert len(self.ai.alien_bullets) > 0
    
    @mock.patch('alien_invasion.alien_invasion.randint')
    def test_check_alien_shooting_false(self, mock_randint):
        mock_randint.return_value = 3000
        self.ai._check_alien_shooting()
        assert len(self.ai.alien_bullets) == 0
    
    def test_check_fleet_edges_false(self):
        self.ai.empty_sprites()
        starting_direction = self.ai.settings.fleet_direction
        self.ai._check_fleet_edges()
        assert self.ai.settings.fleet_direction == starting_direction
    
    def test_check_fleet_edges_true(self):
        starting_direction = self.ai.settings.fleet_direction
        self.ai._create_alien(self.ai.screen_width, 0)
        self.ai._check_fleet_edges()
        assert self.ai.settings.fleet_direction == - starting_direction
    
    def test_change_fleet_direction(self):
        starting_y = self.alien.rect.y
        self.ai._change_fleet_direction()
        assert self.alien.rect.y > starting_y
    
    def test_check_aliens_bottom(self):
        starting_ships = self.ai.stats.ships_left
        self.alien.rect.bottom = self.ai.screen_height
        self.ai._check_aliens_bottom()
        assert self.ai.stats.ships_left < starting_ships


class TestCollisions:
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
        self.ai.aliens.add(self.alien)
    
    def test_ship_hit(self):
        self.ai.ship.rect.x = 0
        self.ai._ship_hit()
        assert self.ai.ship.rect.midbottom == self.ai.screen.get_rect().midbottom

    def test_bullet_alien_collisions(self):
        starting_score = self.ai.stats.score
        bullet = Bullet(self.ai)
        self.ai.bullets.add(bullet)
        bullet.rect.center = self.alien.rect.center
        self.ai._check_bullet_alien_collisions()
        assert self.ai.stats.score > starting_score and len(self.ai.bullets) == 0
    
    def test_update_aliens(self):
        starting_ships = self.ai.stats.ships_left
        self.alien.x = self.ai.ship.rect.x - self.ai.settings.alien_speed
        self.alien.y = self.ai.ship.rect.y
        self.alien.rect.y = self.alien.y
        self.ai._update_aliens()
        assert self.ai.stats.ships_left < starting_ships
    
    # rect check should not be a collision; mask should be
    def test_bullet_ship_collisions_rect(self):
        bullet = RedBullet(self.ai, self.alien)
        self.ai.alien_bullets.add(bullet)
        bullet.rect.bottomright = self.ai.ship.rect.topleft
        bullet.rect.x -= 1
        bullet.rect.y -= 1
        self.ai._check_bullet_ship_collisions()
        assert len(self.ai.alien_bullets) == 1
    
    def test_bullet_ship_collisions_mask(self):
        bullet = RedBullet(self.ai, self.alien)
        self.ai.alien_bullets.add(bullet)
        bullet.rect.center = self.ai.ship.rect.center
        self.ai._check_bullet_ship_collisions()
        assert len(self.ai.alien_bullets) == 0


class TestEvents:
    """Untested: quitting, mouse motion/clicks, left, q, p, m, h"""
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
        self.ai.aliens.add(self.alien)
    
    @mock.patch("pygame.event.get")
    def test_check_events_right_down(self, mock_pygame_event_get):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_RIGHT
        mock_pygame_event_get.return_value = [key_event]
        self.ai._check_events()
        assert self.ai.ship.moving_right == True
    
    @mock.patch("pygame.event.get")
    def test_check_events_right_up(self, mock_pygame_event_get):
        key_event_1 = mock.Mock()
        key_event_1.type = pygame.KEYDOWN
        key_event_1.key = pygame.K_RIGHT
        key_event_2 = mock.Mock()
        key_event_2.type = pygame.KEYUP
        key_event_2.key = pygame.K_RIGHT
        mock_pygame_event_get.return_value = [key_event_1, key_event_2]
        self.ai._check_events()
        assert self.ai.ship.moving_right == False
    
    @mock.patch("pygame.event.get")
    def test_check_events_space(self, mock_pygame_event_get):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_SPACE
        mock_pygame_event_get.return_value = [key_event]
        self.ai._check_events()
        assert len(self.ai.bullets) == 1
    
    @mock.patch("pygame.event.get")
    def test_check_events_level(self, mock_pygame_event_get):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_l
        mock_pygame_event_get.return_value = [key_event]
        self.ai._check_events()
        assert self.ai.stats.level > 1
    
    @mock.patch("pygame.event.get")
    def test_check_events_reset(self, mock_pygame_event_get):
        self.ai.stats.level = 5
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_r
        mock_pygame_event_get.return_value = [key_event]
        self.ai._check_events()
        assert self.ai.stats.level == 1

class TestStartingStopping:
    
    def setup_method(self):
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)
        self.ai.aliens.add(self.alien)
    
    def test_start_new_level(self):
        starting_level = self.ai.stats.level
        self.ai.start_new_level()
        assert self.ai.stats.level > starting_level
    
    def test_run_game(self):
        pass
    
    def test_start_game(self):
        pass
    
    def test_end_game(self):
        pass


class TestDrawing:
    pass
