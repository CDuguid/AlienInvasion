import sys
from time import sleep
from random import randint
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet, YellowBullet, RedBullet
from alien import Alien, YellowAlien, RedAlien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from game_sounds import GameSounds

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
        
        self._create_fleet()
        
        # Start Alien Invasion in an inactive state
        self.game_active = False
        
        # Make the Play button
        green = (0, 135, 0)
        self.play_button = Button(self, "Play", green, 0, 100)
        
        # Make the Help button
        blue = (0, 0, 135)
        self.help_button = Button(self, "Help", blue, 0, 0)
        
        # Make the Difficulty button
        red = (135, 0, 0)
        self.difficulty_button = Button(self, "Difficulty", red, 0, -100)
        
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
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
            self._start_game()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()
    
    def _start_game(self):
        """Start a new game from welcome screen."""
        # Reset the game settings
        self.settings.initialise_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True
        
        # Get rid of any remaining aliens and bullets
        self.bullets.empty()
        self.aliens.empty()
        self.yellow_aliens.empty()
        self.red_aliens.empty()
        self.alien_bullets.empty()
        
        # Create a new fleet and centre the ship
        self._create_fleet()
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
            self.alien_bullets, self.ship_sprite, True, True)
        if collisions:
            self._ship_hit()
    
    def start_new_level(self):
        """Start a new wave of aliens."""
        # Destroy existing bullets and increase speed.
        self.bullets.empty()
        self.alien_bullets.empty()
        self.yellow_aliens.empty()
        self.red_aliens.empty()
        self.settings.increase_speed()
        
        # Increase level
        self.stats.level += 1
        self.sb.prep_level()
        
        # Create hard fleet if far enough into game; otherwise create normal fleet
        if self.stats.level >= self.settings.hard_level:
            self._create_hard_fleet()
        else:
            self._create_fleet()
        
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
            self.bullets.empty()
            self.aliens.empty()
            self.yellow_aliens.empty()
            self.red_aliens.empty()
            self.alien_bullets.empty()
            
            # Create a new fleet and centre the ship
            self._create_fleet()
            self.ship.centre_ship()
            
            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship gets hit
                self._ship_hit()
                break
    
    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Create an initial row of yellow aliens
        alien = YellowAlien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_yellow_alien(current_x, current_y)
                current_x += 2 * alien_width
        
        # Create an alien and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width and one alien height
        # Basic fleet moved down a row from initial arrangement
        alien = Alien(self)

        current_x, current_y = alien_width, 3 * alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _create_hard_fleet(self):
        """Create a harder version of the fleet."""
        # Create an initial row of red aliens
        alien = RedAlien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_x < (self.settings.screen_width - 2 * alien_width):
            self._create_red_alien(current_x, current_y)
            current_x += 2 * alien_width
                
        # Create a second row with yellow aliens
        alien = YellowAlien(self)
        current_x, current_y = alien_width, 3 * alien_height
        while current_x < (self.settings.screen_width - 2 * alien_width):
            self._create_yellow_alien(current_x, current_y)
            current_x += 2 * alien_width
        
        # Fill the remaining rows with green aliens
        alien = Alien(self)
        current_x, current_y = alien_width, 5 * alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
                
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
        self.screen.fill(self.settings.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        # Draw the score info
        self.sb.show_score()
        
        # Draw the Play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()
            self.help_button.draw_button()
            self.difficulty_button.draw_button()
        
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()