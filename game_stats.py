from pathlib import Path
import os

text_dir = os.path.join(os.path.dirname(__file__), 'text')

class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialise statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.reset_level()
        
        # Access the saved high score
        self.score_path = Path(os.path.join(text_dir, 'high_score.txt'))
        self.high_score = int(self.score_path.read_text())
    
    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
    
    def reset_level(self):
        """Initialise the starting level separately from other statistics."""
        self.level = 1