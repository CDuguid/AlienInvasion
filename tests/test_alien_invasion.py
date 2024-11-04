from alien_invasion.alien_invasion import AlienInvasion
from alien_invasion.alien import Alien
from alien_invasion.bullet import Bullet, YellowBullet, RedBullet
import unittest.mock as mock
import pygame
import pytest

@pytest.fixture
def ai():
    return AlienInvasion()

@pytest.fixture
def alien(ai):
    return Alien(ai)

@pytest.fixture
def alien_in_group(ai, alien):
    ai.aliens.add(alien)


class TestSpriteCreation:
    
    # test fire_bullet adds a bullet to group and has upper limit
    @pytest.mark.parametrize("bullets_fired, bullets_active", [(0, 0), (1, 1), (4, 3)])
    def test_fire_bullet(self, bullets_fired, bullets_active, ai):
        for i in range(bullets_fired):
            ai._fire_bullet()
        assert len(ai.bullets) == bullets_active
    
    # check both kinds of alien bullet are added to group
    def test_fire_yellow_bullet(self, ai, alien):
        ai._fire_yellow_bullet(alien)
        assert len(ai.alien_bullets) == 1
    
    def test_fire_red_bullet(self, ai, alien):
        ai._fire_red_bullet(alien)
        assert len(ai.alien_bullets) == 1
    
    # These 5 tests are the effects of empty_sprites
    def test_empty_sprites_bullets(self, ai):
        ai._fire_bullet()
        ai.empty_sprites()
        assert len(ai.bullets) == 0
    
    def test_empty_sprites_aliens(self, ai):
        ai.empty_sprites()
        assert len(ai.aliens) == 0
    
    def test_empty_sprites_yellow_aliens(self, ai):
        ai._create_yellow_alien(0, 0)
        ai.empty_sprites()
        assert len(ai.yellow_aliens) == 0
    
    def test_empty_sprites_red_aliens(self, ai):
        ai._create_red_alien(0, 0)
        ai.empty_sprites()
        assert len(ai.red_aliens) == 0
    
    def test_empty_sprites_alien_bullets(self, ai, alien):
        ai._fire_yellow_bullet(alien)
        ai._fire_red_bullet(alien)
        ai.empty_sprites()
        assert len(ai.alien_bullets) == 0
    
    # Adding 3 kinds of alien to groups
    def test_create_alien(self, ai):
        ai.empty_sprites()
        ai._create_alien(0, 0)
        assert len(ai.aliens) == 1
        
    def test_create_yellow_alien(self, ai):
        ai.empty_sprites()
        ai._create_yellow_alien(50, 50)
        assert len(ai.aliens) == 1 and len(ai.yellow_aliens) == 1
    
    def test_create_red_alien(self, ai):
        ai.empty_sprites()
        ai._create_red_alien(100, 100)
        assert len(ai.aliens) == 1 and len(ai.red_aliens) == 1
    
    # create fleet with and without red aliens
    def test_create_fleet(self, ai):
        ai.empty_sprites()
        ai.create_fleet()
        assert len(ai.aliens) > 0 and len(ai.yellow_aliens) > 0
    
    def test_create_fleet_level_5(self, ai):
        ai.empty_sprites()
        ai.stats.level = 5
        ai.create_fleet()
        assert len(ai.red_aliens) > 1

   
class TestUpdates:
    
    def test_update_bullets_player_offscreen(self, ai):
        bullet = Bullet(ai)
        ai.bullets.add(bullet)
        bullet.y = -50
        ai._update_bullets()
        assert len(ai.bullets) == 0
    
    def test_update_bullets_alien_offscreen(self, ai, alien):
        bullet = YellowBullet(ai, alien)
        ai.alien_bullets.add(bullet)
        bullet.y = ai.screen_height + 50
        ai._update_bullets()
        assert len(ai.alien_bullets) == 0
    
    # mock randint to trigger firing and non-firing
    @mock.patch('alien_invasion.alien_invasion.randint')
    def test_check_alien_shooting_true(self, mock_randint, ai):
        mock_randint.return_value = 3
        ai._check_alien_shooting()
        assert len(ai.alien_bullets) > 0
    
    @mock.patch('alien_invasion.alien_invasion.randint')
    def test_check_alien_shooting_false(self, mock_randint, ai):
        mock_randint.return_value = 3000
        ai._check_alien_shooting()
        assert len(ai.alien_bullets) == 0
    
    def test_check_fleet_edges_false(self, ai):
        ai.empty_sprites()
        starting_direction = ai.settings.fleet_direction
        ai._check_fleet_edges()
        assert ai.settings.fleet_direction == starting_direction
    
    def test_check_fleet_edges_true(self, ai):
        starting_direction = ai.settings.fleet_direction
        ai._create_alien(ai.screen_width, 0)
        ai._check_fleet_edges()
        assert ai.settings.fleet_direction == - starting_direction
    
    def test_change_fleet_direction(self, ai, alien, alien_in_group):
        starting_y = alien.rect.y
        ai._change_fleet_direction()
        assert alien.rect.y > starting_y
    
    def test_check_aliens_bottom(self, ai, alien, alien_in_group):
        starting_ships = ai.stats.ships_left
        alien.rect.bottom = ai.screen_height
        ai._check_aliens_bottom()
        assert ai.stats.ships_left < starting_ships


class TestCollisions:
    
    def test_ship_hit(self, ai):
        ai.ship.rect.x = 0
        ai._ship_hit()
        assert ai.ship.rect.midbottom == ai.screen.get_rect().midbottom

    def test_bullet_alien_collisions(self, ai, alien):
        starting_score = ai.stats.score
        bullet = Bullet(ai)
        ai.bullets.add(bullet)
        bullet.rect.center = alien.rect.center
        ai._check_bullet_alien_collisions()
        assert ai.stats.score > starting_score and len(ai.bullets) == 0
    
    def test_update_aliens(self, ai, alien, alien_in_group):
        starting_ships = ai.stats.ships_left
        alien.x = ai.ship.rect.x - ai.settings.alien_speed
        alien.y = ai.ship.rect.y
        alien.rect.y = alien.y
        ai._update_aliens()
        assert ai.stats.ships_left < starting_ships
    
    # rect check should not be a collision; mask should be
    def test_bullet_ship_collisions_rect(self, ai, alien):
        bullet = RedBullet(ai, alien)
        ai.alien_bullets.add(bullet)
        bullet.rect.bottomright = ai.ship.rect.topleft
        bullet.rect.x -= 1
        bullet.rect.y -= 1
        ai._check_bullet_ship_collisions()
        assert len(ai.alien_bullets) == 1
    
    def test_bullet_ship_collisions_mask(self, ai, alien):
        bullet = RedBullet(ai, alien)
        ai.alien_bullets.add(bullet)
        bullet.rect.center = ai.ship.rect.center
        ai._check_bullet_ship_collisions()
        assert len(ai.alien_bullets) == 0


class TestEvents:
    """Untested: quitting, mouse motion/clicks, left, q, p, m, h"""
    
    @mock.patch("pygame.event.get")
    def test_check_events_right_down(self, mock_pygame_event_get, ai):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_RIGHT
        mock_pygame_event_get.return_value = [key_event]
        ai._check_events()
        assert ai.ship.moving_right == True
    
    @mock.patch("pygame.event.get")
    def test_check_events_right_up(self, mock_pygame_event_get, ai):
        key_event_1 = mock.Mock()
        key_event_1.type = pygame.KEYDOWN
        key_event_1.key = pygame.K_RIGHT
        key_event_2 = mock.Mock()
        key_event_2.type = pygame.KEYUP
        key_event_2.key = pygame.K_RIGHT
        mock_pygame_event_get.return_value = [key_event_1, key_event_2]
        ai._check_events()
        assert ai.ship.moving_right == False
    
    @mock.patch("pygame.event.get")
    def test_check_events_space(self, mock_pygame_event_get, ai):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_SPACE
        mock_pygame_event_get.return_value = [key_event]
        ai._check_events()
        assert len(ai.bullets) == 1
    
    @mock.patch("pygame.event.get")
    def test_check_events_level(self, mock_pygame_event_get, ai):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_l
        mock_pygame_event_get.return_value = [key_event]
        ai._check_events()
        assert ai.stats.level > 1
    
    @mock.patch("pygame.event.get")
    def test_check_events_reset(self, mock_pygame_event_get, ai):
        ai.stats.level = 5
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_r
        mock_pygame_event_get.return_value = [key_event]
        ai._check_events()
        assert ai.stats.level == 1

class TestStartingStopping:
    
    def test_start_new_level(self, ai):
        starting_level = ai.stats.level
        ai.start_new_level()
        assert ai.stats.level > starting_level
    
    def test_run_game(self):
        pass
    
    def test_start_game(self):
        pass
    
    def test_end_game(self):
        pass


class TestDrawing:
    pass
