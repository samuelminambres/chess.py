class Piece:
    """Base class representing a chess piece on the board.

    Attributes:
        color (str): The piece color ('W' for White, 'B' for Black).
        directions (list or tuple or None): Direction vectors for piece movement.
        has_moved (bool or None): Whether the piece has moved from its initial square.
        value (int or None): Material value of the piece.
        piece_square_table (list[list[float]] or None): Positional bonus evaluation table.
    """

    def __init__(self, color):
        """Initializes a chess piece with its color.

        Args:
            color (str): The color of the piece, either 'W' (White) or 'B' (Black).
        """
        self.color = color
        self._directions = None
        self.has_moved = None
        self.value = None
        self._piece_square_table = None

    @property
    def color(self):
        """Gets the color of the piece.

        Returns:
            str: The piece color ('W' or 'B').
        """
        return self._color
    
    @color.setter
    def color(self, value):
        """Sets the color of the piece.

        Args:
            value (str): The piece color ('W' or 'B').

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is not 'W' or 'B'.
        """
        if not isinstance(value, str):
            raise TypeError("Color must be str")
        if value != "W" and value != "B":
            raise ValueError('Color must be "W" or "B"')
        self._color = value

    @property
    def directions(self):
        """Gets the movement direction vectors for the piece.

        Returns:
            list or tuple or None: Movement direction vectors (dx, dy).
        """
        return self._directions
    
    @property
    def has_moved(self):
        """Gets whether the piece has moved.

        Returns:
            bool or None: True if the piece has moved, False or None otherwise.
        """
        return self._has_moved
    
    @has_moved.setter
    def has_moved(self, value):
        """Sets whether the piece has moved.

        Args:
            value (bool or None): Flag indicating if the piece has moved.

        Raises:
            TypeError: If value is not a bool and not None.
        """
        if not isinstance(value, bool) and value is not None:
            raise TypeError("Has moved must be bool")
        self._has_moved = value

    @property
    def piece_square_table(self):
        """Gets the piece-square positional evaluation table.

        Returns:
            list[list[float]] or None: An 8x8 table of positional bonuses/penalties.
        """
        return self._piece_square_table

    def get_possible_moves(self, board, coords):
        """Calculates sliding piece moves along self.directions from given coordinates.

        Args:
            board (Chessboard): The chessboard instance.
            coords (tuple): Current (x, y) coordinates of the piece.

        Returns:
            list[tuple]: List of reachable destination coordinate tuples.
        """
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
    """Represents a Pawn chess piece with single/double advance, captures, and en passant.

    Attributes:
        color (str): The piece color ('W' or 'B').
        value (int): Material value of the pawn (1).
    """

    def __init__(self, color):
        """Initializes a Pawn with its color, movement direction, value, and square table.

        Args:
            color (str): The color of the pawn ('W' or 'B').
        """
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
        """Returns the Unicode character representation of the pawn.

        Returns:
            str: '♟' for White or '♙' for Black.
        """
        return "♟" if self.color == "W" else "♙"
    
    def tuple_print(self):
        """Returns Unicode symbols for dark and light square representations.

        Returns:
            tuple[str, str]: A tuple containing ('♟', '♙').
        """
        return ("♟", "♙")

    def get_possible_moves(self, board, coords):
        """Calculates all possible moves for the pawn including pushes, captures, and en passant.

        Args:
            board (Chessboard): The chessboard instance.
            coords (tuple): Current (x, y) coordinates of the pawn.

        Returns:
            list[tuple]: List of reachable destination coordinate tuples.
        """
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
    """Represents a Knight chess piece with L-shaped jumping movement.

    Attributes:
        color (str): The piece color ('W' or 'B').
        value (int): Material value of the knight (3).
    """
    
    def __init__(self, color):
        """Initializes a Knight with its color, L-shaped movement vectors, value, and square table.

        Args:
            color (str): The color of the knight ('W' or 'B').
        """
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
        """Returns Unicode symbols for dark and light square representations.

        Returns:
            tuple[str, str]: A tuple containing ('♞', '♘').
        """
        return ("♞", "♘")

    def get_possible_moves(self, board, coords):
        """Calculates all possible L-shaped jump moves for the knight.

        Args:
            board (Chessboard): The chessboard instance.
            coords (tuple): Current (x, y) coordinates of the knight.

        Returns:
            list[tuple]: List of reachable destination coordinate tuples.
        """
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
    """Represents a Bishop chess piece with diagonal sliding movement.

    Attributes:
        color (str): The piece color ('W' or 'B').
        value (int): Material value of the bishop (3).
    """

    def __init__(self, color):
        """Initializes a Bishop with its color, diagonal vectors, value, and square table.

        Args:
            color (str): The color of the bishop ('W' or 'B').
        """
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
        """Returns Unicode symbols for dark and light square representations.

        Returns:
            tuple[str, str]: A tuple containing ('♝', '♗').
        """
        return ("♝", "♗")
    
class Rook(Piece):
    """Represents a Rook chess piece with orthogonal sliding movement and castling capability.

    Attributes:
        color (str): The piece color ('W' or 'B').
        has_moved (bool): Whether the rook has moved from its original square.
        value (int): Material value of the rook (5).
    """

    def __init__(self, color, has_moved = False):
        """Initializes a Rook with its color, orthogonal vectors, moved status, value, and square table.

        Args:
            color (str): The color of the rook ('W' or 'B').
            has_moved (bool, optional): Whether the rook has already moved. Defaults to False.
        """
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
        """Returns Unicode symbols for dark and light square representations.

        Returns:
            tuple[str, str]: A tuple containing ('♜', '♖').
        """
        return ("♜", "♖")

class Queen(Piece):
    """Represents a Queen chess piece with orthogonal and diagonal sliding movement.

    Attributes:
        color (str): The piece color ('W' or 'B').
        value (int): Material value of the queen (9).
    """

    def __init__(self, color):
        """Initializes a Queen with its color, 8-directional vectors, value, and square table.

        Args:
            color (str): The color of the queen ('W' or 'B').
        """
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
        """Returns Unicode symbols for dark and light square representations.

        Returns:
            tuple[str, str]: A tuple containing ('♛', '♕').
        """
        return ("♛", "♕")

class King(Piece):
    """Represents a King chess piece with 1-square movement in any direction and castling.

    Attributes:
        color (str): The piece color ('W' or 'B').
        has_moved (bool): Whether the king has moved from its original square.
        value (int): Material value of the king (900).
    """

    def __init__(self, color, has_moved = False):
        """Initializes a King with its color, 8-directional vectors, moved status, value, and square table.

        Args:
            color (str): The color of the king ('W' or 'B').
            has_moved (bool, optional): Whether the king has already moved. Defaults to False.
        """
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
        """Returns Unicode symbols for dark and light square representations.

        Returns:
            tuple[str, str]: A tuple containing ('♚', '♔').
        """
        return ("♚", "♔")

    def get_possible_moves(self, board, coords):
        """Calculates all possible moves for the king including 1-square moves and castling.

        Args:
            board (Chessboard): The chessboard instance.
            coords (tuple): Current (x, y) coordinates of the king.

        Returns:
            list[tuple]: List of reachable destination coordinate tuples.
        """
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
                    