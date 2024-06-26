import sys
from time import sleep
from random import randint
import pygame
import pygamepopup
from settings import Settings
from ship import Ship
from bullet import Bullet, YellowBullet, RedBullet
from alien import Alien, YellowAlien, RedAlien
from game_stats import GameStats
from scoreboard import Scoreboard
from game_sounds import GameSounds
from main_menu import MainMenuScene

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
        """Initialise the game and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.bg_image = pygame.image.load('images/background_space.png').convert()
        
        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.ship_sprite = pygame.sprite.Group()
        self.ship_sprite.add(self.ship)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.yellow_aliens = pygame.sprite.Group()
        self.red_aliens = pygame.sprite.Group()
        
        self.create_fleet()
        
        # Start Alien Invasion in an inactive state
        self.game_active = False
        
        # Initialise main menu
        pygamepopup.init()
        self.main_menu_scene = MainMenuScene(self)
        
        # Play welcome screen soundtrack
        self.sounds = GameSounds(self)
        self.sounds.play_main_theme()
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
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
        elif event.key == pygame.K_p:
            self.start_game()
        elif event.key == pygame.K_l:
            self.main_menu_scene.increase_level()
        elif event.key == pygame.K_h:
            self.main_menu_scene.create_help_menu()
        elif event.key == pygame.K_r:
            self.main_menu_scene.reset_starting_difficulty()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
       
    def start_game(self):
        """Start a new game from welcome screen."""
        # Reset the game settings
        # Conditional block to prevent reset if difficulty increased via menu
        if not self.main_menu_scene.level_modified:
            self.settings.initialise_dynamic_settings()
            self.stats.reset_level()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True
        
        # Get rid of any remaining aliens and bullets
        self.empty_sprites()
        
        # Create a new fleet and centre the ship
        self.create_fleet()
        self.ship.centre_ship()
        
        # Play level soundtrack
        self.sounds.play_level_theme()
        
        # Hide the mouse cursor - currently not working
        pygame.mouse.set_visible(False)
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
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
        # Update bullet positions.
        self.bullets.update()
        self.alien_bullets.update()
        
        # Get rid of disappeared bullets.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
        self._check_bullet_ship_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        # Award points for hit aliens and play sound
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sounds.play_alien_hit_sound()
        
        # Repopulate the fleet if empty.
        if not self.aliens:
            self.start_new_level()
        
    def _check_bullet_ship_collisions(self):
        """Respond to bullet-ship collisions."""
        collisions = pygame.sprite.groupcollide(
            self.alien_bullets, self.ship_sprite, True, False)
        if collisions:
            self._ship_hit()
    
    def start_new_level(self):
        """Start a new wave of aliens."""
        # Destroy existing bullets and increase speed.
        self.empty_sprites()
        self.settings.increase_speed()
        
        # Increase level
        self.stats.level += 1
        self.sb.prep_level()
        
        self.create_fleet()
        
        # Play new level soundtrack
        self.sounds.play_level_theme()
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
        
        # Check for any aliens due to shoot
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
        self.sounds.play_ship_hit_sound()
        
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # Get rid of remaining bullets and aliens
            self.empty_sprites()
            
            # Create a new fleet and centre the ship
            self.create_fleet()
            self.ship.centre_ship()
            
            # Pause
            sleep(0.5)
        else:
            self._end_game()
    
    def _end_game(self):
        """Shows game over stats and then cleans them up."""
        # Show the game over stats; sleep to prevent accidental game over screen skip
        sleep(1)
        self._show_game_over()
        
        # Reset the level and dynamic settings for a new game
        self.main_menu_scene.level_modified = False
        self.stats.reset_level()
        self.settings.initialise_dynamic_settings()
        self.game_active = False
        
        # Mouse isn't going invisible, but just in case it does in the future...
        pygame.mouse.set_visible(True)
    
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
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship gets hit
                self._ship_hit()
                break

    def create_fleet(self):
        """Creates the alien fleet."""
        # All aliens are the same size
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        # Variables to determine how many rows to fill
        current_x, current_y = alien_width, alien_height
        total_space_y = self.settings.screen_height -  3 * alien_height
        total_rows = total_space_y // (2 * alien_height)
        req_red_rows = min((self.stats.level - 1) // 4, total_rows)
        used_rows = 0
        yellow_row_created = False
        
        # Create a red row every 4 levels, then 1 yellow, then green for remaining rows
        while total_rows - used_rows > 0:
            if req_red_rows - used_rows > 0:
                while current_x < (self.settings.screen_width - 2 * alien_width):
                    self._create_red_alien(current_x, current_y)
                    current_x += 2 * alien_width
            elif total_rows >= 1 and not yellow_row_created:
                while current_x < (self.settings.screen_width - 2 * alien_width):
                    self._create_yellow_alien(current_x, current_y)
                    current_x += 2 * alien_width
                yellow_row_created = True
            else:
                while current_x < (self.settings.screen_width - 2 * alien_width):
                    self._create_alien(current_x, current_y)
                    current_x += 2 * alien_width
            
            # Reset variables for new loop after a row is filled
            used_rows += 1
            current_x = alien_width
            current_y += 2 * alien_height
    
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
        self.screen.blit(self.bg_image, (0, 0))
        self.sb.show_score()
        
        for bullet in self.bullets.sprites():
            bullet.blitme()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.blitme()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        # Show the main menu if game is inactive
        if not self.game_active:
            self.main_menu_scene.display()
        
        pygame.display.flip()
    
    def _show_intro(self):
        """Shows the intro screen when game is first loaded."""
        self.screen.fill((0, 0, 0))
        self._draw_text("ALIEN", 60, (200, 0, 150), 
                       self.settings.screen_width / 2, self.settings.screen_height / 4)
        self._draw_text("INVASION", 60, (200, 0, 150), 
                       self.settings.screen_width / 2, self.settings.screen_height / 2)
        self._draw_text("Press any key to begin", 40, (0, 255, 0), 
                       self.settings.screen_width / 2, self.settings.screen_height * 3 / 4)
        
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
        # Create partially transparent surface over the game area
        surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        surface.fill((80, 0, 0, 120))
        self.screen.blit(surface, (0, 0))
        
        self._draw_text("GAME OVER!", 84, (255, 0, 0), 
                        self.settings.screen_width / 2, self.settings.screen_height / 4)
        self._draw_text(f"You successfully defeated {self.stats.level -1} waves of aliens "
                        f"with a score of {round(self.stats.score, -1)}", 40, (255, 0, 0), 
                       self.settings.screen_width / 2, self.settings.screen_height / 2)
        self._draw_text(f"The score to beat is currently {round(self.stats.high_score, -1)}", 40, (255, 0, 0),
                        self.settings.screen_width / 2, self.settings.screen_height / 2 - 40)
        self._draw_text("Press any key to continue", 40, (255, 0, 0),
                        self.settings.screen_width / 2, self.settings.screen_height * 3 / 4)
        
        pygame.display.flip()
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

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai._show_intro()
    ai.run_game()