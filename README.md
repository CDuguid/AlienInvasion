# Alien Invasion

## Project Overview

This is a Space Invaders-like game written in Python which uses the Pygame library. It started life as a tutorial project from Eric Matthes' excellent book *Python Crash Course*, but has since been substantially expanded as a way for me to learn more about the Python language.

Some of the changes include:
- Additional alien types with different probabilities of shooting back at the player. The number of more difficult aliens will increase as the level does.
- Pixel-perfect collision detection with the player's sprite using masks. This prevents the feeling of being cheated by a 'collision' with empty space due to a mismatch between a player's rectangular hitbox and their non-rectangular image.
- An explosion animation when aliens are hit by the player's shots.
- A main menu with buttons to control the starting level and access help info.
- A variety of background music tracks, along with sound effects.
- A high score system to track the player's progress.

If you have any suggestions for interesting modifications (or bugs), please get in touch!


![Game screenshot](https://github.com/user-attachments/assets/eb64e8a2-318b-4bba-a6e1-c4488620a5dd)


## Running the game

### Via .exe
If you are on Windows, I have created a .exe file which you can download and run. This method is self-contained and doesn't require the installation of anything. Head to [Releases](https://github.com/CDuguid/AlienInvasion/releases) and download the .zip file. After extracting it, you should see AlienInvasion.exe - double-click this to run the game.

At this point in time, Mac and Linux distributions don't have an executable provided and will need to follow the directions below.

### Installation
If you have [Python](https://www.python.org/downloads/) installed, you can run the code directly. Assuming [git](https://git-scm.com/downloads) is also installed, navigate to where you want to store the files and open the terminal. Enter either `git clone https://github.com/CDuguid/AlienInvasion.git` or `git clone git@github.com:CDuguid/AlienInvasion.git`. Then move into the directory just created with `cd AlienInvasion`.

The project requires pygame and a popup manager module to be installed. It's recommended that you use a [virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) to do this, but the choice is yours. After setting up and activating the virtual environment, enter `pip install -r requirements.txt`.

It should then be a simple matter of entering `python alien_invasion.py` to run the game.

### Gameplay
The gameplay controls are straightforward: the left and right arrow keys control your movement, and spacebar shoots. For some useful keyboard shortcuts, see the Help section from the main menu. Note that you're limited to 3 active bullets in the air at once.


## TODO

- The game currently displays the highest score achieved. But arcades show a top list, along with initials. Flesh out the high score system.
- There is no in-game volume control. Implement a sliding scale or volume selection box for this.

## Credits

Ship:
[Sci-fi hover tank by Kingshemboo](https://opengameart.org/content/sci-fi-hover-tank)

Ship Bullets:
[Bullets Game Asset by bevouliin](https://opengameart.org/content/bullets-game-asset)

Aliens:
[Space Invaders Cartoon Icon by Fupi](https://opengameart.org/content/space-invaders-cartoon-icon)

Alien Bullets:
[Spaceship Bullet by vergil1018](https://opengameart.org/content/spaceship-bullet)

Background Image:
[Space by Kutejnikov](https://opengameart.org/content/space-9)

Explosion Images:
[Explosion Animation by den_yes](https://opengameart.org/content/explosion-animation-1)

Music and Sounds:
[Various tracks by Eric Matyas](https://soundimage.org)
