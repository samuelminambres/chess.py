def to_coords(square):
    """Converts algebraic chess notation to grid coordinates.

    Args:
        square (str): The chess square algebraic notation (e.g., 'E4', 'A1').

    Returns:
        tuple[int, int]: The (x, y) board coordinates, 0-indexed from top-left.

    Raises:
        ValueError: If the notation length is not 2, the file letter is invalid,
            the second character is not a digit, or the rank number is not
            between 1 and 8.
    """
    square = square.upper().strip()
    if len(square) != 2:
        raise ValueError("Length not valid")
    rank = range(8,0, -1)
    file = ["A", "B", "C", "D", "E", "F", "G", "H"]
    if square[0] not in file:
        raise ValueError("Letter not valid")
    try:
        y = 8 - int(square[1])
    except ValueError:
        raise ValueError("Second character must be a number")
    if not (1 <= int(square[1]) <= 8):
        raise ValueError("Number must be between 1 and 8")
    return file.index(square[0]), y

def to_notation(coords):
    """Converts grid coordinates to algebraic chess notation.

    Args:
        coords (tuple[int, int]): The (x, y) board coordinates, 0-indexed.

    Returns:
        str: The algebraic notation corresponding to the coordinates (e.g., 'E4').

    Raises:
        TypeError: If coords is not a tuple or if coordinate components are not integers.
        ValueError: If coords length is not 2 or coordinates are not between 0 and 7.
    """
    if not isinstance(coords, tuple):
        raise TypeError("Coords must be tuple")
    if len(coords) != 2:
        raise ValueError("Length not valid")
    if not isinstance(coords[0], int) or not isinstance(coords[1], int):
        raise TypeError("Each coords must be int")
    if not(0 <= coords[0] <= 7) or not(0 <= coords[1] <= 7):
        raise ValueError("Coords not valid")
    file = ["A", "B", "C", "D", "E", "F", "G", "H"]
    return file[coords[0]] + str(8 - coords[1])