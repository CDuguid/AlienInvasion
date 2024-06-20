from pathlib import Path

class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialise statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Access the saved high score
        self.score_path = Path('high_score.txt')
        self.high_score = int(self.score_path.read_text())
    
    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1