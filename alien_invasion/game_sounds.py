from os import path
import pygame

sounds_dir = path.join(path.dirname(__file__), 'assets', 'sounds')

class GameSounds:
    """Play music and sound effects for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialise mixer and pull game level."""
        pygame.mixer.init()
        self.stats = ai_game.stats
        
        self.channel_bullet = pygame.mixer.Channel(0)
        self.channel_alien = pygame.mixer.Channel(1)
        self.channel_ship = pygame.mixer.Channel(2)
    
    def play_main_theme(self):
        """Plays the main soundtrack in welcome screen."""
        pygame.mixer.music.load(path.join(sounds_dir, 'soundtrack_0.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    
    def play_level_theme(self):
        """Stops last soundtrack and plays the soundtrack for a level."""
        pygame.mixer.music.stop()
        soundtrack_range = 4
        if (self.stats.level % soundtrack_range) == 1:
            pygame.mixer.music.load(path.join(sounds_dir, 'soundtrack_1.mp3'))
        elif (self.stats.level % soundtrack_range) == 2:
            pygame.mixer.music.load(path.join(sounds_dir, 'soundtrack_2.mp3'))
        elif (self.stats.level % soundtrack_range) == 3:
            pygame.mixer.music.load(path.join(sounds_dir, 'soundtrack_3.mp3'))
        elif (self.stats.level % soundtrack_range) == 0:
            pygame.mixer.music.load(path.join(sounds_dir, 'soundtrack_4.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    
    def play_bullet_sound(self):
        """Plays the sound for a bullet being fired."""
        sound = pygame.mixer.Sound(path.join(sounds_dir, 'firing_bullet.mp3'))
        sound.set_volume(1.2)
        self.channel_bullet.play(sound)
    
    def play_alien_hit_sound(self):
        """Plays the sound for an alien being hit."""
        sound = pygame.mixer.Sound(path.join(sounds_dir, 'alien_hit.mp3'))
        sound.set_volume(0.6)
        self.channel_alien.play(sound)
    
    def play_ship_hit_sound(self):
        """Plays the sound for the ship being lost."""
        sound = pygame.mixer.Sound(path.join(sounds_dir, 'ship_lost.mp3'))
        sound.set_volume(1.5)
        self.channel_ship.play(sound)