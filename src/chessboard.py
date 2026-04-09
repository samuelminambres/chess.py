from pieces import *

class Chessboard:

    def __init__(self):
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
        return self._grid

    @property
    def white_pieces_coords(self):
        return self._white_pieces_coords
    
    @property
    def black_pieces_coords(self):
        return self._black_pieces_coords
    
    @property
    def white_king_coords(self):
        return self._white_king_coords
    
    @white_king_coords.setter
    def white_king_coords(self, value):
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
        return self._black_king_coords
    
    @black_king_coords.setter
    def black_king_coords(self, value):
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
        return self._en_passant_target
    
    @en_passant_target.setter
    def en_passant_target(self, value):
        if value is not None:
            if not isinstance(value, tuple):
                raise TypeError("En passant target must be coords (tuple) or None")
            if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
                raise TypeError("Coords not valid")
            if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
                raise TypeError("Coords not valid")
        self._en_passant_target = value

    def __str__(self):
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

    def add_piece(self, piece, x, y):
        if self.get_piece_at(x, y) is not None:
            return False
        self.grid[y][x] = piece
        if piece.color == "W":
            self.white_pieces_coords.append((x,y))
            if isinstance(piece, King):
                self.white_king_coords = (x,y)
        else:
            self.black_pieces_coords.append((x,y))
            if isinstance(piece, King):
                self.black_king_coords = (x,y)
        return True

    def remove_piece(self, x, y):
        piece = self.get_piece_at(x, y)
        if piece is None:
            return False
        if piece.color == "W":
            self.white_pieces_coords.remove((x,y))
            if isinstance(piece, King):
                self.white_king_coords = None
        else:
            self.black_pieces_coords.remove((x,y))
            if isinstance(piece, King):
                self.black_king_coords = None
        self.grid[y][x] = None
        return True

    def get_piece_at(self, x, y):
        return self.grid[y][x]
    
    def move(self, start_x, start_y, end_x, end_y):
        piece = self.get_piece_at(start_x, start_y)
        if piece is None:
            return False
        possible_moves = piece.get_possible_moves(start_x, start_y, self)
        if (end_x, end_y) not in possible_moves:
            return False
        target_piece = self.get_piece_at(end_x, end_y)
        # Castling
        if isinstance(piece, King) and abs(start_x - end_x) == 2:
            # left rook
            if start_x - end_x == 2:
                self.remove_piece(start_x, start_y)
                self.remove_piece(start_x - 4, start_y)
                value = -1
            # right rook
            elif end_x - start_x == 2:
                self.remove_piece(start_x, start_y)
                self.remove_piece(start_x + 3, start_y)
                value = 1
            self.add_piece(Rook(piece.color), start_x + value, start_y)
            self.add_piece(piece, start_x + 2*value, start_y)
            rook = self.get_piece_at(start_x + value, start_y)
            rook.has_moved = True
            piece.has_moved = True
            return True
        if target_piece is not None:
            self.remove_piece(end_x, end_y)
        elif (end_x, end_y) == self.en_passant_target:
            value = 1 if piece.color == "W" else -1
            self.remove_piece(end_x, end_y + value)
        self.remove_piece(start_x, start_y)
        self.add_piece(piece, end_x, end_y)
        return True