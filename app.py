from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Game  # Assuming main.py is in the same directory

# Initialize the game instance
game = Game()
app = FastAPI()


# Pydantic model for move data
class MoveData(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


@app.get("/")
async def get_ui():
    """Serves the main HTML page."""
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    """Serves the CSS file."""
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    """Serves the JavaScript file."""
    return FileResponse("script.js")


@app.get("/get_board")
async def get_board():
    """Returns the current state of the board and current turn, and all valid moves."""
    # Ensure the board is initialized if it's a fresh start
    if not any(piece != '.' for row in game.board for piece in row):
        game.start()
    return {
        "board": game.board,
        "current_turn": game.current_turn,
        "all_valid_moves": game.get_all_valid_moves(game.board, game.current_turn)
    }


@app.post("/start")
async def start():
    """Starts a new game."""
    game.start()
    return {"message": "New game started!"}


@app.get("/is_valid_move")
async def is_valid_move(x1: int, y1: int, x2: int, y2: int):
    """Checks if a move is valid."""
    return game.is_valid_move(x1, y1, x2, y2)


@app.post("/execute_move")
async def execute_move(move: MoveData):
    """Executes a move."""
    x1, y1, x2, y2 = move.x1, move.y1, move.x2, move.y2
    # It's good practice to re-validate on the server side, even if frontend checks
    if not game.is_valid_move(x1, y1, x2, y2):
        raise HTTPException(status_code=400, detail="Invalid move attempted.")

    game.execute_move(x1, y1, x2, y2)
    winner = game.get_winner()
    if winner:
        return {"message": f"Move executed. Game Over! {'White' if winner == 'w' else 'Black'} wins!", "winner": winner}
    return {"message": "Move executed successfully.", "winner": None}


@app.post("/monte_carlo_simulation")
async def monte_carlo_simulation(num_simulations: int = 100):
    """Lets the computer make a move using Monte Carlo simulation."""
    computer_move = game.monte_carlo_simulation(num_simulations)
    if computer_move:
        x1, y1, x2, y2 = computer_move
        # Execute the computer's move on the actual game board
        game.execute_move(x1, y1, x2, y2)
        winner = game.get_winner()
        if winner:
            return {
                "message": f"Computer moved. Game Over! {'White' if winner == 'w' else 'Black'} wins!",
                "move": computer_move,
                "winner": winner
            }
        return {"message": "Computer made a move.", "move": computer_move, "winner": None}
    raise HTTPException(status_code=400, detail="Computer has no valid moves or game is over.")


@app.get("/get_winner")
async def get_winner():
    """Returns the current winner, if any."""
    return game.get_winner()


@app.post("/undo_move")
async def undo_move():
    """Undoes the latest move."""
    if game.history:
        game.undo_move()
        return {"message": "Move undone."}
    raise HTTPException(status_code=400, detail="No moves to undo.")
