# Checkers Solver

A full-featured checkers game with AI opponent built using Python FastAPI backend and vanilla JavaScript frontend. Play against the computer or make manual moves with an intuitive web interface.

## Features

- **Interactive Web Interface**: Click-to-move gameplay with visual feedback
- **AI Opponent**: Monte Carlo simulation-based computer player
- **Move Validation**: Real-time validation of legal moves
- **Game History**: Undo functionality to revert moves
- **King Promotion**: Automatic promotion when pieces reach the opposite end
- **Responsive Design**: Works on desktop and mobile devices
- **Multiple Input Methods**: Click-to-move or manual tile input (1-32)

## Screenshots

The game features a clean, modern interface with:
- 8x8 checkers board with proper light/dark square coloring
- Visual piece representation (● for regular pieces, ♚ for kings)
- Highlighted selected pieces and possible moves
- Real-time game status and turn indicator
- Control panel with all game functions

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone or download the project files**
   ```bash
   # Ensure you have all these files in your project directory:
   # - main.py
   # - app.py
   # - index.html
   # - styles.css
   # - script.js
   ```

2. **Install required dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the application**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Open your web browser**
   Navigate to `http://localhost:8000`

## How to Play

### Game Rules

- **Objective**: Capture all opponent pieces or block them from making valid moves
- **Movement**: Pieces move diagonally on dark squares only
- **Regular Pieces**: Move forward one square diagonally
- **Kings**: Can move forward or backward diagonally
- **Capturing**: Jump over opponent pieces diagonally to capture them
- **King Promotion**: Pieces become kings when reaching the opposite end
- **Mandatory Jumps**: If a jump is available, it must be taken

### Controls

#### Interactive Mode (Recommended)
1. Click on one of your pieces to select it
2. Available moves will be highlighted in green
3. Click on the destination square to make the move

#### Manual Input Mode
1. Enter the start tile number (1-32) in the "Start Tile" field
2. Enter the end tile number (1-32) in the "End Tile" field
3. Click "Execute Move"

#### Game Controls
- **Start New Game**: Reset the board for a fresh game
- **Let Computer Make Move**: AI will analyze and make the best move
- **Undo Last Move**: Revert the most recent move
- **Quit Game**: End the current session

### Tile Numbering System

The board uses a 1-32 numbering system for dark squares only:
```
   1   2   3   4
 5   6   7   8
   9  10  11  12
13  14  15  16
  17  18  19  20
21  22  23  24
  25  26  27  28
29  30  31  32
```

## Technical Details

### Architecture

- **Backend**: FastAPI (Python) - Game logic and API endpoints
- **Frontend**: Vanilla JavaScript - User interface and interactions
- **Styling**: CSS with Tailwind classes for responsive design

### Key Components

#### Backend (`main.py`)
- `Game` class: Core game logic, move validation, and board management
- Monte Carlo simulation for AI decision making
- Move history tracking for undo functionality

#### API Layer (`app.py`)
- RESTful endpoints for game operations
- Static file serving for web interface
- Real-time game state management

#### Frontend (`script.js`)
- Interactive board rendering
- Move validation and execution
- Real-time UI updates

### API Endpoints

- `GET /`: Serve the main game interface
- `GET /get_board`: Get current board state and valid moves
- `POST /start`: Start a new game
- `GET /is_valid_move`: Check if a move is valid
- `POST /execute_move`: Execute a player move
- `POST /monte_carlo_simulation`: Get computer move via AI
- `GET /get_winner`: Check for game winner
- `POST /undo_move`: Undo the last move

### AI Algorithm

The computer player uses Monte Carlo Tree Search (MCTS):
1. For each possible move, run multiple random game simulations
2. Score moves based on win/loss outcomes
3. Select the move with the highest average score
4. Configurable simulation count (default: 100)

## Customization

### Adjusting AI Difficulty
Modify the `num_simulations` parameter in the Monte Carlo function:
```python
# In app.py, monte_carlo_simulation endpoint
computer_move = game.monte_carlo_simulation(num_simulations=200)  # Harder
computer_move = game.monte_carlo_simulation(num_simulations=50)   # Easier
```

### Visual Customization
Edit `styles.css` to modify:
- Board colors and appearance
- Piece styling and symbols
- UI theme and layout
- Responsive breakpoints

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure FastAPI and uvicorn are installed: `pip install fastapi uvicorn`

2. **Port already in use**
   - Change the port: `uvicorn app:app --port 8001`
   - Or kill the process using port 8000

3. **Game not responding**
   - Check browser console for JavaScript errors
   - Ensure all files are in the same directory
   - Verify the FastAPI server is running

4. **Moves not working**
   - Ensure you're clicking on dark squares only
   - Check that it's your turn (white moves first)
   - Verify the move follows checkers rules

### Development Mode

For development with auto-reload:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Contributing

Feel free to submit issues and enhancement requests! Some areas for improvement:
- Enhanced AI algorithms (Alpha-Beta pruning, deeper search)
- Multiplayer support
- Game statistics and analysis
- Tournament mode
- Save/load game functionality

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with FastAPI for the backend API
- Uses vanilla JavaScript for cross-browser compatibility
- Styled with modern CSS and Tailwind classes
- Monte Carlo algorithm implementation for AI gameplay
