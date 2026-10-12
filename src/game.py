from chessboard import Chessboard
from pieces import *
from utils import to_notation
from timers import Timer
from move import Move

class Game:
    """Controls the overall chess game rules, turn cycles, timers, and move execution.

    Attributes:
        board (Chessboard): The active chessboard instance.
        turn (str): Current player turn ('W' or 'B').
        white_timer (Timer): Clock timer for the White player.
        black_timer (Timer): Clock timer for the Black player.
        half_move_clock (int): Half-move clock counter for the 50-move draw rule.
        history (list[Move]): Chronological list of completed moves.
        initial_position_key (tuple or None): State snapshot signature of the starting board.
    """

    def __init__(self, time_limit = 600.0, increment = 0.0):
        """Initializes a new chess game.

        Args:
            time_limit (float, optional): Initial time per player in seconds. Defaults to 600.0.
            increment (float, optional): Time increment per move in seconds. Defaults to 0.0.
        """
        self.board = Chessboard()
        self.turn = "W"
        self.white_timer = Timer(time_limit, increment)
        self.black_timer = Timer(time_limit, increment)
        self.half_move_clock = 0
        self.history = []
        self.initial_position_key = None

    @property
    def board(self):
        """Gets the chessboard instance.

        Returns:
            Chessboard: The game board.
        """
        return self._board
    
    @board.setter
    def board(self, value):
        """Sets the chessboard instance.

        Args:
            value (Chessboard): The game board.

        Raises:
            TypeError: If value is not a Chessboard instance.
        """
        if not isinstance(value, Chessboard):
            raise TypeError("Board must be Chessboard")
        self._board = value

    @property
    def turn(self):
        """Gets the current player's turn.

        Returns:
            str: 'W' for White or 'B' for Black.
        """
        return self._turn
    
    @turn.setter
    def turn(self, value):
        """Sets the current player's turn.

        Args:
            value (str): 'W' or 'B'.

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is not 'W' or 'B'.
        """
        if not isinstance(value, str):
            raise TypeError("Turn must be str")
        if value != "W" and value != "B":
            raise ValueError('Turn must be "W" or "B"')
        self._turn = value

    @property
    def white_timer(self):
        """Gets the timer for the White player.

        Returns:
            Timer: White's timer.
        """
        return self._white_timer
    
    @white_timer.setter
    def white_timer(self, value):
        """Sets the timer for the White player.

        Args:
            value (Timer): White's timer.

        Raises:
            TypeError: If value is not a Timer instance.
        """
        if not isinstance(value, Timer):
            raise TypeError("Timer must be a Timer")
        self._white_timer = value
    
    @property
    def black_timer(self):
        """Gets the timer for the Black player.

        Returns:
            Timer: Black's timer.
        """
        return self._black_timer
    
    @black_timer.setter
    def black_timer(self, value):
        """Sets the timer for the Black player.

        Args:
            value (Timer): Black's timer.

        Raises:
            TypeError: If value is not a Timer instance.
        """
        if not isinstance(value, Timer):
            raise TypeError("Timer must be a Timer")
        self._black_timer = value
        
    @property
    def half_move_clock(self):
        """Gets the half-move clock counter for the 50-move rule.

        Returns:
            int: Number of half-moves since last pawn move or capture.
        """
        return self._half_move_clock
    
    @half_move_clock.setter
    def half_move_clock(self, value):
        """Sets the half-move clock counter for the 50-move rule.

        Args:
            value (int): Half-move counter value.

        Raises:
            TypeError: If value is not an int.
            ValueError: If value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("Counter value must be int")
        if value < 0:
            raise ValueError("Value must be 0 or greater")
        self._half_move_clock = value

    @property
    def history(self):
        """Gets the list of played moves.

        Returns:
            list: Move history list.
        """
        return self._history
    
    @history.setter
    def history(self, value):
        """Sets the list of played moves.

        Args:
            value (list): Move history list.

        Raises:
            TypeError: If value is not a list.
        """
        if not isinstance(value, list):
            raise TypeError("History must be list")
        self._history = value

    def __str__(self):
        """Returns the formatted move history in algebraic notation.

        Returns:
            str: String of moves in format 'A1 -> A2\\n'.
        """
        result = ""
        for move in self.history:
            result += f"{to_notation(move.start)} -> {to_notation(move.end)}\n"
        return result

    def setup_standard_board(self):
        """Sets up initial piece positions and records the starting position signature."""
        for i in range(8):
            self.board.add_piece(Pawn("B"), (i, 1))
            self.board.add_piece(Pawn("W"), (i, 6))

        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for x, piece_class in enumerate(back_rank):
            self.board.add_piece(piece_class("B"), (x, 0))
            self.board.add_piece(piece_class("W"), (x, 7))
            
        self.initial_position_key = self.get_position_key()

    def undo_move(self):
        """Reverts the last move made, restoring pieces and board state."""
        last_move = self.history.pop()
        piece = last_move.piece
        target = last_move.target
        start = last_move.start
        end = last_move.end
        start_x, start_y = start
        end_x, end_y = end
        has_moved = last_move.has_moved
        en_passant_target = last_move.en_passant_target

        # undo castling
        if isinstance(last_move.piece, King) and abs(start_x - end_x) == 2:
            dir_x = 1 if end_x > start_x else -1
            rook_x = 7 if end_x > start_x else 0
            self.board.remove_piece((start_x + dir_x, start_y))
            self.board.add_piece(Rook(piece.color), (rook_x, start_y))

        # undo move
        self.board.remove_piece(end)
        self.board.add_piece(piece, start)

        if isinstance(piece, Rook) or isinstance(piece, King):
            piece.has_moved = has_moved
        
        if target is not None:
            self.board.add_piece(target, end)

        # en passant
        elif (end_x, end_y) == en_passant_target:
            value = 1 if piece.color == "W" else -1
            color = "B" if piece.color == "W" else "W"
            self.board.add_piece(Pawn(color), (end_x, end_y + value))

        self.board.en_passant_target = en_passant_target

    def check(self):
        """Checks whether the current player's king is currently in check.

        Returns:
            bool: True if the current player's king is attacked, False otherwise.
        """
        if self.turn == "W":
            my_king_coords = self.board.white_king_coords
            other_coords = self.board.black_pieces_coords
        else:
            my_king_coords = self.board.black_king_coords
            other_coords = self.board.white_pieces_coords
        
        for coords in other_coords:
            piece = self.board.get_piece_at(coords)
            piece_moves = piece.get_possible_moves(self.board, coords)
            if my_king_coords in piece_moves:
                return True
        return False
    
    def is_insufficient_material(self):
        """Determines if the game is a draw due to insufficient material to checkmate.

        Returns:
            bool: True if insufficient material exists on the board, False otherwise.
        """
        if len(self.board.white_pieces_coords) == 1 and len(self.board.black_pieces_coords) == 1:
            return True
        elif len(self.board.white_pieces_coords) == 1 and len(self.board.black_pieces_coords) <= 2:
            for coords in self.board.black_pieces_coords:
                if not isinstance(self.board.get_piece_at(coords), King) and not isinstance(self.board.get_piece_at(coords), Bishop) and not isinstance(self.board.get_piece_at(coords), Knight):
                    return False
            return True
        elif len(self.board.black_pieces_coords) == 1 and len(self.board.white_pieces_coords) <= 2:
            for coords in self.board.white_pieces_coords:
                if not isinstance(self.board.get_piece_at(coords), King) and not isinstance(self.board.get_piece_at(coords), Bishop) and not isinstance(self.board.get_piece_at(coords), Knight):
                    return False
            return True
        return False
    
    def get_position_key(self, turn = None):
        """Generates an immutable signature of the current board and game state.

        Encapsulates piece layout, castling rights (via piece movement flags),
        player turn, and en passant target coordinates to evaluate FIDE threefold
        repetition rules.

        Args:
            turn (str, optional): The player turn ('W' or 'B') associated with the
                position. Defaults to None, which uses the current game turn.

        Returns:
            tuple[str, str, tuple or None]: A tuple containing the serialized
                64-square grid string, the active player turn, and the en passant
                target coordinates.
        """
        if turn is None:
            turn = self.turn

        pieces = []
        for row in self.board.grid:
            for piece in row:
                if piece is None:
                    pieces.append(".")
                else:
                    pieces.append(f"{piece.color}{type(piece).__name__[0]}{piece.has_moved}")

        return ("".join(pieces), turn, self.board.en_passant_target)

    def is_threefold_repetition(self, current_key):
        """Determines whether the given board state has occurred three or more times.

        Compares the provided state key against the initial board state and all
        historical move snapshots stored in self.history.

        Args:
            current_key (tuple): The position state key generated by get_position_key.

        Returns:
            bool: True if the position has occurred at least 3 times, False otherwise.
        """
        count = 1 if self.initial_position_key == current_key else 0

        for move in self.history:
            if getattr(move, "position_key", None) == current_key:
                count += 1

        return count >= 3

    def get_all_legal_moves(self):
        """Generates all legal (start, end) coordinate moves for the current player.

        Returns:
            list[tuple[tuple[int, int], tuple[int, int]]]: List of tuples with start and end coordinates.
        """
        legal_moves = []
        if self.turn == "W":
            my_coords = list(self.board.white_pieces_coords)
        else:
            my_coords = list(self.board.black_pieces_coords)

        for start in my_coords:
            start_x, start_y = start
            piece = self.board.get_piece_at(start)
            piece_moves = piece.get_possible_moves(self.board, start)

            for end in piece_moves:
                end_x, end_y = end

                # simulate move
                target = self.board.get_piece_at(end)
                self.board.move(start, end)
                self.history.append(Move(start, end, piece, target, self.board.en_passant_target, piece.has_moved, self.half_move_clock))

                if not self.check():
                    # castling comprobations
                    if isinstance(piece, King) and abs(start_x - end_x) == 2:
                        self.undo_move()
                        was_in_check = self.check()
                        dir_x = 1 if end_x > start_x else -1
                        self.board.move(self, start, (start_x + dir_x, start_y))
                        passed_trough_check = self.check()

                        if was_in_check or passed_trough_check:
                            self.undo_move()
                            continue

                    legal_moves.append((start, end))

                self.undo_move()

        return legal_moves
    
    def pawn_promotion(self, coords):
        """Checks if a pawn at coords has reached the opposite end of the board.

        Args:
            coords (tuple): The (x, y) coordinates of the square to check.

        Returns:
            bool: True if the piece at coords is a Pawn on row 0 or 7, False otherwise.
        """
        x, y = coords
        return (y == 0 or y == 7) and isinstance(self.board.get_piece_at(coords), Pawn)
    
    def promotion_to(self, piece, coords):
        """Replaces a pawn at the given coordinates with the promoted piece type.

        Args:
            piece (str): Target piece abbreviation ('Q', 'R', 'B', 'N').
            coords (tuple): The (x, y) board coordinates of the promoting pawn.
        """
        pawn = self.board.get_piece_at(coords)
        self.board.remove_piece(coords)

        if piece == "Q":
            self.board.add_piece(Queen(pawn.color), coords)
        elif piece == "R":
            self.board.add_piece(Rook(pawn.color, has_moved = True), coords)
        elif piece == "B":
            self.board.add_piece(Bishop(pawn.color), coords)
        elif piece == "N":
            self.board.add_piece(Knight(pawn.color), coords)

    def swap_turn(self):
        """Swaps the turn between White ('W') and Black ('B')."""
        if self.turn == "W":
            self.turn = "B"
        else:
            self.turn = "W"

    def play_move(self, start, end):
        """Attempts to play a move from start to end coordinates and updates game state.

        Args:
            start (tuple): The starting (x, y) coordinates.
            end (tuple): The destination (x, y) coordinates.

        Returns:
            str: Move status outcome ('SUCCESS', 'INVALID', 'CHECKMATE', 'STALEMATE',
                'DRAW', or 'TIMEOUT').
        """
        legal_moves = self.get_all_legal_moves()

        # Checkmate and stalemate comprobations
        if len(legal_moves) == 0:
            check = self.check()
            if check:
                return "CHECKMATE"
            return "STALEMATE"
        
        if (start, end) not in legal_moves:
            return "INVALID"
        
        piece = self.board.get_piece_at(start)
        target = self.board.get_piece_at(end)
        self.board.move(start, end)
        
        # 50 moves rule
        if isinstance(piece, Pawn) or target is not None:
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1
        
        if self.half_move_clock == 50:
            return "DRAW"
            
        # Threefold repetition evaluation
        next_turn = "B" if self.turn == "W" else "W"
        current_key = self.get_position_key(turn=next_turn)

        new_move = Move(start, end, piece, target, self.board.en_passant_target, piece.has_moved, self.half_move_clock)
        new_move.position_key = current_key
        self.history.append(new_move)
        
        if self.is_threefold_repetition(current_key):
            return "DRAW"
        
        # Insufficient material
        if self.is_insufficient_material():
            return "DRAW"

        # Timer
        if self.white_timer.is_timeout() or self.black_timer.is_timeout():
                return "TIMEOUT"
        if self.turn == "W":
            self.white_timer.stop()
            self.black_timer.start()
        else:
            self.black_timer.stop()
            self.white_timer.start()
    
        return "SUCCESS"
        