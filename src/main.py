from game import Game
from utils import seg_to_min_seg

game = Game()
game.setup_standard_board()
counter = 0

while True:
    if game.turn == "W":
        print(f"Whites' turn: {seg_to_min_seg(game.white_timer)}\n")
    else:
        print(f"Blacks' turn: {seg_to_min_seg(game.black_timer)}\n")

    while True:
        print(game.board)
        start = input("\nFrom (Ex: A1, G7): ")
        end = input("To: ")
        try:
            result = game.play_move(start, end)
        except ValueError:
            print("\nError: square not valid, try again\n")
            continue
        if result == "INVALID":
            print("\nIllegal movement, try again\n")
            continue
        break

    if result == "SUCCESS":
        print("\nSuccesful movement, your turn is over\n")
        counter += 1
        if counter >= 5:
            print(game)
        continue
    elif result == "CHECKMATE":
        print("\n¡CHECKMATE! You lose")
    elif result == "\nSTALEMATE":
        print("\n¡STALEMATE! Tie")
    else:
        print("\nTime is out, you lose")
    break