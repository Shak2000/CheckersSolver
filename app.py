from fastapi import FastAPI
from fastapi.responses import FileResponse
from main import Game

game = Game()
app = FastAPI()


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


@app.post("/start")
async def start():
    game.start()


@app.post("/convert")
async def convert(tile):
    game.convert(tile)


@app.get("/is_valid_move")
async def is_valid_move(x1, y1, x2, y2):
    return game.is_valid_move(x1, y1, x2, y2)


@app.post("/execute_move")
async def execute_move(x1, y1, x2, y2):
    game.execute_move(x1, y1, x2, y2)


@app.get("/get_winner")
async def get_winner():
    return game.get_winner()


@app.post("/monte_carlo_simulation")
async def monte_carlo_simulation(num_simulations=100):
    game.monte_carlo_simulation(num_simulations)


@app.post("/undo_move")
async def undo_move():
    game.undo_move()
