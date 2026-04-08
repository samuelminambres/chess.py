from chessboard import Chessboard
from pieces import *
from stack import Stack
import time

class Game:

    def __init__(self, time = 600):
        self.board = Chessboard()
        self.turn = "W"
        self.white_timer = time
        self.black_timer = time
        self.history = Stack()

    def check_check(self):
        pass

    def check_checkmate(self):
        pass

    def play_move(self):
        pass

    def take(self):
        pass

    def get_all_legal_moves(self):
        pass

    def setup_standard_board(self):
        for i in range(8):
            self.board.add_piece(Pawn("B"), i, 1)
            self.board.add_piece(Pawn("W"), i, 6)
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for x, piece_class in enumerate(back_rank):
            self.board.add_piece(piece_class("B"), x, 0)
            self.board.add_piece(piece_class("W"), x, 7)