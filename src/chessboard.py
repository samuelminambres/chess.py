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

    def add_piece(self, piece, coords):
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
        x, y = coords
        return self.grid[y][x]
    
    def move(self, game, start, end):
        piece = self.get_piece_at(start)
        if piece is None:
            return False
        possible_moves = piece.get_possible_moves(self, start)
        if end not in possible_moves:
            return False
        game.history.append({"piece": piece, "target": self.get_piece_at(end), "start": start, "end": end, "en_passant_target": self.en_passant_target, "has_moved": piece.has_moved, "white_timer": game.white_timer, "black_timer": game.black_timer})
        target_piece = self.get_piece_at(end)
        if target_piece is not None:
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