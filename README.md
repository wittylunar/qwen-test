# Cuddly Chainsaw - Enhanced Russian Roulette Game 🎰

#ASASASASASAS college project
#ffffffff russian roulette game
#lazy with fancy effects and cheats

## About

"Cuddly Chainsaw" is a Russian Roulette game with extra features. Made for college assignment.

## Features

### Russian Roulette
- Choose a number between 1-10
- Game generates a random number 1-10
- If your number matches = you lose
- If they don't match = you win double your bet

### Money System
- Start with $100
- Win = double your bet
- Lose = lose your bet
- If you lose all money, get $10 to continue playing

### XP and Levels
- Get XP for playing
- Level up when enough XP
- More XP needed each level

### Shop
- Buy cool stuff:
  - Extra life ($50)
  - Bet doubler ($75)
  - Secret bullet ($100)
  - Safety shield ($150)
  - Lucky number ($200)
  - Bonus round ($300)
  - Golden ticket ($500)
  - Crystal ball ($750)
  - GOD MODE (-$123456789) - Special item that adds huge amount to balance

### Save System
- Save your progress anytime
- Load your saved game later
- Encrypted with base64 to prevent easy modification

### Settings
- Toggle typewriter effect
- Set auto save interval (1-60 minutes)
- Toggle auto save on/off
- Reset all settings

### Cheat Codes
- 1337 - +1000$
- GODMODE - Level 10
- LUCKY - +500 XP
- RICH - +5000$
- NOLOSS - Next game = win
- INSTAWIN - Instant level up
- RESET - Reset everything
- UNLOCK - Unlock all shop items
- LUCKY7 - Next number will be 7
- NOSURPRISE - Disable random events

### Colorful Interface
- Full color support for better visual experience
- Different colors for different menu items and messages

### Module System
- Organized code into separate modules:
  - game.py: Core game mechanics
  - shop.py: Shop system
  - save.py: Save/load system
  - settings.py: Settings management

### Typewriter Effect
- Text appears letter by letter
- Makes it feel cooler

## How to Play

1. Make sure Python 3.x is installed
2. Install dependencies: `pip install -r requirements.txt`
3. Go to project folder: `cd cuddly-chainsaw`
4. Run game: `python src/main.py`
5. Have fun!

## Files

- `src/main.py`: Main entry point
- `modules/game.py`: Core game mechanics
- `modules/shop.py`: Shop system
- `modules/save.py`: Save/load system
- `modules/settings.py`: Settings management
- `savegame.dat`: Encrypted save file (created automatically)
- `settings.json`: Settings file (created automatically)
- `requirements.txt`: Python dependencies
- `pyproject.toml`: Project configuration
- `README.md`: This file

Done for college. MIT license.