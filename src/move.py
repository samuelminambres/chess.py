from pieces import Piece

class Move:
    """Represents an executed chess move along with its historical state for undo operations.

    Attributes:
        piece (Piece): The piece that performed the move.
        target (Piece or None): The captured piece, if any.
        start (tuple): Starting coordinates (x, y).
        end (tuple): Destination coordinates (x, y).
        en_passant_target (tuple or None): En passant target square prior to the move.
        has_moved (bool): Moved status of the piece prior to the move.
        half_move_clock (int): Half-move clock counter value prior to the move.
    """

    def __init__(self, start: tuple, end: tuple, piece: Piece, target, en_passant_target, has_moved: bool, half_move_clock: int):
        """Initializes a Move instance.

        Args:
            start (tuple): The starting coordinates (x, y) of the move.
            end (tuple): The destination coordinates (x, y) of the move.
            piece (Piece): The piece that is making the move.
            target (Piece or None): The piece captured by the move, if any.
            en_passant_target (tuple or None): The en passant target coordinates before the move, or None.
            has_moved (bool): Whether the moving piece had already moved prior to this move.
            half_move_clock (int): Half-move clock count for the 50-move rule.
        """
        self.piece = piece
        self.target = target
        self.start = start
        self.end = end
        self.en_passant_target = en_passant_target
        self.has_moved = has_moved

    @property
    def piece(self):
        """Gets the piece making the move.

        Returns:
            Piece: The moving piece.
        """
        return self._piece
    
    @piece.setter
    def piece(self, value):
        """Sets the piece making the move.

        Args:
            value (Piece): The moving piece.

        Raises:
            TypeError: If value is not a Piece instance.
        """
        if not isinstance(value, Piece):
            raise TypeError("Piece must be Piece")
        self._piece = value
    
    @property
    def target(self):
        """Gets the captured piece.

        Returns:
            Piece or None: The captured piece, or None if no capture occurred.
        """
        return self._target
    
    @target.setter
    def target(self, value):
        """Sets the captured piece.

        Args:
            value (Piece or None): The captured piece, or None.

        Raises:
            TypeError: If value is not a Piece instance or None.
        """
        if value is not None:
            if not isinstance(value, Piece):
                raise TypeError("Target must be Piece or None")
        self._target = value
    
    @property
    def start(self):
        """Gets the starting coordinates of the move.

        Returns:
            tuple: The starting (x, y) coordinates.
        """
        return self._start
    
    @start.setter
    def start(self, value):
        """Sets the starting coordinates of the move.

        Args:
            value (tuple): The starting (x, y) coordinates.

        Raises:
            TypeError: If value is not a tuple.
            ValueError: If value does not contain two valid board integers (0-7).
        """
        if not isinstance(value, tuple):
            raise TypeError("Coords must be tuple")
        if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
            raise ValueError("Coords not valid")
        if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
            raise ValueError("Coords not valid")
        self._start = value
    
    @property
    def end(self):
        """Gets the destination coordinates of the move.

        Returns:
            tuple: The destination (x, y) coordinates.
        """
        return self._end
    
    @end.setter
    def end(self, value):
        """Sets the destination coordinates of the move.

        Args:
            value (tuple): The destination (x, y) coordinates.

        Raises:
            TypeError: If value is not a tuple.
            ValueError: If value does not contain two valid board integers (0-7).
        """
        if not isinstance(value, tuple):
            raise TypeError("Coords must be tuple")
        if len(value) != 2 or not isinstance(value[0], int) or not isinstance(value[1], int):
            raise ValueError("Coords not valid")
        if not (0 <= value[0] <= 7 and 0 <= value[1] <= 7):
            raise ValueError("Coords not valid")
        self._end = value
    
    @property
    def en_passant_target(self):
        """Gets the en passant target coordinates before the move.

        Returns:
            tuple or None: The en passant coordinates, or None.
        """
        return self._en_passant_target
    
    @en_passant_target.setter
    def en_passant_target(self, value):
        """Sets the en passant target coordinates before the move.

        Args:
            value (tuple or None): The en passant target coordinates, or None.

        Raises:
            TypeError: If value is not a tuple or None.
            ValueError: If coordinates do not consist of two valid board integers (0-7).
        """
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
        """Gets whether the piece had moved prior to this move.

        Returns:
            bool or None: True if piece had moved, False otherwise.
        """
        return self._has_moved
    
    @has_moved.setter
    def has_moved(self, value):
        """Sets whether the piece had moved prior to this move.

        Args:
            value (bool or None): True if the piece had moved, False otherwise.

        Raises:
            TypeError: If value is not a bool and not None.
        """
        if not isinstance(value, bool) and value is not None:
            raise TypeError("Has moved must be bool")
        self._has_moved = value
        
    @property
    def half_move_clock(self):
        """Gets the half-move clock counter for the 50-move rule.

        Returns:
            int: The half-move clock value.
        """
        return self._half_move_clock
    
    @half_move_clock.setter
    def half_move_clock(self, value):
        """Sets the half-move clock counter for the 50-move rule.

        Args:
            value (int): The half-move clock value.

        Raises:
            TypeError: If value is not an int.
            ValueError: If value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("Counter value must be int")
        if value < 0:
            raise ValueError("Value must be 0 or greater")
        self._half_move_clock = value