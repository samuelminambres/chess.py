class Piece:

    def __init__(self, color):
        self.color = color
        self._directions = None
        self.has_moved = None
        self.value = None
        self._piece_square_table = None

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError("Color must be str")
        if value != "W" and value != "B":
            raise ValueError('Color must be "W" or "B"')
        self._color = value

    @property
    def directions(self):
        return self._directions
    
    @property
    def has_moved(self):
        return self._has_moved
    
    @has_moved.setter
    def has_moved(self, value):
        if not isinstance(value, bool) and value is not None:
            raise TypeError("Has moved must be bool")
        self._has_moved = value

    @property
    def piece_square_table(self):
        return self._piece_square_table

    def get_possible_moves(self, board, coords):
        possible_moves = []
        for dir_x, dir_y in self.directions:
            current_x, current_y = coords
            while True:
                current_x += dir_x
                current_y += dir_y
                current_coords = (current_x, current_y)
                if not (0 <= current_x <= 7 and 0 <= current_y <= 7):
                    break
                target = board.get_piece_at(current_coords)
                if target is None:
                    possible_moves.append(current_coords)
                elif self.color != target.color:
                    possible_moves.append(current_coords)
                    break
                else:
                    break
        return possible_moves

class Pawn(Piece):

    def __init__(self, color):
        super().__init__(color)
        self._directions = (0,1) if self.color == "B" else (0,-1)
        self.value = 1
        self._piece_square_table = [
[ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
[ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
[ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
[ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
[ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
[ 0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
[ 0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
[ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
]

    def __str__(self):
        return "♟" if self.color == "W" else "♙"
    
    def tuple_print(self):
        return ("♟", "♙")

    def get_possible_moves(self, board, coords):
        possible_moves = []
        x, y = coords
        dir_x, dir_y = self.directions
        end_x = x + dir_x
        end_y = y + dir_y
        end = (end_x, end_y)
        if 0 <= end_y <= 7:
            if board.get_piece_at(end) is None:
                possible_moves.append(end)
                if ((self.color == "W" and y == 6) or (self.color == "B" and y == 1)) and board.get_piece_at((end_x, y + 2*dir_y)) is None:
                    possible_moves.append((x, y + 2*dir_y))
            if x - 1 >= 0:
                target_left = board.get_piece_at((x - 1, end_y))
                if (target_left is not None and self.color != target_left.color) or (x - 1, end_y) == board.en_passant_target:
                    possible_moves.append((x - 1, end_y))
            if x + 1 <= 7: 
                target_right = board.get_piece_at((x + 1, end_y))
                if (target_right is not None and self.color != target_right.color) or (x + 1, end_y) == board.en_passant_target:
                    possible_moves.append((x + 1, end_y))
        return possible_moves

class Knight(Piece):
    
    def __init__(self, color):
        super().__init__(color)
        self._directions = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]
        self.value = 3
        self._piece_square_table = [
[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
[-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
[-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
[-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
[-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
[-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
[-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]
    
    def tuple_print(self):
        return ("♞", "♘")

    def get_possible_moves(self, board, coords):
        possible_moves = []
        x, y = coords
        for dir_x, dir_y in self.directions:
            end_x = x + dir_x
            end_y = y + dir_y
            if 0 <= end_x <= 7 and 0 <= end_y <= 7:
                target = board.get_piece_at((end_x, end_y))
                if target is None or target.color != self.color:
                    possible_moves.append((end_x, end_y))
        return possible_moves

class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color)
        self._directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        self.value = 3
        self._piece_square_table = [
[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
[-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
[-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
[-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
[-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
[-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
[-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

    def tuple_print(self):
        return ("♝", "♗")
    
class Rook(Piece):

    def __init__(self, color, has_moved = False):
        super().__init__(color)
        self._directions = [(1,0), (-1,0), (0,1), (0,-1)]
        self.has_moved = has_moved
        self.value = 5
        self._piece_square_table = [
[ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
[ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
[-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
[-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
[-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
[-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
[-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
[ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]
    
    def tuple_print(self):
        return ("♜", "♖")

class Queen(Piece):

    def __init__(self, color):
        super().__init__(color)
        self._directions = [(1,1), (1,-1), (-1,1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]
        self.value = 9
        self._piece_square_table = [
[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
[-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
[-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
[-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
[ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
[-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
[-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]
    
    def tuple_print(self):
        return ("♛", "♕")

class King(Piece):

    def __init__(self, color, has_moved = False):
        super().__init__(color)
        self._directions = [(1,1), (1,-1), (-1,1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]
        self.has_moved = has_moved
        self.value = 900
        self._piece_square_table = [
[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
[-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
[-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
[ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
[ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
]
    
    def tuple_print(self):
        return ("♚", "♔")

    def get_possible_moves(self, board, coords):
        possible_moves = []
        x, y = coords
        for dir_x, dir_y in self.directions:
            end_x = x + dir_x
            end_y = y + dir_y
            if 0 <= end_x <= 7 and 0 <= end_y <= 7:
                target = board.get_piece_at((end_x, end_y))
                if target is None:
                    possible_moves.append((end_x, end_y))
                elif self.color != target.color:
                    possible_moves.append((end_x, end_y))
        value = 7 if self.color == "W" else 0
        right_rook = board.get_piece_at((7, value))
        left_rook = board.get_piece_at((0, value))
        if not self.has_moved and isinstance(right_rook, Rook) and not right_rook.has_moved and board.get_piece_at((x + 1, y)) is None and board.get_piece_at((x + 2, y)) is None:
            possible_moves.append((x + 2, y))
        if not self.has_moved and isinstance(left_rook, Rook) and not left_rook.has_moved and board.get_piece_at((x - 1, y)) is None and board.get_piece_at((x - 2, y)) is None and board.get_piece_at((x - 3, y)) is None:
            possible_moves.append((x - 2, y))
        return possible_moves
                    