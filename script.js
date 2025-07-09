document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('checkers-board');
    const currentTurnDisplay = document.getElementById('current-turn');
    const gameMessageDisplay = document.getElementById('game-message');
    const newGameBtn = document.getElementById('new-game-btn');
    const startTileInput = document.getElementById('start-tile-input');
    const endTileInput = document.getElementById('end-tile-input');
    const makeMoveBtn = document.getElementById('make-move-btn');
    const computerMoveBtn = document.getElementById('computer-move-btn');
    const undoMoveBtn = document.getElementById('undo-move-btn');
    const quitBtn = document.getElementById('quit-btn');

    let selectedSquare = null; // Stores the currently selected square element
    let selectedCoords = { x: -1, y: -1 }; // Stores the coordinates of the selected piece

    // Function to convert (x, y) coordinates to a 1-32 tile number
    function convertToTile(x, y) {
        if (x < 0 || x > 7 || y < 0 || y > 7) {
            return -1;
        }
        // Check if the square is a dark square (where pieces are)
        if ((x + y) % 2 === 0) { // Light squares have (x+y) even
            return -1;
        }

        let tile = 0;
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                if ((r + c) % 2 === 1) { // Only dark squares are numbered
                    tile++;
                }
                if (r === y && c === x) {
                    return tile;
                }
            }
        }
        return -1; // Should not reach here for valid dark squares
    }

    // Function to convert a 1-32 tile number to (x, y) coordinates
    function convertToCoords(tile) {
        if (tile < 1 || tile > 32) {
            return { x: -1, y: -1 };
        }

        let count = 0;
        for (let y = 0; y < 8; y++) {
            for (let x = 0; x < 8; x++) {
                if ((x + y) % 2 === 1) { // Dark squares
                    count++;
                    if (count === tile) {
                        return { x, y };
                    }
                }
            }
        }
        return { x: -1, y: -1 }; // Should not reach here for valid tiles
    }


    // Function to fetch the current board state from the backend
    async function fetchBoardState() {
        try {
            const response = await fetch('/get_board');
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail || 'Unknown error'}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching board state:', error);
            gameMessageDisplay.textContent = `Error fetching board state: ${error.message}`;
            return null;
        }
    }

    // Function to render the checkers board
    async function renderBoard() {
        boardElement.innerHTML = ''; // Clear existing board
        const boardState = await fetchBoardState();
        if (!boardState) return;

        const board = boardState.board;
        const currentTurn = boardState.current_turn;
        const allValidMoves = boardState.all_valid_moves; // Get all valid moves from backend

        currentTurnDisplay.textContent = `Current Turn: ${currentTurn === 'w' ? 'White' : 'Black'}`;
        gameMessageDisplay.textContent = ''; // Clear previous messages

        for (let y = 0; y < 8; y++) {
            for (let x = 0; x < 8; x++) {
                const square = document.createElement('div');
                square.classList.add('square');
                const isDarkSquare = (x + y) % 2 === 1;

                if (isDarkSquare) {
                    square.classList.add('dark-square');
                } else {
                    square.classList.add('light-square');
                }

                const piece = board[y][x];
                if (piece !== '.') {
                    const pieceElement = document.createElement('div');
                    pieceElement.classList.add('piece');
                    if (piece.toLowerCase() === 'w') {
                        pieceElement.classList.add('white');
                    } else {
                        pieceElement.classList.add('black');
                    }
                    if (piece.toUpperCase() === piece && piece !== '.') { // Check if it's a king (uppercase)
                        pieceElement.classList.add('king');
                        pieceElement.textContent = '♚'; // King symbol
                    } else {
                        pieceElement.textContent = '●'; // Regular piece symbol
                    }
                    square.appendChild(pieceElement);
                }

                // Add data attributes for coordinates
                square.dataset.x = x;
                square.dataset.y = y;

                // Add click listener for piece selection/movement
                if (isDarkSquare) {
                    square.addEventListener('click', handleSquareClick);
                }

                boardElement.appendChild(square);
            }
        }
        checkWinner(); // Check for winner after rendering board
    }

    // Handle square clicks for interactive moves
    async function handleSquareClick(event) {
        const clickedSquare = event.currentTarget;
        const x = parseInt(clickedSquare.dataset.x);
        const y = parseInt(clickedSquare.dataset.y);

        // Clear previous selections and possible moves highlights
        document.querySelectorAll('.square').forEach(s => {
            s.classList.remove('selected', 'possible-move');
        });

        if (selectedSquare === null) {
            // No piece selected yet, try to select this one
            const boardState = await fetchBoardState();
            if (!boardState) return;
            const piece = boardState.board[y][x];
            const currentTurn = boardState.current_turn;

            if (piece !== '.' && piece.toLowerCase() === currentTurn) {
                selectedSquare = clickedSquare;
                selectedCoords = { x, y };
                clickedSquare.classList.add('selected');
                gameMessageDisplay.textContent = `Selected piece at tile ${convertToTile(x, y)}. Now select destination.`;

                // Highlight possible moves for the selected piece
                const allPossibleMoves = boardState.all_valid_moves || [];
                allPossibleMoves.forEach(move => {
                    if (move[0] === x && move[1] === y) {
                        const targetSquare = document.querySelector(`.square[data-x="${move[2]}"][data-y="${move[3]}"]`);
                        if (targetSquare) {
                            targetSquare.classList.add('possible-move');
                        }
                    }
                });
            } else {
                gameMessageDisplay.textContent = 'No piece or not your turn. Please select your own piece.';
            }
        } else {
            // A piece is already selected, this is the destination
            const startX = selectedCoords.x;
            const startY = selectedCoords.y;
            const endX = x;
            const endY = y;

            const startTile = convertToTile(startX, startY);
            const endTile = convertToTile(endX, endY);

            startTileInput.value = startTile;
            endTileInput.value = endTile;

            // Automatically try to make the move
            await makeMove();

            // Reset selection after attempt
            selectedSquare = null;
            selectedCoords = { x: -1, y: -1 };
        }
    }


    // Function to make a move
    async function makeMove() {
        const startTile = parseInt(startTileInput.value);
        const endTile = parseInt(endTileInput.value);

        if (isNaN(startTile) || isNaN(endTile) || startTile < 1 || startTile > 32 || endTile < 1 || endTile > 32) {
            gameMessageDisplay.textContent = 'Please enter valid tile numbers (1-32).';
            return;
        }

        const { x: x1, y: y1 } = convertToCoords(startTile);
        const { x: x2, y: y2 } = convertToCoords(endTile);

        if (x1 === -1 || y1 === -1 || x2 === -1 || y2 === -1) {
            gameMessageDisplay.textContent = 'Invalid tile numbers or not a valid square.';
            return;
        }

        try {
            // First, check if the move is valid
            const isValidResponse = await fetch(`/is_valid_move?x1=${x1}&y1=${y1}&x2=${x2}&y2=${y2}`);
            if (!isValidResponse.ok) {
                const errorData = await isValidResponse.json();
                throw new Error(`HTTP error! status: ${isValidResponse.status}, detail: ${errorData.detail || 'Unknown error'}`);
            }
            const isValid = await isValidResponse.json(); // is_valid_move returns boolean directly

            if (isValid) {
                // If valid, execute the move
                const executeResponse = await fetch('/execute_move', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ x1, y1, x2, y2 })
                });
                if (!executeResponse.ok) {
                    const errorData = await executeResponse.json();
                    throw new Error(`HTTP error! status: ${executeResponse.status}, detail: ${errorData.detail || 'Unknown error'}`);
                }
                const result = await executeResponse.json();

                gameMessageDisplay.textContent = result.message;
                await renderBoard(); // Re-render board to show changes
                if (result.winner) {
                    gameMessageDisplay.textContent = `Game Over! ${result.winner === 'w' ? 'White' : 'Black'} wins!`;
                    disableControls();
                }
            } else {
                gameMessageDisplay.textContent = 'Invalid move. Please try again.';
            }
        } catch (error) {
            console.error('Error making move:', error);
            gameMessageDisplay.textContent = `An error occurred while trying to make the move: ${error.message}`;
        } finally {
            startTileInput.value = '';
            endTileInput.value = '';
            selectedSquare = null; // Reset selection
            selectedCoords = { x: -1, y: -1 };
            document.querySelectorAll('.square').forEach(s => {
                s.classList.remove('selected', 'possible-move');
            });
        }
    }

    // Function to check for a winner
    async function checkWinner() {
        try {
            const response = await fetch('/get_winner');
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail || 'Unknown error'}`);
            }
            const winner = await response.json();
            if (winner) {
                gameMessageDisplay.textContent = `Game Over! ${winner === 'w' ? 'White' : 'Black'} wins!`;
                disableControls();
            }
        } catch (error) {
            console.error('Error checking winner:', error);
            gameMessageDisplay.textContent = `Error checking for winner: ${error.message}`;
        }
    }

    function disableControls() {
        newGameBtn.disabled = true;
        makeMoveBtn.disabled = true;
        computerMoveBtn.disabled = true;
        undoMoveBtn.disabled = true;
        startTileInput.disabled = true;
        endTileInput.disabled = true;
    }

    function enableControls() {
        newGameBtn.disabled = false;
        makeMoveBtn.disabled = false;
        computerMoveBtn.disabled = false;
        undoMoveBtn.disabled = false;
        startTileInput.disabled = false;
        endTileInput.disabled = false;
    }


    // Event Listeners
    newGameBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/start', { method: 'POST' });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail || 'Unknown error'}`);
            }
            const result = await response.json();
            gameMessageDisplay.textContent = result.message;
            await renderBoard();
            enableControls(); // Re-enable controls for new game
        } catch (error) {
            console.error('Error starting new game:', error);
            gameMessageDisplay.textContent = `Error starting new game: ${error.message}`;
        }
    });

    makeMoveBtn.addEventListener('click', makeMove);

    computerMoveBtn.addEventListener('click', async () => {
        gameMessageDisplay.textContent = 'Computer is thinking...';
        try {
            const response = await fetch('/monte_carlo_simulation', { method: 'POST' });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail || 'Unknown error'}`);
            }
            const result = await response.json();
            if (result.move) {
                const startTile = convertToTile(result.move[0], result.move[1]);
                const endTile = convertToTile(result.move[2], result.move[3]);
                gameMessageDisplay.textContent = `Computer moved from tile ${startTile} to ${endTile}.`;
                await renderBoard();
                if (result.winner) {
                    gameMessageDisplay.textContent = `Game Over! ${result.winner === 'w' ? 'White' : 'Black'} wins!`;
                    disableControls();
                }
            } else {
                gameMessageDisplay.textContent = result.message || 'Computer has no valid moves or game is over.';
            }
        } catch (error) {
            console.error('Error with computer move:', error);
            gameMessageDisplay.textContent = `An error occurred while computer was making a move: ${error.message}`;
        }
    });

    undoMoveBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/undo_move', { method: 'POST' });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail || 'Unknown error'}`);
            }
            const result = await response.json();
            gameMessageDisplay.textContent = result.message;
            await renderBoard();
        } catch (error) {
            console.error('Error undoing move:', error);
            gameMessageDisplay.textContent = `Error undoing move: ${error.message}`;
        }
    });

    quitBtn.addEventListener('click', () => {
        gameMessageDisplay.textContent = 'Game quit. Refresh to start a new session.';
        disableControls();
    });

    // Initial render of the board when the page loads
    renderBoard();
});
