from chessboard import Chessboard
from pieces import *
from stack import Stack
import time
from utils import to_coords, to_notation
import copy

class Game:

    def __init__(self, time_limit = 600.0):
        self.board = Chessboard()
        self.turn = "W"
        self.white_timer = time_limit
        self.black_timer = time_limit
        self.turn_time = time.time()
        self.history = Stack()

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
        if not isinstance(value, Stack):
            raise TypeError("History must be Stack")
        self._history = value

    def __str__(self):
        result = ""
        for node in self.history:
            result += f"{type(node.value["piece"]).__name__}: {to_notation(node.value["start"])} -> {to_notation(node.value["end"])}\n\n{node.value["board_before"]}\n\n"
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
        self.board = last_move.value["board_before"]

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
                self.history.push({"piece": piece, "start": (start_x, start_y), "end": (end_x, end_y), "board_before": copy.deepcopy(self.board)})
                self.board.move(start_x, start_y, end_x, end_y)
                if not self.check():
                    # castling comprobations
                    if isinstance(piece, King) and abs(start_x - end_x) == 2:
                        self.undo_move()
                        was_in_check = self.check()
                        dir_x = 1 if end_x > start_x else -1
                        self.history.push({"piece": piece, "start": (start_x, start_y), "end": (start_x + dir_x, start_y), "board_before": copy.deepcopy(self.board)})
                        self.board.move(start_x, start_y, start_x + dir_x, start_y)
                        passed_trough_check = self.check()
                        if was_in_check or passed_trough_check:
                            self.undo_move()
                            continue
                    legal_moves.append(((start_x, start_y), (end_x, end_y)))
                self.undo_move()
        return legal_moves

    def play_move(self, notation_start, notation_end):
        coords_start = to_coords(notation_start)
        coords_end = to_coords(notation_end)
        legal_moves = self.get_all_legal_moves()
        if len(legal_moves) == 0:
            check = self.check()
            if check:
                return "CHECKMATE"
            return "STALEMATE"
        for legal_start, legal_end in legal_moves:
            if legal_start == coords_start and legal_end == coords_end:
                piece = self.board.get_piece_at(coords_start[0], coords_start[1])
                self.history.push({"piece": piece, "start": coords_start, "end": coords_end, "board_before": copy.deepcopy(self.board)})
                self.board.move(coords_start[0], coords_start[1], coords_end[0], coords_end[1])
                # En passant
                if isinstance(piece, Pawn) and abs(coords_end[1] - coords_start[1]) == 2:
                    value = -1 if self.turn == "W" else 1
                    self.board.en_passant_target = (coords_start[0], coords_start[1] + value)
                else:
                    self.board.en_passant_target = None
                # Pawn promotion
                if (coords_end[1] == 0 or coords_end[1] == 7) and isinstance(piece, Pawn):
                    self.board.remove_piece(coords_end[0], coords_end[1])
                    self.board.add_piece(Queen(piece.color), coords_end[0], coords_end[1])
                if isinstance(piece, King):
                    piece.has_moved = True
                elif isinstance(piece, Rook):
                    piece.has_moved = True
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
