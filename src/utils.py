import time

def to_coords(square):
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

def seg_to_min_seg(s):
    return time.strftime("%M:%S", time.gmtime(s*1000 // 1000))