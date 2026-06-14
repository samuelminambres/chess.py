from chessboard import Chessboard
from pieces import *
from utils import to_notation
from timer import Timer

class Game:

    def __init__(self, time_limit = 600.0, increment = 0.0):
        self.board = Chessboard()
        self.turn = "W"
        self.white_timer = Timer(time_limit, increment)
        self.black_timer = Timer(time_limit, increment)
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
        if not isinstance(value, Timer):
            raise TypeError("Timer must be a Timer")
        self._white_timer = value
    
    @property
    def black_timer(self):
        return self._black_timer
    
    @black_timer.setter
    def black_timer(self, value):
        if not isinstance(value, Timer):
            raise TypeError("Timer must be a Timer")
        self._black_timer = value

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
            result += f"{to_notation(move["start"])} -> {to_notation(move["end"])}\n"
        return result

    def setup_standard_board(self):
        for i in range(8):
            self.board.add_piece(Pawn("B"), (i, 1))
            self.board.add_piece(Pawn("W"), (i, 6))

        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for x, piece_class in enumerate(back_rank):
            self.board.add_piece(piece_class("B"), (x, 0))
            self.board.add_piece(piece_class("W"), (x, 7))

    def undo_move(self):
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

    def get_all_legal_moves(self):
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
                self.board.move(self, start, end)

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
        x, y = coords
        return (y == 0 or y == 7) and isinstance(self.board.get_piece_at(coords), Pawn)
    
    def promotion_to(self, piece, coords):
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
        if self.turn == "W":
            self.turn = "B"
        else:
            self.turn = "W"

    def play_move(self, start, end):
        legal_moves = self.get_all_legal_moves()

        # Checkmate and stalemate comprobations
        if len(legal_moves) == 0:
            check = self.check()
            if check:
                return "CHECKMATE"
            return "STALEMATE"
        
        if (start, end) not in legal_moves:
            return "INVALID"
        
        self.board.move(self, start, end)

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
        