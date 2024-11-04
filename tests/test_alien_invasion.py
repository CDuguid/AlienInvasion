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
    
    @pytest.mark.parametrize("bullets_fired, bullets_active", [(0, 0), (1, 1), (4, 3)])
    def test_fire_bullet(self, bullets_fired, bullets_active, ai):
        for i in range(bullets_fired):
            ai._fire_bullet()
        assert len(ai.bullets) == bullets_active
    
    def test_fire_alien_bullet(self, ai, alien):
        ai._fire_yellow_bullet(alien)
        ai._fire_red_bullet(alien)
        assert len(ai.alien_bullets) == 2
    
    def test_empty_sprites(self, ai, alien):
        ai._fire_bullet()
        ai._create_yellow_alien(0, 0)
        ai._create_red_alien(0, 0)
        ai._fire_yellow_bullet(alien)
        ai._fire_red_bullet(alien)
        ai.empty_sprites()
        assert len(ai.bullets) == len(ai.aliens) == len(ai.yellow_aliens) == len(ai.red_aliens) == len(ai.alien_bullets) == 0
    
    def test_create_alien(self, ai):
        ai.empty_sprites()
        ai._create_alien(0, 0)
        ai._create_yellow_alien(50, 50)
        ai._create_red_alien(100, 100)
        assert len(ai.aliens) == 3 and len(ai.yellow_aliens) == len(ai.red_aliens)
    
    def test_create_correct_number_of_yellow_aliens_in_fleet(self, ai, alien):
        ai.empty_sprites()
        ai.create_fleet()
        aliens_per_row = ai.screen_width // (2 * alien.rect.width)
        assert len(ai.yellow_aliens) == aliens_per_row
    
    @pytest.mark.parametrize("level", [1, 5, 9])
    def test_create_correct_number_of_red_aliens_in_fleet(self, level, ai, alien):
        ai.empty_sprites()
        ai.stats.level = level
        ai.create_fleet()
        red_rows = (ai.stats.level - 1) // 4
        aliens_per_row = ai.screen_width // (2 * alien.rect.width)
        expected_red_aliens = red_rows * aliens_per_row
        assert len(ai.red_aliens) == expected_red_aliens
    
    @pytest.mark.parametrize("level", [1, 5, 9])
    def test_create_correct_number_of_green_aliens_in_fleet(self, level, ai, alien):
        ai.empty_sprites()
        ai.stats.level = level
        ai.create_fleet()
        total_space_y = ai.screen_height -  3 * alien.rect.height
        total_rows = total_space_y // (2 * alien.rect.height)
        red_rows = (ai.stats.level - 1) // 4
        aliens_per_row = ai.screen_width // (2 * alien.rect.width)
        green_rows = total_rows - red_rows - 1
        expected_green_aliens = green_rows * aliens_per_row
        created_green_aliens = len(ai.aliens) - len(ai.red_aliens) - len(ai.yellow_aliens)
        assert created_green_aliens == expected_green_aliens

   
class TestUpdates:
    
    def test_delete_offscreen_bullets(self, ai, alien):
        bullet = Bullet(ai)
        ai.bullets.add(bullet)
        bullet.y = -50
        alien_bullet = YellowBullet(ai, alien)
        ai.alien_bullets.add(alien_bullet)
        alien_bullet.y = ai.screen_height + 50
        ai._update_bullets()
        assert len(ai.bullets) == len(ai.alien_bullets) == 0
    
    @mock.patch('alien_invasion.alien_invasion.randint')
    @pytest.mark.parametrize("rand_val, bullets_active", [(3, 10), (3000, 0)])
    def test_check_alien_shooting(self, mock_randint, rand_val, bullets_active, ai):
        mock_randint.return_value = rand_val
        ai._check_alien_shooting()
        assert len(ai.alien_bullets) == bullets_active
        
    def test_fleet_detects_screen_edges(self, ai, alien, alien_in_group):
        starting_direction = ai.settings.fleet_direction
        starting_y = alien.rect.y
        ai._create_alien(ai.screen_width, 0)
        ai._check_fleet_edges()
        assert ai.settings.fleet_direction == - starting_direction and alien.rect.y > starting_y
    
    def test_fleet_detects_screen_bottom(self, ai, alien, alien_in_group):
        starting_ships = ai.stats.ships_left
        alien.rect.bottom = ai.screen_height
        ai._check_aliens_bottom()
        assert ai.stats.ships_left < starting_ships


class TestCollisions:

    def test_bullets_collide_with_aliens(self, ai, alien):
        starting_score = ai.stats.score
        bullet = Bullet(ai)
        ai.bullets.add(bullet)
        bullet.rect.center = alien.rect.center
        ai._check_bullet_alien_collisions()
        assert ai.stats.score > starting_score and len(ai.bullets) == 0 and alien not in ai.aliens
    
    def test_aliens_collide_with_player(self, ai, alien, alien_in_group):
        starting_ships = ai.stats.ships_left
        alien.x = ai.ship.rect.x - ai.settings.alien_speed
        alien.y = ai.ship.rect.y
        alien.rect.y = alien.y
        ai._update_aliens()
        assert ai.stats.ships_left < starting_ships
    
    def test_player_rect_does_not_collide(self, ai, alien):
        starting_ships = ai.stats.ships_left
        bullet = RedBullet(ai, alien)
        ai.alien_bullets.add(bullet)
        bullet.rect.bottomright = ai.ship.rect.topleft
        bullet.rect.x -= 1
        bullet.rect.y -= 1
        ai._check_bullet_ship_collisions()
        assert len(ai.alien_bullets) == 1 and ai.stats.ships_left == starting_ships
    
    def test_player_mask_does_collide(self, ai, alien):
        starting_ships = ai.stats.ships_left
        bullet = RedBullet(ai, alien)
        ai.alien_bullets.add(bullet)
        bullet.rect.center = ai.ship.rect.center
        ai._check_bullet_ship_collisions()
        assert len(ai.alien_bullets) == 0 and ai.stats.ships_left == starting_ships - 1


class TestEvents:
    
    @mock.patch("pygame.event.get")
    def test_right_key_pressed(self, mock_pygame_event_get, ai):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_RIGHT
        mock_pygame_event_get.return_value = [key_event]
        ai._check_events()
        assert ai.ship.moving_right == True
    
    @mock.patch("pygame.event.get")
    def test_right_key_lifted(self, mock_pygame_event_get, ai):
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
    def test_space_pressed(self, mock_pygame_event_get, ai):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_SPACE
        mock_pygame_event_get.return_value = [key_event]
        ai._check_events()
        assert len(ai.bullets) == 1
    
    @mock.patch("pygame.event.get")
    def test_l_key_pressed(self, mock_pygame_event_get, ai):
        key_event = mock.Mock()
        key_event.type = pygame.KEYDOWN
        key_event.key = pygame.K_l
        mock_pygame_event_get.return_value = [key_event]
        ai._check_events()
        assert ai.stats.level > 1
    
    @mock.patch("pygame.event.get")
    def test_r_key_pressed(self, mock_pygame_event_get, ai):
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
