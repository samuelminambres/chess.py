from chessboard import Chessboard
from pieces import *
from stack import Stack
import time
from utils import to_coords

class Game:

    def __init__(self, time_limit = 600.0):
        self.board = Chessboard()
        self.turn = "W"
        self.white_timer = time_limit
        self.black_timer = time_limit
        self.turn_time = time.time()
        self.history = Stack()

    def setup_standard_board(self):
        for i in range(8):
            self.board.add_piece(Pawn("B"), i, 1)
            self.board.add_piece(Pawn("W"), i, 6)
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for x, piece_class in enumerate(back_rank):
            self.board.add_piece(piece_class("B"), x, 0)
            self.board.add_piece(piece_class("W"), x, 7)

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

    def checkmate(self):
        if not self.check():
            return False
        if len(self.get_all_legal_moves()) != 0:
            return False
        return True
    
    def stalemate(self):
        if self.check():
            return False
        if len(self.get_all_legal_moves()) != 0:
            return False
        return True

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
                # save piece
                target = self.board.get_piece_at(end_x, end_y)
                # simulate move
                self.board.remove_piece(start_x, start_y)
                self.board.add_piece(piece, end_x, end_y)
                check = self.check()
                # undo move
                self.board.remove_piece(end_x, end_y)
                self.board.add_piece(piece, start_x, start_y)
                if target:
                    self.board.add_piece(target, end_x, end_y)
                if not check:
                    legal_moves.append(((start_x, start_y), (end_x, end_y)))
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
                self.board.move(coords_start[0], coords_start[1], coords_end[0], coords_end[1])
                self.history.push(f"{type(piece).__name__}: {notation_start.upper()} -> {notation_end.upper()}")
                # Pawn promotion
                if (coords_end[1] == 0 or coords_end[1] == 7) and isinstance(piece, Pawn):
                    self.board.remove_piece(coords_end[0], coords_end[1])
                    self.board.add_piece(Queen(piece.color), coords_end[0], coords_end[1])
                current_time = time.time()
                time_spent = current_time - self.turn_time
                if self.turn  == "W":
                    self.white_timer -= time_spent
                    if self.white_timer <= 0:
                        return "TIMEOUT"
                    self.turn = "B"
                else:
                    self.black_timer -= time_spent
                    if self.black_timer <= 0:
                        return "TIMEOUT"
                    self.turn = "W"
                self.turn_time = time.time()
                return "SUCCESS"
        return "INVALID"