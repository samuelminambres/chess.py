from pieces import Piece

class Move:

    def __init__(self, start: tuple, end: tuple, piece: Piece, target, en_passant_target, has_moved: bool, half_move_clock: int):
        self.piece = piece
        self.target = target
        self.start = start
        self.end = end
        self.en_passant_target = en_passant_target
        self.has_moved = has_moved

    @property
    def piece(self):
        return self._piece
    
    @piece.setter
    def piece(self, value):
        if not isinstance(value, Piece):
            raise TypeError("Piece must be Piece")
        self._piece = value
    
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, value):
        if value is not None:
            if not isinstance(value, Piece):
                raise TypeError("Target must be Piece or None")
        self._target = value
    
    @property
    def start(self):
        return self._start
    
    @start.setter
    def start(self, value):
        if not isinstance(value, tuple):
            raise TypeError("Coords must be tuple")
        if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
            raise ValueError("Coords not valid")
        if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
            raise ValueError("Coords not valid")
        self._start = value
    
    @property
    def end(self):
        return self._end
    
    @end.setter
    def end(self, value):
        if not isinstance(value, tuple):
            raise TypeError("Coords must be tuple")
        if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
            raise ValueError("Coords not valid")
        if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
            raise ValueError("Coords not valid")
        self._end = value
    
    @property
    def en_passant_target(self):
        return self._en_passant_target
    
    @en_passant_target.setter
    def en_passant_target(self, value):
        if value is not None:
            if not isinstance(value, tuple):
                raise TypeError("En passant target must be coords (tuple) or None")
            if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
                raise ValueError("Coords not valid")
            if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
                raise ValueError("Coords not valid")
        self._en_passant_target = value
    
    @property
    def has_moved(self):
        return self._has_moved
    
    @has_moved.setter
    def has_moved(self, value):
        if not isinstance(value, bool) and value is not None:
            raise TypeError("Has moved must be bool")
        self._has_moved = value
        
    @property
    def half_move_clock(self):
        return self._half_move_clock
    
    @half_move_clock.setter
    def half_move_clock(self, value):
        if not isinstance(value, int):
            raise TypeError("Counter value must be int")
        if value < 0:
            raise ValueError("Value must be 0 or greater")
        self._half_move_clock = value