class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialise the game's static settings."""
        # Ship settings
        self.ship_limit = 3
        
        # Bullet settings        
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 10
        self.yellow_bullet_chance = 3
        self.red_bullet_chance = 6
                
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        
        self.initialise_dynamic_settings()
    
    def initialise_dynamic_settings(self):
        """Initialise the settings that change over the game."""
        self.ship_speed = 2.0
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        
        # Scoring settings
        self.alien_points = 50
    
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)