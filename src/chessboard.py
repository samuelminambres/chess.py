from pieces import *

class Chessboard:
    """Manages the 8x8 chessboard state, piece positions, and board movements.

    Attributes:
        grid (list[list[Piece or None]]): 2D list representing squares on the 8x8 board.
        white_pieces_coords (list[tuple]): Coordinates of all active White pieces.
        black_pieces_coords (list[tuple]): Coordinates of all active Black pieces.
        white_king_coords (tuple or None): Current coordinates of the White king.
        black_king_coords (tuple or None): Current coordinates of the Black king.
        en_passant_target (tuple or None): Target coordinates eligible for en passant.
    """

    def __init__(self):
        """Initializes an empty 8x8 chessboard and resets state variables."""
        grid = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(None)
            grid.append(row)
        self._grid = grid
        self._white_pieces_coords = []
        self._black_pieces_coords = []
        self.white_king_coords = None
        self.black_king_coords = None
        self.en_passant_target = None

    @property
    def grid(self):
        """Gets the 8x8 chessboard grid.

        Returns:
            list[list[Piece or None]]: The 2D grid containing pieces or None.
        """
        return self._grid

    @property
    def white_pieces_coords(self):
        """Gets coordinates of all active white pieces.

        Returns:
            list[tuple]: List of (x, y) coordinate tuples for white pieces.
        """
        return self._white_pieces_coords
    
    @property
    def black_pieces_coords(self):
        """Gets coordinates of all active black pieces.

        Returns:
            list[tuple]: List of (x, y) coordinate tuples for black pieces.
        """
        return self._black_pieces_coords
    
    @property
    def white_king_coords(self):
        """Gets coordinates of the white king.

        Returns:
            tuple or None: (x, y) coordinates of the white king, or None.
        """
        return self._white_king_coords
    
    @white_king_coords.setter
    def white_king_coords(self, value):
        """Sets coordinates of the white king.

        Args:
            value (tuple or None): (x, y) coordinates of the white king, or None.

        Raises:
            TypeError: If value is not a tuple or None, or coordinates are not valid integers (0-7).
        """
        if value is not None:
            if not isinstance(value, tuple):
                raise TypeError("King's coords must be tuple or None")
            if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
                raise TypeError("Coords not valid")
            if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
                raise TypeError("Coords not valid")
        self._white_king_coords = value

    @property
    def black_king_coords(self):
        """Gets coordinates of the black king.

        Returns:
            tuple or None: (x, y) coordinates of the black king, or None.
        """
        return self._black_king_coords
    
    @black_king_coords.setter
    def black_king_coords(self, value):
        """Sets coordinates of the black king.

        Args:
            value (tuple or None): (x, y) coordinates of the black king, or None.

        Raises:
            TypeError: If value is not a tuple or None, or coordinates are not valid integers (0-7).
        """
        if value is not None:
            if not isinstance(value, tuple):
                raise TypeError("King's coords must be tuple or None")
            if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
                raise TypeError("Coords not valid")
            if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
                raise TypeError("Coords not valid")
        self._black_king_coords = value
    
    @property
    def en_passant_target(self):
        """Gets current en passant target square coordinates.

        Returns:
            tuple or None: (x, y) coordinates of target square, or None.
        """
        return self._en_passant_target
    
    @en_passant_target.setter
    def en_passant_target(self, value):
        """Sets current en passant target square coordinates.

        Args:
            value (tuple or None): (x, y) coordinates of target square, or None.

        Raises:
            TypeError: If value is not a tuple or None, or coordinates are not valid integers (0-7).
        """
        if value is not None:
            if not isinstance(value, tuple):
                raise TypeError("En passant target must be coords (tuple) or None")
            if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
                raise TypeError("Coords not valid")
            if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
                raise TypeError("Coords not valid")
        self._en_passant_target = value

    def __str__(self):
        """Returns a colored ANSI string representation of the chessboard.

        Returns:
            str: String representing the chessboard with ANSI background colors.
        """
        result = "   A  B  C  D  E  F  G  H  "
        for y in range(8):
            result += f"\n{8 - y} "
            for x in range(8):
                square = self.grid[y][x]
                is_light_square = (x + y) % 2 == 0
                bg_color = "\033[47m" if is_light_square else "\033[100m"
                reset = "\033[0m"
                if square is None:
                    result += f"{bg_color}   {reset}"
                elif square.color == "W":
                    if is_light_square:
                        result += f"{bg_color} {square.tuple_print()[1]} {reset}"
                    else:
                        result += f"{bg_color} {square.tuple_print()[0]} {reset}"
                else:
                    if is_light_square:
                        result += f"{bg_color} {square.tuple_print()[0]} {reset}"
                    else:
                        result += f"{bg_color} {square.tuple_print()[1]} {reset}"
        return result

    def add_piece(self, piece, coords):
        """Adds a piece to the board at the specified coordinates.

        Args:
            piece (Piece): The piece to add to the chessboard.
            coords (tuple): The (x, y) coordinates where the piece will be placed.

        Returns:
            bool: True if the piece was successfully placed, False if square is occupied.
        """
        if self.get_piece_at(coords) is not None:
            return False
        
        x, y = coords
        self.grid[y][x] = piece

        if piece.color == "W":
            self.white_pieces_coords.append(coords)

            if isinstance(piece, King):
                self.white_king_coords = coords
        else:
            self.black_pieces_coords.append(coords)

            if isinstance(piece, King):
                self.black_king_coords = coords
        return True

    def remove_piece(self, coords):
        """Removes the piece at the specified coordinates from the board.

        Args:
            coords (tuple): The (x, y) coordinates of the piece to remove.

        Returns:
            bool: True if a piece was removed, False if square was empty.
        """
        piece = self.get_piece_at(coords)

        if piece is None:
            return False
        
        x, y = coords

        if piece.color == "W":
            self.white_pieces_coords.remove(coords)

            if isinstance(piece, King):
                self.white_king_coords = None
        else:
            self.black_pieces_coords.remove(coords)

            if isinstance(piece, King):
                self.black_king_coords = None

        self.grid[y][x] = None

        return True

    def get_piece_at(self, coords):
        """Retrieves the piece located at the given coordinates.

        Args:
            coords (tuple): The (x, y) coordinates on the board.

        Returns:
            Piece or None: The piece at the coordinates, or None if empty.
        """
        x, y = coords
        return self.grid[y][x]
    
    def move(self, start, end):
        """Executes a move on the board including castling, captures, and en passant.

        Args:
            start (tuple): The starting (x, y) coordinates of the piece.
            end (tuple): The destination (x, y) coordinates.

        Returns:
            bool: True if the move was valid and performed, False otherwise.
        """
        piece = self.get_piece_at(start)
        if piece is None:
            return False
        
        possible_moves = piece.get_possible_moves(self, start)
        if end not in possible_moves:
            return False
        
        target = self.get_piece_at(end)
        if target is not None:
            self.remove_piece(end)
        
        # Castling
        start_x, start_y = start
        end_x, end_y = end

        if isinstance(piece, King) and abs(start_x - end_x) == 2:
            dir_x = 1 if end_x > start_x else -1
            rook_x = 7 if end_x > start_x else 0
            self.remove_piece((rook_x, start_y))
            self.add_piece(Rook(piece.color, True), (start_x + dir_x, start_y))
            piece.has_moved = True
        elif isinstance(piece, King):
            piece.has_moved = True
        elif isinstance(piece, Rook):
            piece.has_moved = True

        # En passant
        if isinstance(piece, Pawn) and end == self.en_passant_target:
            value = 1 if piece.color == "W" else -1
            self.remove_piece((end_x, end_y + value))
            self.en_passant_target = None
        elif isinstance(piece, Pawn) and abs(end_y - start_y) == 2:
            value = -1 if piece.color == "W" else 1
            self.en_passant_target = (start_x, start_y + value)
        else:
            self.en_passant_target = None
        
        self.remove_piece(start)
        self.add_piece(piece, end)
        return True