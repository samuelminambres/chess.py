from chessboard import Chessboard
from pieces import *
import time
from utils import to_coords, to_notation

class Game:

    def __init__(self, time_limit = 600.0):
        self.board = Chessboard()
        self.turn = "W"
        self.white_timer = time_limit
        self.black_timer = time_limit
        self.turn_time = time.time()
        self.history = []

    @property
    def board(self):
        return self._board
    
    @board.setter
    def board(self, value):
        if not isinstance(value, Chessboard):
            raise TypeError("Board must be Chessboard")
        self._board = value

    @property
    def turn(self):
        return self._turn
    
    @turn.setter
    def turn(self, value):
        if not isinstance(value, str):
            raise TypeError("Turn must be str")
        if value != "W" and value != "B":
            raise ValueError('Turn must be "W" or "B"')
        self._turn = value

    @property
    def white_timer(self):
        return self._white_timer
    
    @white_timer.setter
    def white_timer(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Time must be a number")
        if value <= 0:
            raise ValueError("Time must greater than 0")
        self._white_timer = value
    
    @property
    def black_timer(self):
        return self._black_timer
    
    @black_timer.setter
    def black_timer(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Time must be a number")
        if value <= 0:
            raise ValueError("Time must greater than 0")
        self._black_timer = value

    @property
    def turn_time(self):
        return self._turn_time
    
    @turn_time.setter
    def turn_time(self, value):
        if not isinstance(value, float):
            raise TypeError("Turn time must be float")
        if value <= 0:
            raise ValueError("Turn time must be positive")
        self._turn_time = value

    @property
    def history(self):
        return self._history
    
    @history.setter
    def history(self, value):
        if not isinstance(value, list):
            raise TypeError("History must be list")
        self._history = value

    def __str__(self):
        result = ""
        for move in self.history:
            result += f"\n{type(move["piece"]).__name__}: {to_notation(move["start"])} -> {to_notation(move["end"])}"
        return result

    def setup_standard_board(self):
        for i in range(8):
            self.board.add_piece(Pawn("B"), i, 1)
            self.board.add_piece(Pawn("W"), i, 6)
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for x, piece_class in enumerate(back_rank):
            self.board.add_piece(piece_class("B"), x, 0)
            self.board.add_piece(piece_class("W"), x, 7)

    def undo_move(self):
        last_move = self.history.pop()
        piece = last_move["piece"]
        target = last_move["target"]
        start = last_move["start"]
        end = last_move["end"]
        # undo castling
        if isinstance(piece, King) and abs(start[0] - end[0]) == 2:
            dir_x = 1 if end[0] > start[0] else -1
            rook_x = 7 if end[0] > start[0] else 0
            self.board.remove_piece(start[0] + dir_x, start[1])
            self.board.add_piece(Rook(piece.color), rook_x, start[1])
        # undo move
        self.board.remove_piece(end[0], end[1])
        self.board.add_piece(piece, start[0], start[1])
        self.white_timer = last_move["white_timer"]
        self.black_timer = last_move["black_timer"]
        if isinstance(piece, Rook) or isinstance(piece, King):
            piece.has_moved = last_move["has_moved"]
        if target is not None:
            self.board.add_piece(target, end[0], end[1])
        # en passant
        elif (end[0], end[1]) == last_move["en_passant_target"]:
            value = 1 if piece.color == "W" else -1
            color = "B" if piece.color == "W" else "W"
            self.board.add_piece(Pawn(color), end[0], end[1] + value)
        self.board.en_passant_target = last_move["en_passant_target"]
                

    def check(self):
        if self.turn == "W":
            my_king_coords = self.board.white_king_coords
            other_coords = self.board.black_pieces_coords
        else:
            my_king_coords = self.board.black_king_coords
            other_coords = self.board.white_pieces_coords
        for x, y in other_coords:
            piece = self.board.get_piece_at(x, y)
            piece_moves = piece.get_possible_moves(x, y, self.board)
            if my_king_coords in piece_moves:
                return True
        return False

    def get_all_legal_moves(self):
        legal_moves = []
        if self.turn == "W":
            my_coords = list(self.board.white_pieces_coords)
        else:
            my_coords = list(self.board.black_pieces_coords)
        for start_x, start_y in my_coords:
            piece = self.board.get_piece_at(start_x, start_y)
            piece_moves = piece.get_possible_moves(start_x, start_y, self.board)
            for end_x, end_y in piece_moves:
                # simulate move
                self.board.move(self, start_x, start_y, end_x, end_y)
                if not self.check():
                    # castling comprobations
                    if isinstance(piece, King) and abs(start_x - end_x) == 2:
                        self.undo_move()
                        was_in_check = self.check()
                        dir_x = 1 if end_x > start_x else -1
                        self.board.move(self, start_x, start_y, start_x + dir_x, start_y)
                        passed_trough_check = self.check()
                        if was_in_check or passed_trough_check:
                            self.undo_move()
                            continue
                    legal_moves.append(((start_x, start_y), (end_x, end_y)))
                self.undo_move()
        return legal_moves
    
    def pawn_promotion(self, x, y):
        pawn = self.board.get_piece_at(x, y)
        if not(y == 0 or y == 7) or not isinstance(pawn, Pawn):
            return False
        while True:
            piece_to_promote = input("\nPawn promotion (Q, R, B, N): ").strip().upper()
            self.board.remove_piece(x, y)
            if piece_to_promote == "Q":
                self.board.add_piece(Queen(pawn.color), x, y)
            elif piece_to_promote == "R":
                self.board.add_piece(Rook(pawn.color, has_moved = True), x, y)
            elif piece_to_promote == "B":
                self.board.add_piece(Bishop(pawn.color), x, y)
            elif piece_to_promote == "N":
                self.board.add_piece(Knight(pawn.color), x, y)
            else:
                print("\nPiece invalid, try again")
                continue
            return True

    def play_move(self, start, end):
        legal_moves = self.get_all_legal_moves()
        # Checkmate and stalemate comprobations
        if len(legal_moves) == 0:
            check = self.check()
            if check:
                return "CHECKMATE"
            return "STALEMATE"
        for legal_start, legal_end in legal_moves:
            if legal_start == start and legal_end == end:
                piece = self.board.get_piece_at(start[0], start[1])
                self.board.move(self, start[0], start[1], end[0], end[1])
                # En passant
                if isinstance(piece, Pawn) and abs(end[1] - start[1]) == 2:
                    value = -1 if self.turn == "W" else 1
                    self.board.en_passant_target = (start[0], start[1] + value)
                else:
                    self.board.en_passant_target = None
                # Pawn promotion
                self.pawn_promotion(end[0], end[1])
                # has_moved parameter comprobation for castling
                if isinstance(piece, King):
                    piece.has_moved = True
                elif isinstance(piece, Rook):
                    piece.has_moved = True
                # Timer and swap turn logic
                current_time = time.time()
                time_spent = current_time - self.turn_time
                if self.turn  == "W":
                    if self.white_timer - time_spent <= 0:
                        return "TIMEOUT"
                    else:
                        self.white_timer -= time_spent
                    self.turn = "B"
                else:
                    self.black_timer -= time_spent
                    if self.black_timer <= 0:
                        return "TIMEOUT"
                    self.turn = "W"
                self.turn_time = time.time()
                return "SUCCESS"
        return "INVALID"