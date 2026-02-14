# Cuddly Chainsaw - Enhanced Russian Roulette Game 🎰

## Project Overview

Cuddly Chainsaw is an enhanced Russian Roulette game built in Python as a college assignment. The game features a colorful, interactive interface with multiple gameplay systems including betting, progression, shop mechanics, save/load functionality, and cheat codes.

### Key Features
- **Russian Roulette Gameplay**: Players choose a number between 1-10, with the computer generating a random number. Matching numbers result in a loss, while non-matching numbers result in doubled winnings.
- **Money System**: Starting with $100, players can bet and win/lose money based on game outcomes.
- **XP and Leveling**: Players earn XP for playing and can level up when accumulating sufficient XP.
- **Shop System**: Various items can be purchased to enhance gameplay (extra lives, bet doublers, shields, etc.).
- **Save/Load System**: Game progress is encrypted and saved in base64 format.
- **Settings Management**: Configurable options including typewriter effect, auto-save intervals, and more.
- **Cheat Codes**: Multiple cheat codes available for various benefits (money, levels, XP, etc.).
- **Multiplayer Support**: Network-based multiplayer functionality with room creation and joining.
- **Achievements and Daily Challenges**: Progression system with unlockable achievements and daily tasks.
- **Additional Game Modes**: Includes Double or Nothing, Progressive Jackpot, Coin Flip, and Bonus Round games.

### Technologies Used
- Python 3.8+
- Colorama library for colorful terminal output
- JSON for data storage
- Base64 encryption for save files
- Socket programming for multiplayer functionality
- Threading for concurrent operations

## Project Structure
```
cuddly-chainsaw/
├── main.py                 # Main game implementation
├── pyproject.toml          # Poetry project configuration
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License
├── settings.json           # Current settings configuration
├── savegame.dat            # Encrypted save game data
├── savegame.json           # Sample save game data
├── QWEN.md                 # This file
├── test_format.py          # Test file for number formatting
└── modules/
    ├── core.py             # Core game logic and mechanics
    ├── ui.py               # User interface handling
    ├── save.py             # Save/load functionality
    ├── shop.py             # Shop system implementation
    ├── achievements.py     # Achievements and daily challenges
    ├── multiplayer.py      # Multiplayer networking
    └── __pycache__/        # Compiled Python files
```

## Building and Running

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup and Execution
1. Clone or navigate to the project directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or if using Poetry:
   ```bash
   poetry install
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Development Conventions

### Coding Style
- The code follows standard Python PEP 8 conventions
- Class-based organization for game logic
- Modular design with methods for different game systems
- Color-coded output using the Colorama library
- Typewriter effect for enhanced user experience
- Russian language interface (with some English comments)

### Game Architecture
- Main game class inherits from RussianRouletteCore
- Separate modules for different functionality:
  - `core.py`: Core game mechanics and rules
  - `ui.py`: User interface and menu display
  - `save.py`: Save/load and settings management
  - `shop.py`: Shop system and item purchasing
  - `achievements.py`: Achievement tracking and daily challenges
  - `multiplayer.py`: Network-based multiplayer functionality

### Data Storage
- Player data stored in JSON format
- Save files encrypted using base64 encoding with checksums
- Settings stored separately in JSON format
- Cloud sync functionality (simulated) for backup saves
- Anti-cheat mechanisms to detect suspicious activity

## Key Components

### Game Mechanics
- Random number generation for Russian Roulette
- Betting system with win/loss calculations
- Level progression based on XP accumulation
- Anti-cheat detection for suspicious gameplay patterns
- Multiple game modes (Russian Roulette, Double or Nothing, Progressive Jackpot)

### User Interface
- Colorful terminal interface with different colors for menu items
- Typewriter effect for text display (configurable)
- Clear menu navigation and prompts
- Status display showing balance, level, and XP
- Animated text effects for enhanced experience

### Additional Systems
- Shop with multiple purchasable items
- Statistics display showing player progress
- Settings management with configurable options
- Comprehensive achievement system
- Daily challenges with rewards
- Multiplayer functionality with room creation/joining
- Cloud synchronization (simulated)

## Error Handling
- Proper exception handling for input operations (EOFError, KeyboardInterrupt)
- Validation of save file integrity using checksums
- Anti-cheat mechanisms to detect suspicious gameplay
- Graceful handling of network disconnections in multiplayer

## Modules Overview

### Core Module (`core.py`)
Contains the fundamental game mechanics including Russian Roulette rules, betting system, XP/leveling, anti-cheat detection, and additional game modes.

### UI Module (`ui.py`)
Handles all user interface elements including menu display, settings management, and statistics presentation.

### Save Module (`save.py`)
Manages game saving/loading with encryption, settings persistence, and cloud sync simulation.

### Shop Module (`shop.py`)
Implements the in-game store with various items that can be purchased to enhance gameplay.

### Achievements Module (`achievements.py`)
Tracks player achievements, manages daily challenges, and provides bonus rounds and mini-games.

### Multiplayer Module (`multiplayer.py`)
Provides network-based multiplayer functionality with room management and game synchronization.

## Testing
While no formal tests are included in the project, the game can be tested by:
- Playing through various game scenarios
- Testing save/load functionality
- Verifying shop purchases work correctly
- Checking cheat codes activate properly
- Ensuring settings changes are saved
- Testing multiplayer functionality between different machines
- Validating anti-cheat mechanisms respond appropriately

## License
This project is licensed under the MIT License - see the LICENSE file for details.