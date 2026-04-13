from game import Game
from utils import seg_to_min_seg

game = Game()
game.setup_standard_board()

while True:
    if game.turn == "W":
        print(f"Whites' turn: {seg_to_min_seg(game.white_timer)}\n")
    else:
        print(f"Blacks' turn: {seg_to_min_seg(game.black_timer)}\n")

    while True:
        print(game.board)
        move_input = input('\nEnter move (e.g. e2e4) or "undo": ').strip().lower()
        if move_input == "undo":
            if game.history.length == 0:
                print("\nError: no moves to undo, try again\n")
                continue
            game.undo_move()
            game.turn = "B" if game.turn == "W" else "W"
            print("\nMove undone succesfully!\n")
            break
        start = move_input[:2]
        end = move_input[2:]
        try:
            result = game.play_move(start, end)
        except ValueError:
            print("\nError: coords not valid, try again\n")
            continue
        if result == "INVALID":
            print("\nIllegal movement, try again\n")
            continue
        break
    
    if move_input == "undo":
        continue

    if result == "SUCCESS":
        print("\nSuccesful movement!\n")
        continue
    elif result == "CHECKMATE":
        print("\n¡CHECKMATE! You lose")
    elif result == "\nSTALEMATE":
        print("\n¡STALEMATE! Tie")
    else:
        print("\nTime is out, you lose")
    break