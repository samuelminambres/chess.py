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

def seg_to_min_seg(s):
    return time.strftime("%M:%S", time.gmtime(s*1000 // 1000))