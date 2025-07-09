import random
import copy


class Game:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.history = []
        self.current_turn = 'w'  # 'w' for white, 'b' for black

    def start(self):
        """Initializes the board for a new game."""
        self.history = []
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        # Place black pieces
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'b'
        # Place white pieces
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'w'
        self.current_turn = 'w'

    def convert(self, tile):
        """
        Converts a 1-32 tile number to (x, y) coordinates on the board.
        Returns (-1, -1) for invalid tile numbers.
        """
        if tile < 1 or tile > 32:
            return -1, -1
        # Checkers board mapping (example for 1-32)
        # Row 0: 1, 2, 3, 4
        # Row 1: 5, 6, 7, 8
        # ...
        # Row 7: 29, 30, 31, 32

        # Calculate row (y)
        y = (tile - 1) // 4

        # Calculate column (x)
        if y % 2 == 0:  # Even rows (0, 2, 4, 6) have pieces on odd columns (1, 3, 5, 7)
            x = ((tile - 1) % 4) * 2 + 1
        else:  # Odd rows (1, 3, 5, 7) have pieces on even columns (0, 2, 4, 6)
            x = ((tile - 1) % 4) * 2

        return x, y

    def convert_to_tile(self, x, y):
        """
        Converts (x, y) coordinates to a 1-32 tile number.
        Returns -1 for invalid coordinates.
        """
        if not (0 <= x < 8 and 0 <= y < 8 and (x + y) % 2 == 1):
            return -1

        tile = 0
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == 1:  # Only dark squares have pieces
                    tile += 1
                if r == y and c == x:
                    return tile
        return -1

    def is_valid_move(self, x1, y1, x2, y2):
        """
        Checks if a move from (x1, y1) to (x2, y2) is valid.
        Considers regular moves and jumps.
        """
        if not (0 <= x1 < 8 and 0 <= y1 < 8 and 0 <= x2 < 8 and 0 <= y2 < 8):
            return False  # Out of bounds
        if self.board[y1][x1] == '.':
            return False  # No piece at start position
        if self.board[y2][x2] != '.':
            return False  # Destination is not empty

        piece = self.board[y1][x1]
        is_king = piece.isupper()
        player_color = piece.lower()

        if player_color != self.current_turn:
            return False  # Not current player's piece

        dx = x2 - x1
        dy = y2 - y1

        # Regular move
        if abs(dx) == 1 and abs(dy) == 1:
            if player_color == 'w' and dy == -1:  # White moves up
                return True
            elif player_color == 'b' and dy == 1:  # Black moves down
                return True
            elif is_king and abs(dy) == 1:  # Kings can move in any diagonal direction
                return True

        # Jump move
        if abs(dx) == 2 and abs(dy) == 2:
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            captured_piece = self.board[mid_y][mid_x]

            if captured_piece == '.':
                return False  # No piece to jump over

            captured_color = captured_piece.lower()

            if player_color == 'w' and captured_color == 'b' and dy == -2:  # White jumps black up
                return True
            elif player_color == 'b' and captured_color == 'w' and dy == 2:  # Black jumps white down
                return True
            elif is_king and captured_color != player_color and abs(dy) == 2:  # King jumps any opponent piece
                return True

        return False

    def get_all_valid_moves(self, board, player_color):
        """
        Returns a list of all valid moves (start_x, start_y, end_x, end_y) for the given player on the given board.
        Prioritizes jumps.
        """
        moves = []
        jumps = []

        for y1 in range(8):
            for x1 in range(8):
                piece = board[y1][x1]
                if piece != '.' and piece.lower() == player_color:
                    for y2 in range(8):
                        for x2 in range(8):
                            if self.is_valid_move_on_board(board, x1, y1, x2, y2, player_color):
                                dx = x2 - x1
                                dy = y2 - y1
                                if abs(dx) == 2 and abs(dy) == 2:
                                    jumps.append((x1, y1, x2, y2))
                                else:
                                    moves.append((x1, y1, x2, y2))
        return jumps if jumps else moves  # Prioritize jumps

    def is_valid_move_on_board(self, board, x1, y1, x2, y2, player_color):
        """
        A helper function for get_all_valid_moves that checks validity on a given board state.
        """
        if not (0 <= x1 < 8 and 0 <= y1 < 8 and 0 <= x2 < 8 and 0 <= y2 < 8):
            return False
        if board[y1][x1] == '.':
            return False
        if board[y2][x2] != '.':
            return False

        piece = board[y1][x1]
        is_king = piece.isupper()
        current_piece_color = piece.lower()

        if current_piece_color != player_color:
            return False

        dx = x2 - x1
        dy = y2 - y1

        # Regular move
        if abs(dx) == 1 and abs(dy) == 1:
            if player_color == 'w' and dy == -1:
                return True
            elif player_color == 'b' and dy == 1:
                return True
            elif is_king and abs(dy) == 1:
                return True

        # Jump move
        if abs(dx) == 2 and abs(dy) == 2:
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            captured_piece = board[mid_y][mid_x]

            if captured_piece == '.':
                return False

            captured_color = captured_piece.lower()

            if player_color == 'w' and captured_color == 'b' and dy == -2:
                return True
            elif player_color == 'b' and captured_color == 'w' and dy == 2:
                return True
            elif is_king and captured_color != player_color and abs(dy) == 2:
                return True

        return False

    def execute_move(self, x1, y1, x2, y2):
        """
        Executes a move on the board and updates history.
        Assumes the move is valid.
        """
        self.history.append(copy.deepcopy((self.board, self.current_turn)))  # Store board state and turn
        piece = self.board[y1][x1]
        self.board[y2][x2] = piece
        self.board[y1][x1] = '.'

        # Check for jump and remove captured piece
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) == 2 and abs(dy) == 2:
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            self.board[mid_y][mid_x] = '.'

        # Check for king promotion
        if piece.lower() == 'w' and y2 == 0:
            self.board[y2][x2] = 'W'  # Promote white to king
        elif piece.lower() == 'b' and y2 == 7:
            self.board[y2][x2] = 'B'  # Promote black to king

        self.switch_turn()

    def switch_turn(self):
        """Switches the current player's turn."""
        self.current_turn = 'b' if self.current_turn == 'w' else 'w'

    def undo_move(self):
        """Undoes the latest move by restoring the previous board state and turn."""
        if self.history:
            self.board, self.current_turn = self.history.pop()
            print("Move undone.")
        else:
            print("No moves to undo.")

    def display_board(self):
        """Prints the current state of the checkers board."""
        print("\n  1 2 3 4 5 6 7 8")
        print(" +-----------------+")
        for r_idx, row in enumerate(self.board):
            print(f"{r_idx}|", end="")
            for c_idx, piece in enumerate(row):
                if (r_idx + c_idx) % 2 == 1:  # Dark squares where pieces can be
                    print(f" {piece}", end="")
                else:  # Light squares
                    print("  ", end="")
            print("|")
        print(" +-----------------+")
        print(f"Current Turn: {'White' if self.current_turn == 'w' else 'Black'}")

    def get_winner(self):
        """
        Determines if there's a winner.
        Returns 'w' for white, 'b' for black, or None if no winner yet.
        """
        white_pieces = 0
        black_pieces = 0
        for r in range(8):
            for c in range(8):
                if self.board[r][c].lower() == 'w':
                    white_pieces += 1
                elif self.board[r][c].lower() == 'b':
                    black_pieces += 1

        if white_pieces == 0:
            return 'b'  # Black wins
        if black_pieces == 0:
            return 'w'  # White wins
        return None

    def monte_carlo_simulation(self, num_simulations=100):
        """
        Runs Monte Carlo simulations to find the best move for the current player.
        """
        current_player = self.current_turn
        opponent_player = 'b' if current_player == 'w' else 'w'
        possible_moves = self.get_all_valid_moves(self.board, current_player)

        if not possible_moves:
            return None  # No moves available

        move_wins = {move: 0 for move in possible_moves}

        for move in possible_moves:
            for _ in range(num_simulations):  # Distribute simulations
                sim_game = copy.deepcopy(self)  # Create a deep copy for simulation
                x1, y1, x2, y2 = move
                sim_game.execute_move(x1, y1, x2, y2)  # Make the first move

                # Simulate the rest of the game
                while sim_game.get_winner() is None and sim_game.get_all_valid_moves(sim_game.board,
                                                                                     sim_game.current_turn):
                    next_player_moves = sim_game.get_all_valid_moves(sim_game.board, sim_game.current_turn)
                    if not next_player_moves:
                        break  # No moves for current player in simulation
                    random_move = random.choice(next_player_moves)
                    sim_game.execute_move(*random_move)

                winner = sim_game.get_winner()
                if winner == current_player:
                    move_wins[move] += 1
                elif winner == opponent_player:
                    move_wins[move] -= 1  # Penalize moves that lead to opponent wins

        best_move = None
        max_wins = -float('inf')

        for move, wins in move_wins.items():
            if wins > max_wins:
                max_wins = wins
                best_move = move
        return best_move


def main():
    game = Game()
    print("Welcome to the Checkers Solver!")

    while True:
        game.display_board()
        print("\nChoose an option:")
        print("1. Start a new game")
        print("2. Make a move (e.g., 10 14)")
        print("3. Let the computer make a move")
        print("4. Undo the latest move")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            game.start()
            print("New game started!")
        elif choice == '2':
            try:
                move_input = input(f"Enter your move (start_tile end_tile) for {game.current_turn.upper()}: ")
                start_tile, end_tile = map(int, move_input.split())
                x1, y1 = game.convert(start_tile)
                x2, y2 = game.convert(end_tile)

                if x1 == -1 or y1 == -1 or x2 == -1 or y2 == -1:
                    print("Invalid tile numbers. Please use numbers between 1 and 32.")
                    continue

                if game.is_valid_move(x1, y1, x2, y2):
                    game.execute_move(x1, y1, x2, y2)
                    print(f"Move from {start_tile} to {end_tile} executed.")
                    winner = game.get_winner()
                    if winner:
                        print(f"Game Over! {'White' if winner == 'w' else 'Black'} wins!")
                        break
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter two numbers separated by a space.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif choice == '3':
            print(f"Computer ({game.current_turn.upper()}) is thinking...")
            computer_move = game.monte_carlo_simulation(num_simulations=100)
            if computer_move:
                x1, y1, x2, y2 = computer_move
                start_tile = game.convert_to_tile(x1, y1)
                end_tile = game.convert_to_tile(x2, y2)
                print(f"Computer moves from {start_tile} to {end_tile}.")
                game.execute_move(x1, y1, x2, y2)
                winner = game.get_winner()
                if winner:
                    print(f"Game Over! {'White' if winner == 'w' else 'Black'} wins!")
                    break
            else:
                print("Computer has no valid moves. Game might be over or stuck.")
        elif choice == '4':
            game.undo_move()
        elif choice == '5':
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
