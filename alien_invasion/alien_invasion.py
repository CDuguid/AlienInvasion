import sys
from time import sleep
from random import randint
from os import path
import pygame
import pygamepopup

from alien_invasion.settings import Settings
from alien_invasion.ship import Ship
from alien_invasion.bullet import Bullet, YellowBullet, RedBullet
from alien_invasion.alien import Alien, YellowAlien, RedAlien
from alien_invasion.game_stats import GameStats
from alien_invasion.scoreboard import Scoreboard
from alien_invasion.game_sounds import GameSounds
from alien_invasion.main_menu import MainMenuScene
from alien_invasion.explosion import Explosion

images_dir = path.join(path.dirname(__file__), "assets", "images")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 150)


class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self, testing=False):
        """Initialise the game and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.testing = testing
        self.game_active = False

        self.screen = pygame.display.set_mode((1280, 800))
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.bg_image_orig = pygame.image.load(
            path.join(images_dir, "background_space.png")
        ).convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image_orig, (self.screen_width, self.screen_height)
        )

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.alien = Alien(self)
        self.ship = Ship(self)
        self.ship_sprite = pygame.sprite.Group()
        self.ship_sprite.add(self.ship)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.yellow_aliens = pygame.sprite.Group()
        self.red_aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.create_fleet()

        pygamepopup.init()
        self.main_menu_scene = MainMenuScene(self)

        self.sounds = GameSounds(self)
        if not self.testing:
            self.sounds.play_main_theme()

    def run_game(self):
        """Start the main loop for the game."""
        self._show_intro()
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.explosions.update()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEMOTION:
                # Highlight buttons upon hover
                self.main_menu_scene.motion(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_active == False:
                    self.main_menu_scene.click(event.button, event.pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            new_high_score = self.stats.high_score
            self.stats.score_path.write_text(str(new_high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and self.game_active == False:
            self.start_game()
        elif event.key == pygame.K_l:
            self.main_menu_scene.increase_level()
        elif event.key == pygame.K_m and self.game_active == True:
            self._end_game()
        elif event.key == pygame.K_h and self.game_active == False:
            self.main_menu_scene.create_help_menu()
        elif event.key == pygame.K_r and self.game_active == False:
            self.main_menu_scene.reset_starting_difficulty()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def start_game(self):
        """Start a new game from welcome screen."""
        if not self.main_menu_scene.level_modified:
            self.settings.initialise_dynamic_settings()
            self.stats.reset_level()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True

        self.empty_sprites()
        self.create_fleet()
        self.ship.centre_ship()

        if not self.testing:
            self.sounds.play_level_theme()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if not self.testing:
                self.sounds.play_bullet_sound()

    def _fire_yellow_bullet(self, alien):
        """Create a yellow alien bullet and add it to the alien bullets group."""
        new_bullet = YellowBullet(self, alien)
        self.alien_bullets.add(new_bullet)

    def _fire_red_bullet(self, alien):
        """Create a red alien bullet and add it to the alien bullets group."""
        new_bullet = RedBullet(self, alien)
        self.alien_bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        self.alien_bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.screen_height:
                self.alien_bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        self._check_bullet_ship_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            for collision in collisions:
                explosion = Explosion(collision.rect.center)
                self.explosions.add(explosion)
            self.sb.prep_score()
            self.sb.check_high_score()
            if not self.testing:
                self.sounds.play_alien_hit_sound()

        if not self.aliens:
            self.start_new_level()

    def _check_bullet_ship_collisions(self):
        """Respond to bullet-ship collisions."""
        rect_collisions = pygame.sprite.groupcollide(
            self.alien_bullets, self.ship_sprite, False, False
        )

        if rect_collisions:
            if pygame.sprite.spritecollide(
                self.ship, self.alien_bullets, True, pygame.sprite.collide_mask
            ):
                self._ship_hit()

    def start_new_level(self):
        """Increase level and start a new wave of aliens."""
        self.empty_sprites()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()
        self.create_fleet()

        if not self.testing:
            self.sounds.play_level_theme()

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            if pygame.sprite.spritecollide(
                self.ship, self.aliens, False, pygame.sprite.collide_mask
            ):
                self._ship_hit()

        self._check_aliens_bottom()
        self._check_alien_shooting()

    def _check_alien_shooting(self):
        """Checks for any aliens due to shoot."""
        for alien in self.red_aliens:
            shot_roll = randint(1, 10000)
            if shot_roll <= self.settings.red_bullet_chance:
                self._fire_red_bullet(alien)

        for alien in self.yellow_aliens:
            shot_roll = randint(1, 10000)
            if shot_roll <= self.settings.yellow_bullet_chance:
                self._fire_yellow_bullet(alien)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if not self.testing:
            self.sounds.play_ship_hit_sound()

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.empty_sprites()
            self.create_fleet()
            self.ship.centre_ship()

            sleep(0.5)
        else:
            self._end_game()

    def _end_game(self):
        """Shows game over stats and then cleans them up."""
        sleep(1)
        self._show_game_over()

        self.main_menu_scene.level_modified = False
        self.stats.reset_level()
        self.settings.initialise_dynamic_settings()
        self.game_active = False

    def empty_sprites(self):
        """Empties all sprite groups except for the ship."""
        self.bullets.empty()
        self.aliens.empty()
        self.yellow_aliens.empty()
        self.red_aliens.empty()
        self.alien_bullets.empty()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_height:
                self._ship_hit()
                break

    def create_fleet(self):
        """Creates the alien fleet."""
        row_comp = self._calculate_row_composition()
        current_y = self.alien.rect.height
        alien_y_spacing = 2 * self.alien.rect.height

        for _ in range(row_comp["red_rows"]):
            self._create_row_of_aliens("red", current_y)
            current_y += alien_y_spacing
        for _ in range(row_comp["yellow_rows"]):
            self._create_row_of_aliens("yellow", current_y)
            current_y += alien_y_spacing
        for _ in range(row_comp["green_rows"]):
            self._create_row_of_aliens("green", current_y)
            current_y += alien_y_spacing

    def _calculate_number_of_rows(self):
        """Calculates the number of rows of aliens required to create a full fleet."""
        alien_free_area = 3 * self.alien.rect.height
        alien_y_spacing = 2 * self.alien.rect.height
        total_y_space = self.screen_height - alien_free_area
        total_rows = total_y_space // alien_y_spacing
        return total_rows

    def _calculate_row_composition(self):
        """Calculates how many rows of each alien type to create."""
        row_comp = {}
        total_rows = self._calculate_number_of_rows()
        levels_for_new_red_row = 4
        req_red_rows = min((self.stats.level - 1) // levels_for_new_red_row, total_rows)
        row_comp["red_rows"] = req_red_rows
        req_yellow_rows = min(1, total_rows - req_red_rows)
        row_comp["yellow_rows"] = req_yellow_rows
        req_green_rows = max(0, total_rows - req_red_rows - req_yellow_rows)
        row_comp["green_rows"] = req_green_rows
        return row_comp

    def _create_row_of_aliens(self, alien_color, y_position):
        """Creates a row of aliens of the specified type."""
        alien_x_spacing = 2 * self.alien.rect.width
        current_x = self.alien.rect.width

        while current_x < (self.screen_width - alien_x_spacing):
            if alien_color == "green":
                self._create_alien(current_x, y_position)
            elif alien_color == "yellow":
                self._create_yellow_alien(current_x, y_position)
            elif alien_color == "red":
                self._create_red_alien(current_x, y_position)
            current_x += alien_x_spacing

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_yellow_alien(self, x_position, y_position):
        """Create a yellow alien and place it in the fleet."""
        new_alien = YellowAlien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        self.yellow_aliens.add(new_alien)

    def _create_red_alien(self, x_position, y_position):
        """Create a red alien and place it in the fleet."""
        new_alien = RedAlien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        self.red_aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_image, (0, 0))
        self.sb.show_score()

        for bullet in self.bullets.sprites():
            bullet.blitme()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.blitme()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)

        if not self.game_active:
            self.main_menu_scene.display()

        pygame.display.flip()

    def _show_intro(self):
        """Shows the intro screen when game is first loaded."""
        self.screen.fill(BLACK)
        self._draw_text(
            "ALIEN", 60, PURPLE, self.screen_width / 2, self.screen_height / 4
        )
        self._draw_text(
            "INVASION", 60, PURPLE, self.screen_width / 2, self.screen_height / 2
        )
        self._draw_text(
            "Press any key to begin",
            40,
            GREEN,
            self.screen_width / 2,
            self.screen_height * 3 / 4,
        )

        pygame.display.flip()
        self._wait_for_key()

    def _draw_text(self, text, size, colour, x, y):
        """Draws text for use on the intro/game-over screens."""
        font = pygame.font.Font("freesansbold.ttf", size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def _show_game_over(self):
        """Shows game info when the player is defeated."""
        surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        surface.fill((80, 0, 0, 120))
        self.screen.blit(surface, (0, 0))

        self._draw_text(
            "GAME OVER!", 84, RED, self.screen_width / 2, self.screen_height / 4
        )
        self._draw_text(
            f"You successfully defeated {self.stats.level -1} waves of aliens "
            f"with a score of {round(self.stats.score, -1)}",
            40,
            RED,
            self.screen_width / 2,
            self.screen_height / 2,
        )
        self._draw_text(
            f"The score to beat is currently {round(self.stats.high_score, -1)}",
            40,
            RED,
            self.screen_width / 2,
            self.screen_height / 2 - 40,
        )
        self._draw_text(
            "Press any key to continue",
            40,
            RED,
            self.screen_width / 2,
            self.screen_height * 3 / 4,
        )

        pygame.display.flip()
        sleep(1)
        self._wait_for_key()

    def _wait_for_key(self):
        """Pauses the game during intro and end screens while waiting for the player to respond."""
        self.clock.tick(60)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    waiting = False
